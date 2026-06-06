from dotenv import load_dotenv
import os

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")

if not NASA_API_KEY:
    raise ValueError("NASA_API_KEY environment variable not set")