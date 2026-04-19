import os
import random
import pymysql
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

class HybridDataGenerator:
    def __init__(self):
        self.db_host = os.getenv('MYSQL_HOST', 'localhost')
        self.db_port = int(os.getenv('MYSQL_PORT', 3306))
        self.db_user = os.getenv('MYSQL_USER', 'root')
        self.db_password = os.getenv('MYSQL_PASSWORD', 'root')
        self.db_name = os.getenv('MYSQL_DATABASE', 'ai_trend')
        
        # 주요 기술 ID 맵핑
        self.tech_pool = {
            "Language": [1, 2, 3, 4, 5, 6, 7],
            "Framework": [8, 9, 10, 11, 12, 13],
            "AI_ML": [14, 15, 16, 17],
            "DevOps": [18, 19, 26, 27],
            "Database": [20, 21, 22, 23],
            "Cloud": [24, 25]
        }
        
        # 그럴듯한 뉴스 제목 템플릿
        self.templates = [
            "{tech}의 새로운 혁신: {feature} 공개",
            "{tech} {version} 업데이트가 가져온 변화",
            "왜 개발자들은 {tech}에 열광하는가?",
            "{tech} 생태계의 급격한 성장과 미래",
            "{tech}를 활용한 효율적인 {field} 구축 방법",
            "실무에서 바로 쓰는 {tech} 가이드",
            "{tech} vs 경쟁 기술: 심층 비교 분석",
            "{tech} 커뮤니티에서 가장 많이 묻는 질문 TOP 10"
        ]
        
        self.features = ["성능 향상", "보안 강화", "AI 기반 최적화", "사용자 경험 개선", "생산성 극대화"]
        self.fields = ["데이터 파이프라인", "마이크로서비스 아키텍처", "클라우드 인프라", "실시간 분석 시스템"]

    def get_connection(self):
        return pymysql.connect(
            host=self.db_host, port=self.db_port, user=self.db_user,
            password=self.db_password, database=self.db_name,
            autocommit=True, cursorclass=pymysql.cursors.DictCursor
        )

    def generate_random_date(self, month):
        year = 2026
        if month == 2:
            day = random.randint(1, 28)
        elif month == 4:
            day = random.randint(1, 14) # 4월은 현재 날짜까지
        else:
            day = random.randint(1, 31)
        return datetime(year, month, day, random.randint(0, 23), random.randint(0, 59))

    def run(self):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                # 1. 기존 더미 데이터 정리 (필요 시)
                print("[Hybrid] 기존 하이브리드 데이터 정리 중...")
                cursor.execute("DELETE FROM articles WHERE url LIKE '%hybrid-media%'")
                cursor.execute("DELETE FROM trends WHERE year = 2026 AND month IN (2, 3, 4)")
                
                print("[Hybrid] 300개의 기사 생성을 시작합니다 (2월~4월)...")
                
                articles_per_month = {2: 100, 3: 100, 4: 100}
                total_inserted = 0
                
                for month, count in articles_per_month.items():
                    print(f" -> {month}월분 데이터 주입 중...")
                    for i in range(count):
                        # 기술 선택 (특정 달에 특정 기술 비중 높이기)
                        if month == 4:
                            # 4월에는 Python, Gemini, LangChain 비중 대폭 상승 (트렌드 극대화)
                            tech_id = random.choice([1, 1, 16, 16, 16, 14, 14] + list(range(1, 28)))
                        else:
                            tech_id = random.randint(1, 27)
                            
                        # 기술명 조회 (더미 제목용)
                        cursor.execute("SELECT name FROM technologies WHERE id = %s", (tech_id,))
                        tech_name = cursor.fetchone()['name']
                        
                        # 뉴스 소식 생성 (제목 및 다이나믹 링크)
                        title = random.choice(self.templates).format(
                            tech=tech_name, 
                            feature=random.choice(self.features),
                            version=f"v{random.randint(2, 5)}",
                            field=random.choice(self.fields)
                        )
                        search_keyword = tech_name.replace(' ', '+')
                        url = f"https://www.google.com/search?q={search_keyword}+tech+news&tbm=nws&v={month}-{i}"
                        
                        pub_date = self.generate_random_date(month)
                        
                        # Article 저장 (Source 2: GeekNews 고정)
                        cursor.execute("""
                            INSERT IGNORE INTO articles (title, url, content, published_at, source_id)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (title, url, f"{tech_name}에 관한 심층 테크 리포트입니다.", pub_date, 2))
                        
                        article_id = cursor.lastrowid
                        
                        # 만약 중복 데이터라 INSERT 되지 않았다면 기존 ID 조회
                        if article_id == 0:
                            cursor.execute("SELECT id FROM articles WHERE url = %s", (url,))
                            article_id = cursor.fetchone()['id']
                        
                        # Article-Tech 연결 (중복 방지 IGNORE 추가)
                        cursor.execute("""
                            INSERT IGNORE INTO article_technologies (article_id, tech_id, mention_count)
                            VALUES (%s, %s, %s)
                        """, (article_id, tech_id, random.randint(1, 5)))
                        
                        total_inserted += 1
                
                print(f"[Hybrid] 총 {total_inserted}개의 기사 주입 완료.")
                
        finally:
            conn.close()

if __name__ == "__main__":
    generator = HybridDataGenerator()
    generator.run()
