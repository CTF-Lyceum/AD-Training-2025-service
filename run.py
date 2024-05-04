from flask import Flask
from flask_cors import CORS
from app import routes


def create_app():
    app = Flask(__name__, template_folder="app/templates/")
    app.static_folder = "app/static/"
    CORS(app)

    for route in routes:
        app.register_blueprint(route)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000, debug=False)
