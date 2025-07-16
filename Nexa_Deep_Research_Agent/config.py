import os
from dotenv import load_dotenv

load_dotenv()

# Redis configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Helix DB configuration
HELIX_DB_URL = os.getenv("HELIX_DB_URL", "http://localhost:6333")
