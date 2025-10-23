from flask import Blueprint, jsonify, request
from .models import User, Job, Application, UserProfile, CompanyProfile
from .extensions import db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import time
from .s3 import upload_to_s3

bp = Blueprint('routes', __name__)

# In-memory data stores
user_profiles = {}
company_profiles = {}

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user_type = request.json.get('user_type', 'job_seeker')
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400

    new_user = User(username=username, password=generate_password_hash(password), user_type=user_type)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201

@bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@bp.route('/profile', methods=['GET', 'POST', 'PUT'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if request.method == 'GET':
        if user.user_type == 'job_seeker':
            profile = user_profiles.get(user.id)
            if profile:
                return jsonify(profile)
            return jsonify({'msg': 'Profile not found'}), 404
        else:
            profile = company_profiles.get(user.id)
            if profile:
                return jsonify(profile)
            return jsonify({'msg': 'Profile not found'}), 404

    if request.method == 'POST' or request.method == 'PUT':
        data = request.get_json()
        if user.user_type == 'job_seeker':
            user_profiles[user.id] = data
            return jsonify(data)
        else:
            company_profiles[user.id] = data
            return jsonify(data)

@bp.route('/upload/resume', methods=['POST'])
@jwt_required()
def upload_resume():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if 'file' not in request.files:
        return jsonify({'msg': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'msg': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{user.id}_{file.filename}")
        bucket_name = os.environ.get('R2_BUCKET_NAME')

        file_url = upload_to_s3(file, bucket_name, filename)

        if file_url:
            profile = user_profiles.get(user.id, {})
            profile['resume'] = file_url
            user_profiles[user.id] = profile
            return jsonify({'msg': 'File uploaded successfully', 'file_url': file_url})
        else:
            return jsonify({'msg': 'File upload failed'}), 500

    return jsonify({'msg': 'File type not allowed'}), 400

@bp.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.query.all()
    return jsonify([{'id': job.id, 'title': job.title, 'company': job.company, 'location': job.location, 'description': job.description, 'applicants': [app.user.username for app in job.applications]} for job in jobs])

@bp.route('/jobs', methods=['POST'])
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

@bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = Job.query.get(job_id)
    if job:
        return jsonify({'id': job.id, 'title': job.title, 'company': job.company, 'location': job.location, 'description': job.description})
    return jsonify({'error': 'Job not found'}), 404

@bp.route('/jobs/<int:job_id>', methods=['PUT'])
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

@bp.route('/jobs/<int:job_id>', methods=['DELETE'])
@jwt_required()
def delete_job(job_id):
    job = Job.query.get(job_id)
    if job:
        db.session.delete(job)
        db.session.commit()
        return '', 204
    return jsonify({'error': 'Job not found'}), 404

@bp.route('/jobs/<int:job_id>/apply', methods=['POST'])
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

import psutil
from datetime import datetime

@bp.route('/healthz', methods=['GET'])
def healthz():
    return jsonify(status="OK"), 200

@bp.route('/readyz', methods=['GET'])
def readyz():
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        db_status = 'connected'
    except Exception as e:
        db_status = f'disconnected: {e}'

    # System metrics
    p = psutil.Process(os.getpid())
    uptime_seconds = time.time() - p.create_time()
    memory_usage = psutil.virtual_memory()._asdict()

    response = {
        'status': 'OK',
        'timestamp': datetime.utcnow().isoformat(),
        'database': db_status,
        'memory': memory_usage,
        'uptime': uptime_seconds
    }

    return jsonify(response), 200
