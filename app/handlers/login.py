import os
from datetime import datetime, timedelta
from flask import Blueprint, request, render_template, redirect, url_for, make_response
import json
import jwt
from config import SECRET_KEY


auth_route = Blueprint("auth_route", __name__)
ACCOUNTS_FILE = "app/service/database/accounts.json"


def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    else:
        return {}


def save_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


@auth_route.route("/", methods=['GET'])
def main():
    return render_template("auth/index.html")


@auth_route.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        accounts = load_data(ACCOUNTS_FILE)
        if username in accounts:
            accounts[username]["password"] = password
        else:
            accounts[username] = {"password": password}
        save_data(accounts, ACCOUNTS_FILE)

        return redirect(url_for('auth_route.login'))

    return render_template("auth/register.html")


@auth_route.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        accounts = load_data(ACCOUNTS_FILE)

        if accounts and username in accounts:
            # Проверяем соответствие пароля
            if accounts[username]["password"]:
                token = jwt.encode({'username': username, 'exp': datetime.utcnow() + timedelta(hours=1)}, SECRET_KEY,
                                   algorithm='HS256')
                response = make_response(redirect(url_for('view_note_route.note_wall')))
                response.set_cookie('jwt_token', token, httponly=True)
                return response
            else:
                return render_template("errors/401.html")
        else:
            return render_template("errors/401.html")

    return render_template('auth/login.html')

