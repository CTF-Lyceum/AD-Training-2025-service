from flask import Blueprint, jsonify
from app.database.models import db, User

users_route = Blueprint("users", __name__)


@users_route.route("/api/users", methods=["GET"])
def get_all_users():
    users = User.query.all()
    users_data = [
        {
            "id": user.id,
            "username": user.username,
            "password": user.password
        } for user in users
    ]

    return jsonify(users_data)