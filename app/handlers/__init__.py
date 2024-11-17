from .create_note import create_note_route
from .login import auth_route
from .note import view_note_route
from .edit_note import edit_note_route
from .users import users_route


routes = [
    create_note_route,
    auth_route,
    view_note_route,
    edit_note_route,
    users_route
]