import os
from dotenv import load_dotenv

load_dotenv()

print("Environment Variables Check:")
print(f"DATABASE_URL: {os.environ.get('DATABASE_URL', 'NOT SET')}")
print(f"JWT_SECRET: {os.environ.get('JWT_SECRET', 'NOT SET')}")
print(f"R2_ENDPOINT: {os.environ.get('R2_ENDPOINT', 'NOT SET')}")
print(f"R2_ACCESS_KEY_ID: {os.environ.get('R2_ACCESS_KEY_ID', 'NOT SET')}")
print(f"R2_BUCKET_NAME: {os.environ.get('R2_BUCKET_NAME', 'NOT SET')}")

print("\nTesting app creation...")
try:
    from backend.app import create_app
    app = create_app()
    print("✓ App created successfully")
    print(f"✓ Database URI configured: {bool(app.config.get('SQLALCHEMY_DATABASE_URI'))}")
    print(f"✓ JWT Secret configured: {bool(app.config.get('JWT_SECRET_KEY'))}")
except Exception as e:
    print(f"✗ Error creating app: {e}")
    import traceback
    traceback.print_exc()
