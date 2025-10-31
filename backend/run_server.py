
import os
import uvicorn
from dotenv import load_dotenv

if __name__ == "__main__":
    # Construct the path to the .env file in the parent directory
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')

    # Load the environment variables from the .env file
    load_dotenv(dotenv_path)

    # Start the uvicorn server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        app_dir="."
    )
