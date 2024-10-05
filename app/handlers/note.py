import re
import jwt
from flask import Blueprint, request, render_template, redirect, url_for, make_response
from config import SECRET_KEY
from .login import load_data


view_note_route = Blueprint("view_note_route", __name__)


NOTES_FILE = "app/database/notes.json"


@view_note_route.route("/note/<note_id>", methods=["GET"])
def view_note(note_id):
    if 'jwt_token' not in request.cookies:
        return redirect(url_for("auth_route.register"))
    jwt_token = request.cookies.get("jwt_token")
    if jwt_token:
        try:
            payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])
            username = payload.get('username')
            if not username:
                return '''401\n Unauthorized'''
        except jwt.ExpiredSignatureError:
            return '''401\nToken expired'''''
        except jwt.InvalidTokenError:
            return '''401\n Token is invalid'''
    notes = load_data(NOTES_FILE)
    note = notes.get(note_id)

    if note:
        if note["visibility"] == "private":
            if username != note['author'] and username != "admin":
                return render_template('errors/404.html')
        if username != note['author'] and username != "admin":
            can_edit = "0"
        else:
            can_edit = "1"
        response = make_response(render_template('notes/view_note.html', note=note, current_user=username))
        response.set_cookie("can_edit_note", can_edit)

        return response
    else:
        return render_template('errors/404.html')


@view_note_route.route("/note/wall", methods=["GET"])
def note_wall():
    filter_content = request.args.get('filter_content', '')
    notes = load_data(NOTES_FILE)
    jwt_token = request.cookies.get("jwt_token")
    if jwt_token:
        try:
            payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])
            username = payload.get('username')
        except jwt.ExpiredSignatureError:
            username = None
        except jwt.InvalidTokenError:
            username = None
    else:
        username = None

    if filter_content:
        filtered_notes = [note for note in notes.values() if re.search(filter_content, note['content'], re.IGNORECASE)]
    else:
        filtered_notes = [note for note in notes.values() if note['visibility'] == 'public' or
                          note['author'] == username or username == 'admin']

    sorted_notes = sorted(filtered_notes, key=lambda x: x['timestamp'], reverse=True)

    response = make_response(render_template('notes/note_wall.html', notes=sorted_notes, current_user=username))
    response.delete_cookie("can_edit_note")

    return response
