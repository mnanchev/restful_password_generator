import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_FILE_FOLDER = os.path.join(ROOT_DIR, "mock_objects")
NOT_AVAILABLE = "Provider is not available at the moment.\n Please try again later"
REQUIRED_KEYS = ["secret", "password", "is_password_protected", "creator_id"]
NOT_EXISTING = "Secret does not exist"
