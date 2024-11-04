from flask import Blueprint, request, render_template, redirect, url_for, make_response
from .create_note import verify_jwt_cookie
from app.database.models import db, Note

edit_note_route = Blueprint("edit_note_route", __name__)


@edit_note_route.route('/note/edit/<note_id>', methods=["GET", "POST"])
def edit_note(note_id):
    username = verify_jwt_cookie()
    can_edit = request.cookies.get("can_edit_note")

    if not username:
        return redirect(url_for('auth_route.register'))

    note = Note.query.filter_by(id=note_id).first()

    if not note:
        return render_template('errors/404.html')

    if can_edit == "0":
        return render_template('errors/403.html')

    if request.method == "POST":
        note.title = request.form.get('title')
        note.content = request.form.get('content')
        note.visibility = request.form.get('visib', 'public')

        db.session.commit()

        return redirect(url_for("view_note_route.view_note", note_id=note_id))

    response = make_response(render_template("notes/edit_note.html", note=note, current_user=username))
    response.delete_cookie("can_edit_note")

    return response
