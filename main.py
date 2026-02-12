
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
from app import db

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return jsonify({"message": "SaaS Platform Running"})

@main_bp.route("/dashboard")
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user.plan == "free" and user.usage_count >= 20:
        return jsonify({"error": "Upgrade required"}), 403

    user.usage_count += 1
    db.session.commit()

    return jsonify({
        "message": "Access granted",
        "plan": user.plan,
        "usage": user.usage_count
    })
