import os
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = conn.cursor()

cursor.execute("""
    INSERT INTO usage_log (user_id, model_name, input_tokens, output_tokens, timestamp)
    VALUES (%s, %s, %s, %s, %s)
""", ("test_user", "test_model", 10, 15, datetime.utcnow()))

conn.commit()

cursor.close()
conn.close()

print("DB insert test successful!")
