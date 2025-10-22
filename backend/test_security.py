import os
import sys
import unittest

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app

class SecurityTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            "TESTING": True,
            "SECRET_KEY": "test",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
        })
        self.client = self.app.test_client()

        # Create a dummy file outside the static folder
        self.dummy_file_path = os.path.join(self.app.root_path, '..', 'dummy.txt')
        with open(self.dummy_file_path, 'w') as f:
            f.write('secret')

    def tearDown(self):
        os.remove(self.dummy_file_path)

    def test_path_traversal(self):
        # Attempt to access the dummy file using path traversal
        response = self.client.get('/../../dummy.txt')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
