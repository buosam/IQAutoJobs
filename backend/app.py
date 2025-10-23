import os
import logging
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException

from backend.extensions import db, migrate, jwt
from backend import routes

logging.basicConfig(level=logging.INFO)

def create_app(config_overrides=None):
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

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if app.static_folder and os.path.exists(app.static_folder):
            safe_path = secure_filename(path)
            if safe_path != "" and os.path.exists(os.path.join(app.static_folder, safe_path)):
                return send_from_directory(app.static_folder, safe_path)
            else:
                index_path = os.path.join(app.static_folder, 'index.html')
                if os.path.exists(index_path):
                    return send_from_directory(app.static_folder, 'index.html')
        return jsonify({"message": "API is running. Frontend not built yet."}), 200

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return e
        logging.error(f"Unhandled exception: {e}", exc_info=True)
        return jsonify(error="An unexpected error occurred"), 500

    return app
