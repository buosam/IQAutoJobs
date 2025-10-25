import os
import logging
from flask import Flask, send_from_directory, jsonify, abort
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException, SecurityError
from werkzeug.utils import safe_join

from extensions import db, migrate, jwt
import routes

logging.basicConfig(level=logging.INFO)

def create_app(config_overrides=None):
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        logging.info(f"Loading .env file from {dotenv_path}")
        load_dotenv(dotenv_path)

    static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'frontend', 'build'))

    app = Flask(__name__, static_folder=static_folder, static_url_path='/')
    CORS(app, resources={r"/*": {"origins": ["*"]}})

    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///:memory:')
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
    app.register_blueprint(routes.bp, url_prefix='/api')
    logging.info("Blueprints registered.")

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return e
        logging.error(f"Unhandled exception: {e}", exc_info=True)
        return jsonify(error="An unexpected error occurred"), 500

    return app

app = create_app()
