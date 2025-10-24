import errno
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

        # Ensure a static directory with sample assets exists
        self.static_dir = self.app.static_folder
        os.makedirs(self.static_dir, exist_ok=True)

        self.sample_static_path = os.path.join(self.static_dir, 'app.js')
        with open(self.sample_static_path, 'w') as f:
            f.write('console.log("hello");')

        self.nested_dir = os.path.join(self.static_dir, 'assets')
        os.makedirs(self.nested_dir, exist_ok=True)

        self.nested_static_path = os.path.join(self.nested_dir, 'image.png')
        with open(self.nested_static_path, 'w') as f:
            f.write('fake image data')

    def tearDown(self):
        for path in [
            self.dummy_file_path,
            self.sample_static_path,
            self.nested_static_path,
        ]:
            if os.path.exists(path):
                os.remove(path)

        # Remove the directories created for the static assets if empty
        if os.path.isdir(self.nested_dir):
            try:
                os.rmdir(self.nested_dir)
            except OSError as exc:
                if exc.errno not in {errno.ENOTEMPTY, errno.EEXIST}:
                    raise
            except OSError:
                pass

        if os.path.isdir(self.static_dir):
            try:
                os.rmdir(self.static_dir)
            except OSError as exc:
                if exc.errno not in {errno.ENOTEMPTY, errno.EEXIST}:
                    raise
            except OSError:
                pass

    def test_path_traversal(self):
        # Attempt to access the dummy file using path traversal
        response = self.client.get('/../../dummy.txt')
        self.assertEqual(response.status_code, 404)

    def test_static_file_served(self):
        response = self.client.get('/app.js')
        self.assertEqual(response.status_code, 200)
        self.assertIn('console.log("hello");', response.get_data(as_text=True))

    def test_nested_static_file_served(self):
        response = self.client.get('/assets/image.png')
        self.assertEqual(response.status_code, 200)
        self.assertIn('fake image data', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
