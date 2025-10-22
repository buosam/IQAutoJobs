from flask import Blueprint, jsonify, request
from models import User, Job, Application, UserProfile, CompanyProfile
from extensions import db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import boto3
from botocore.client import Config
from botocore.exceptions import NoCredentialsError

bp = Blueprint('routes', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_r2_client():
    return boto3.client(
        service_name='s3',
        endpoint_url=os.environ.get('R2_ENDPOINT_URL'),
        aws_access_key_id=os.environ.get('R2_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('R2_SECRET_ACCESS_KEY'),
        region_name='auto',
        config=Config(signature_version='s3v4')
    )

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
            profile = UserProfile.query.filter_by(user_id=user.id).first()
            if profile:
                return jsonify({
                    'name': profile.name,
                    'headline': profile.headline,
                    'bio': profile.bio,
                    'resume': profile.resume
                })
            return jsonify({'msg': 'Profile not found'}), 404
        else:
            profile = CompanyProfile.query.filter_by(user_id=user.id).first()
            if profile:
                return jsonify({
                    'name': profile.name,
                    'description': profile.description,
                    'website': profile.website,
                    'logo': profile.logo
                })
            return jsonify({'msg': 'Profile not found'}), 404

    if request.method == 'POST' or request.method == 'PUT':
        data = request.get_json()
        if user.user_type == 'job_seeker':
            profile = UserProfile.query.filter_by(user_id=user.id).first()
            if not profile:
                profile = UserProfile(user_id=user.id)
                db.session.add(profile)

            profile.name = data.get('name')
            profile.headline = data.get('headline')
            profile.bio = data.get('bio')
            db.session.commit()
            return jsonify({'msg': 'Profile updated successfully'})
        else:
            profile = CompanyProfile.query.filter_by(user_id=user.id).first()
            if not profile:
                profile = CompanyProfile(user_id=user.id, name=data.get('name'))
                db.session.add(profile)

            profile.name = data.get('name')
            profile.description = data.get('description')
            profile.website = data.get('website')
            profile.logo = data.get('logo')
            db.session.commit()
            return jsonify({'msg': 'Profile updated successfully'})

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
        filename = secure_filename(file.filename)
        r2 = create_r2_client()
        bucket_name = os.environ.get('R2_BUCKET_NAME')

        try:
            r2.upload_fileobj(file, bucket_name, filename)
            resume_url = f"{os.environ.get('R2_PUBLIC_URL')}/{filename}"

            profile = UserProfile.query.filter_by(user_id=user.id).first()
            if not profile:
                profile = UserProfile(user_id=user.id)
                db.session.add(profile)

            profile.resume = resume_url
            db.session.commit()

            return jsonify({'msg': 'File uploaded successfully', 'url': resume_url})
        except NoCredentialsError:
            return jsonify({'msg': 'Credentials not available'}), 500
        except Exception as e:
            return jsonify({'msg': str(e)}), 500

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

@bp.get("/health")
def health():
    return jsonify(ok=True), 200
