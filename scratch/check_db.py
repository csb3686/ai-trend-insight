import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def check_db():
    try:
        conn = pymysql.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            port=int(os.getenv("MYSQL_PORT", 3306))
        )
        cursor = conn.cursor()
        
        cursor.execute("SELECT type, COUNT(*) FROM articles GROUP BY type")
        results = cursor.fetchall()
        
        print("Article counts by type:")
        for row in results:
            print(f"- {row[0]}: {row[1]}")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error connecting to DB: {e}")

if __name__ == "__main__":
    check_db()
