import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["*"]}})

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')
jwt = JWTManager(app)

# In-memory user store
users = {}
user_id_counter = 1

jobs = [
    {
        'id': 1,
        'title': 'Software Engineer',
        'company': 'Google',
        'location': 'Mountain View, CA',
        'description': 'We are looking for a talented Software Engineer to join our team.',
        'applicants': [],
    },
    {
        'id': 2,
        'title': 'Product Manager',
        'company': 'Facebook',
        'location': 'Menlo Park, CA',
        'description': 'We are looking for a talented Product Manager to join our team.',
        'applicants': [],
    },
    {
        'id': 3,
        'title': 'Data Scientist',
        'company': 'Amazon',
        'location': 'Seattle, WA',
        'description': 'We are looking for a talented Data Scientist to join our team.',
        'applicants': [],
    },
]

@app.route('/register', methods=['POST'])
def register():
    global user_id_counter
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400
    if username in [user['username'] for user in users.values()]:
        return jsonify({"msg": "Username already exists"}), 400

    users[user_id_counter] = {'username': username, 'password': generate_password_hash(password)}
    user_id_counter += 1

    return jsonify({"msg": "User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = next((user for user in users.values() if user['username'] == username), None)

    if not user or not check_password_hash(user['password'], password):
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
    return jsonify(jobs)

@app.route('/jobs', methods=['POST'])
@jwt_required()
def create_job():
    job = request.get_json()
    job['applicants'] = []
    jobs.append(job)
    return jsonify(job), 201

@app.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = next((job for job in jobs if job['id'] == job_id), None)
    if job:
        return jsonify(job)
    return jsonify({'error': 'Job not found'}), 404

@app.route('/jobs/<int:job_id>', methods=['PUT'])
@jwt_required()
def update_job(job_id):
    job = next((job for job in jobs if job['id'] == job_id), None)
    if job:
        data = request.get_json()
        job.update(data)
        return jsonify(job)
    return jsonify({'error': 'Job not found'}), 404

@app.route('/jobs/<int:job_id>', methods=['DELETE'])
@jwt_required()
def delete_job(job_id):
    global jobs
    jobs = [job for job in jobs if job['id'] != job_id]
    return '', 204

@app.route('/jobs/<int:job_id>/apply', methods=['POST'])
@jwt_required()
def apply_to_job(job_id):
    job = next((job for job in jobs if job['id'] == job_id), None)
    if job:
        current_user = get_jwt_identity()
        if current_user not in job['applicants']:
            job['applicants'].append(current_user)
        return jsonify(job)
    return jsonify({'error': 'Job not found'}), 404

@app.get("/health")
def health():
    return jsonify(ok=True), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
