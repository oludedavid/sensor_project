import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
load_dotenv()

while True:
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DATABASE_HOST"),
            database="social_media",
            user=os.environ.get("DATABASE_USER"),
            password=os.environ.get("DATABASE_PASSWORD"),
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("✅ Database connection successful!")
        break
    except Exception as error:
        print("❌ Failed to connect to DB:", error)
        time.sleep(3)
