import os
import pymysql
from dotenv import load_dotenv

def check_schema():
    load_dotenv()
    conn = pymysql.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        port=int(os.getenv('MYSQL_PORT', 3306)),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', 'root'),
        database=os.getenv('MYSQL_DATABASE', 'ai_trend'),
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute("DESCRIBE articles")
            columns = cursor.fetchall()
            print("--- Articles Table Schema ---")
            for col in columns:
                print(f"Column: {col['Field']}, Type: {col['Type']}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_schema()
