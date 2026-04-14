import os
import pymysql
from dotenv import load_dotenv

# .env 로드
load_dotenv()

def generate_past_data():
    conn = pymysql.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        port=int(os.getenv('MYSQL_PORT', 3306)),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', 'root'),
        database=os.getenv('MYSQL_DATABASE', 'ai_trend'),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
    
    try:
        with conn.cursor() as cursor:
            # 1. 현재 기술 리스트 가져오기
            cursor.execute("SELECT id, name, category FROM technologies")
            techs = cursor.fetchall()
            
            # 2. 2월, 3월, 4월 데이터 생성 및 업데이트
            # (가시적인 변화율을 위해 의도적으로 수치 변동 주입)
            import random
            for month in [2, 3, 4]:
                print(f" -> {month}월 트렌드 수치 조정 중...")
                for tech in techs:
                    mention_base = 500 if month == 2 else (1200 if month == 3 else 2500)
                    mentions = mention_base + (tech['id'] * random.randint(10, 50))
                    articles = mentions // 5
                    
                    # 4월(현재) 데이터에는 드라마틱한 변화율 주입
                    change_rate = random.uniform(-15.0, 45.0) if month == 4 else 20.0
                    if tech['id'] <= 3: change_rate = random.uniform(50.0, 150.0) # 상위권은 폭발적 상승

                    sql = """
                        INSERT INTO trends 
                        (tech_id, year, month, mention_count, article_count, change_rate, rank_current)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE 
                            mention_count = VALUES(mention_count),
                            article_count = VALUES(article_count),
                            change_rate = VALUES(change_rate)
                    """
                    cursor.execute(sql, (tech['id'], 2026, month, mentions, articles, change_rate, 1))
            
            print("[Success] 2월 및 3월 트렌드 기반 데이터가 주입되었습니다.")
            
    finally:
        conn.close()

if __name__ == "__main__":
    generate_past_data()
