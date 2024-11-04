from app.database.models import Note
import jwt
from flask import Blueprint, request, render_template, redirect, url_for, make_response
from config import SECRET_KEY

view_note_route = Blueprint("view_note_route", __name__)


@view_note_route.route("/note/<int:note_id>", methods=["GET"])
def view_note(note_id):
    if 'jwt_token' not in request.cookies:
        return redirect(url_for("auth_route.register"))

    jwt_token = request.cookies.get("jwt_token")
    username = None

    if jwt_token:
        try:
            payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])
            username = payload.get('username')
            if not username:
                return '''401\n Unauthorized'''
        except jwt.ExpiredSignatureError:
            return '''401\nToken expired'''
        except jwt.InvalidTokenError:
            return '''401\n Token is invalid'''

    note = Note.query.filter_by(id=note_id).first()
    if not note:
        return render_template('errors/404.html')

    if note.visibility == "private" and username != note.creator_username and username != "admin":
        return render_template('errors/404.html')

    can_edit = "1" if username == note.creator_username or username == "admin" else "0"

    response = make_response(render_template('notes/view_note.html', note=note, current_user=username))
    response.set_cookie("can_edit_note", can_edit)
    return response

@view_note_route.route("/note/wall", methods=["GET"])
def note_wall():
    filter_content = request.args.get('filter_content', '')
    jwt_token = request.cookies.get("jwt_token")
    username = None

    if jwt_token:
        try:
            payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])
            username = payload.get('username')
        except jwt.ExpiredSignatureError:
            username = None
        except jwt.InvalidTokenError:
            username = None

    if filter_content:
        notes = Note.query.filter(Note.content.op('REGEXP')(filter_content)).all()
    else:
        if username == 'admin':
            notes = Note.query.all()
        else:
            notes = Note.query.filter(
                (Note.visibility == 'public') | (Note.creator_username == username)
            ).all()

    sorted_notes = sorted(notes, key=lambda x: x.datetime, reverse=True)

    response = make_response(render_template('notes/note_wall.html', notes=sorted_notes, current_user=username))
    response.delete_cookie("can_edit_note")
    return response
