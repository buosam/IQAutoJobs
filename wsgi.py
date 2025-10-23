import os
import logging
from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

from extensions import db, migrate, jwt
import routes

logging.basicConfig(level=logging.INFO)

def create_app(config_overrides=None):
    # a HACK to make this work with the flattened directory structure
    # that railway seems to be creating
    env_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
    if os.path.exists(env_path):
        logging.info(f"Loading .env file from {env_path}")
        load_dotenv(env_path)

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
        safe_path = secure_filename(path)
        if safe_path != "" and os.path.exists(os.path.join(app.static_folder, safe_path)):
            return send_from_directory(app.static_folder, safe_path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    return app

# This block is now the only place where create_app is called directly
if __name__ == "__main__":
    app = create_app()
    app.run()
