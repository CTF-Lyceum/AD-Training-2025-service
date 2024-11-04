from datetime import datetime
from flask import Blueprint, request, render_template, redirect, url_for
import jwt
from config import SECRET_KEY
from app.database.models import Note, db, User

create_note_route = Blueprint("create_note_route", __name__)


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


@create_note_route.route('/create_note', methods=["GET", 'POST'])
def create_note():
    if request.method == "POST":
        username = verify_jwt_cookie()
        if not username:
            return redirect(url_for('auth_route.login'))

        title = request.form.get('title')
        content = request.form.get('content')
        visibility = request.form.get('visibility', 'private')

        user = User.query.filter_by(username=username).first()
        if not user:
            return redirect(url_for('auth_route.login'))

        new_note = Note(
            creator_id=user.id,
            creator_username=username,
            datetime=datetime.utcnow(),
            visibility="public",
            title=title,
            content=content
        )

        db.session.add(new_note)
        db.session.commit()

        return redirect(url_for("view_note_route.view_note", note_id=new_note.id))

    username = verify_jwt_cookie()
    if not username:
        return redirect(url_for('auth_route.login'))

    return render_template("notes/create_note.html", current_user=username)
