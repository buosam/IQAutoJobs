import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from .extensions import db, migrate, jwt
from . import routes

def create_app():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        print(f"Loading .env file from {dotenv_path}")
        load_dotenv(dotenv_path)

    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": ["*"]}})

    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Setup the Flask-JWT-Extended extension
    app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET')

    # Register extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(routes.bp)

    return app
