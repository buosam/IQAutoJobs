import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["*"]}})

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')
jwt = JWTManager(app)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import User, Job, Application

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400

    new_user = User(username=username, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route('/profile')
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.query.all()
    return jsonify([{'id': job.id, 'title': job.title, 'company': job.company, 'location': job.location, 'description': job.description, 'applicants': [app.user.username for app in job.applications]} for job in jobs])

@app.route('/jobs', methods=['POST'])
@jwt_required()
def create_job():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    data = request.get_json()
    new_job = Job(
        title=data['title'],
        company=data['company'],
        location=data['location'],
        description=data['description'],
        employer_id=user.id
    )
    db.session.add(new_job)
    db.session.commit()

    return jsonify({'id': new_job.id, 'title': new_job.title, 'company': new_job.company, 'location': new_job.location, 'description': new_job.description}), 201

@app.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = Job.query.get(job_id)
    if job:
        return jsonify({'id': job.id, 'title': job.title, 'company': job.company, 'location': job.location, 'description': job.description})
    return jsonify({'error': 'Job not found'}), 404

@app.route('/jobs/<int:job_id>', methods=['PUT'])
@jwt_required()
def update_job(job_id):
    job = Job.query.get(job_id)
    if job:
        data = request.get_json()
        job.title = data['title']
        job.company = data['company']
        job.location = data['location']
        job.description = data['description']
        db.session.commit()
        return jsonify({'id': job.id, 'title': job.title, 'company': job.company, 'location': job.location, 'description': job.description})
    return jsonify({'error': 'Job not found'}), 404

@app.route('/jobs/<int:job_id>', methods=['DELETE'])
@jwt_required()
def delete_job(job_id):
    job = Job.query.get(job_id)
    if job:
        db.session.delete(job)
        db.session.commit()
        return '', 204
    return jsonify({'error': 'Job not found'}), 404

@app.route('/jobs/<int:job_id>/apply', methods=['POST'])
@jwt_required()
def apply_to_job(job_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    job = Job.query.get(job_id)
    if job:
        application = Application.query.filter_by(user_id=user.id, job_id=job.id).first()
        if not application:
            new_application = Application(user_id=user.id, job_id=job.id)
            db.session.add(new_application)
            db.session.commit()
        return jsonify({'msg': 'Application successful'})
    return jsonify({'error': 'Job not found'}), 404

@app.get("/health")
def health():
    return jsonify(ok=True), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
