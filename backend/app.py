import os
import logging
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from extensions import db, migrate, jwt
from . import routes

logging.basicConfig(level=logging.INFO)

def create_app(config_overrides=None):
 
def create_app():
  main
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        logging.info(f"Loading .env file from {dotenv_path}")
        load_dotenv(dotenv_path)

    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": ["*"]}})

    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Setup the Flask-JWT-Extended extension
    app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET')

    if config_overrides:
        app.config.update(config_overrides)

    logging.info(f"DATABASE_URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
    logging.info(f"JWT_SECRET_KEY: {app.config['JWT_SECRET_KEY']}")

    # Register extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    logging.info("Extensions registered.")

    # Register blueprints
    app.register_blueprint(routes.bp)
    logging.info("Blueprints registered.")

    return app
