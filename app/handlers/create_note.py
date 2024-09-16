from datetime import datetime
from flask import Blueprint, request, render_template, redirect, url_for
import jwt
from .login import load_data, save_data
from config import SECRET_KEY

create_note_route = Blueprint("create_note_route", __name__)

NOTES_FILE = "app/database/notes.json"


def verify_jwt_cookie():
    jwt_token = request.cookies.get('jwt_token')
    if jwt_token:
        try:
            payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])
            username = payload.get('username')
            return username
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    return None


def get_last_id(notes):
    if notes:
        return max(int(note_id) for note_id in notes.keys())
    return 0


@create_note_route.route('/create_note', methods=["GET", 'POST'])
def create_note():
    notes = load_data(NOTES_FILE)
    id = get_last_id(notes)

    if request.method == "POST":
        username = verify_jwt_cookie()
        if not username:
            return redirect(url_for('auth_route.login'))

        title = request.form.get('title')
        content = request.form.get('content')
        visibility = request.form.get('visibility', 'private')
        author = username
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        id += 1

        new_note = {
            "id": str(id),
            'title': title,
            'content': content,
            'visibility': visibility,
            'author': author,
            'timestamp': timestamp
        }

        notes[new_note["id"]] = new_note
        save_data(notes, NOTES_FILE)

        return redirect(url_for("view_note_route.view_note", note_id=id))

    username = verify_jwt_cookie()
    if not username:
        return redirect(url_for('auth_route.login'))

    return render_template("notes/create_note.html", current_user=username)
