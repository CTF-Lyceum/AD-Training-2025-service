from datetime import datetime, timedelta
from flask import Blueprint, request, render_template, redirect, url_for, make_response
import jwt
from config import SECRET_KEY
from app.database.models import User, db


auth_route = Blueprint("auth_route", __name__)

@auth_route.route("/", methods=['GET'])
def main():
    return render_template("auth/index.html")


@auth_route.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user:
            user.password = password
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)

        db.session.commit()

        return redirect(url_for('auth_route.login'))

    response = make_response(render_template("auth/register.html"))
    response.delete_cookie("can_edit_note")

    return response


@auth_route.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user:
            if password:
                token = jwt.encode(
                    {'username': username, 'exp': datetime.utcnow() + timedelta(hours=1)},
                    SECRET_KEY,
                    algorithm='HS256'
                )
                response = make_response(redirect(url_for('view_note_route.note_wall')))
                response.set_cookie('jwt_token', token, httponly=True)
                return response
            else:
                return render_template("errors/401.html")
        else:
            return render_template("errors/401.html")

    response = make_response(render_template('auth/login.html'))
    response.delete_cookie("can_edit_note")

    return response


