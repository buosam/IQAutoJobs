import os
import sys
import unittest
import json

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.extensions import db
from backend.models import User, Job, Application

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "JWT_SECRET_KEY": "test-secret"
        })
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_user(self):
        response = self.client.post('/register', json={
            "username": "testuser",
            "password": "testpassword",
            "user_type": "job_seeker"
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], "User created successfully")

    def test_register_existing_user(self):
        self.client.post('/register', json={
            "username": "testuser",
            "password": "testpassword",
            "user_type": "job_seeker"
        })
        response = self.client.post('/register', json={
            "username": "testuser",
            "password": "testpassword",
            "user_type": "job_seeker"
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], "Username already exists")

    def test_login_user(self):
        self.client.post('/register', json={
            "username": "testuser",
            "password": "testpassword",
            "user_type": "job_seeker"
        })
        response = self.client.post('/login', json={
            "username": "testuser",
            "password": "testpassword"
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)

    def test_login_invalid_credentials(self):
        self.client.post('/register', json={
            "username": "testuser",
            "password": "testpassword",
            "user_type": "job_seeker"
        })
        response = self.client.post('/login', json={
            "username": "testuser",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], "Bad username or password")

    def test_get_job_seeker_profile(self):
        self.client.post('/register', json={
            "username": "testuser",
            "password": "testpassword",
            "user_type": "job_seeker"
        })
        response = self.client.post('/login', json={
            "username": "testuser",
            "password": "testpassword"
        })
        access_token = json.loads(response.data)['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}

        # Initially, the profile should not be found
        response = self.client.get('/profile', headers=headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], "Profile not found")

        # Create a profile
        profile_data = {"name": "Test User", "headline": "Test Headline"}
        self.client.post('/profile', json=profile_data, headers=headers)

        # Now, the profile should be found
        response = self.client.get('/profile', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "Test User")

    def test_update_job_seeker_profile(self):
        self.client.post('/register', json={
            "username": "testuser",
            "password": "testpassword",
            "user_type": "job_seeker"
        })
        response = self.client.post('/login', json={
            "username": "testuser",
            "password": "testpassword"
        })
        access_token = json.loads(response.data)['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}

        # Create a profile
        profile_data = {"name": "Test User", "headline": "Test Headline"}
        self.client.post('/profile', json=profile_data, headers=headers)

        # Update the profile
        updated_profile_data = {"name": "Updated User", "headline": "Updated Headline"}
        response = self.client.put('/profile', json=updated_profile_data, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "Updated User")

    def _create_user_and_get_token(self, username, password, user_type):
        """Helper function to register a user and return an access token."""
        self.client.post('/register', json={
            "username": username,
            "password": password,
            "user_type": user_type
        })
        response = self.client.post('/login', json={
            "username": username,
            "password": password
        })
        return json.loads(response.data)['access_token']

    def test_create_job(self):
        token = self._create_user_and_get_token("employer", "password", "employer")
        headers = {'Authorization': f'Bearer {token}'}
        job_data = {
            "title": "Software Engineer",
            "company": "Test Inc.",
            "location": "Testville",
            "description": "A test job."
        }
        response = self.client.post('/jobs', json=job_data, headers=headers)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['title'], "Software Engineer")

    def test_get_jobs(self):
        token = self._create_user_and_get_token("employer", "password", "employer")
        headers = {'Authorization': f'Bearer {token}'}
        job_data = {
            "title": "Software Engineer",
            "company": "Test Inc.",
            "location": "Testville",
            "description": "A test job."
        }
        self.client.post('/jobs', json=job_data, headers=headers)
        response = self.client.get('/jobs')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], "Software Engineer")

    def test_apply_to_job(self):
        employer_token = self._create_user_and_get_token("employer", "password", "employer")
        job_seeker_token = self._create_user_and_get_token("jobseeker", "password", "job_seeker")

        headers_employer = {'Authorization': f'Bearer {employer_token}'}
        job_data = {
            "title": "Software Engineer",
            "company": "Test Inc.",
            "location": "Testville",
            "description": "A test job."
        }
        response = self.client.post('/jobs', json=job_data, headers=headers_employer)
        job_id = json.loads(response.data)['id']

        headers_job_seeker = {'Authorization': f'Bearer {job_seeker_token}'}
        response = self.client.post(f'/jobs/{job_id}/apply', headers=headers_job_seeker)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], "Application successful")

        # Verify the application was created in the database
        user = User.query.filter_by(username="jobseeker").first()
        application = Application.query.filter_by(user_id=user.id, job_id=job_id).first()
        self.assertIsNotNone(application)

    def test_healthz(self):
        response = self.client.get('/healthz')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], "OK")

    def test_readyz(self):
        response = self.client.get('/readyz')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], "OK")
        self.assertEqual(data['database'], "connected")

if __name__ == '__main__':
    unittest.main()
