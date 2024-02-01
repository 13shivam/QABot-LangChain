import os

from dotenv import find_dotenv


# Load environment variables based on the chosen environment
environment = os.getenv("ENVIRONMENT", "default")
env_file = f".env.{environment}"
dotenv_path = find_dotenv(env_file)
