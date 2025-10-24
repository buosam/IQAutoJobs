import os
import logging
from flask import Flask, send_from_directory, jsonify, abort
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException, SecurityError
from werkzeug.utils import safe_join

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
        static_root = app.static_folder

        if not static_root or not os.path.isdir(static_root):
            return jsonify({"message": "API is running. Frontend not built yet."}), 200

        if path:
            try:
                candidate = safe_join(static_root, path)
            except (SecurityError, ValueError):
                logging.exception("Security or value error during safe_join for path %s", path)
                abort(404)

            if candidate is None:
                # safe_join returns None when the resolved path would escape static_root
                abort(404)

            if candidate and os.path.isfile(candidate):
                relative_path = os.path.relpath(candidate, static_root)
                return send_from_directory(static_root, relative_path)
        index_path = os.path.join(static_root, 'index.html')
        if os.path.isfile(index_path):
            return send_from_directory(static_root, 'index.html')

        return jsonify({"message": "API is running. Frontend not built yet."}), 200

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return e
        logging.error(f"Unhandled exception: {e}", exc_info=True)
        return jsonify(error="An unexpected error occurred"), 500

    return app
