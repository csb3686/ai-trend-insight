import os
import pymysql
from datetime import datetime
from dotenv import load_dotenv

# 루트 디렉토리의 .env 로드
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..', '.env')
load_dotenv(dotenv_path=env_path)

class TrendsAggregator:
    def __init__(self):
        self.db_host = os.getenv('MYSQL_HOST', 'localhost')
        self.db_port = int(os.getenv('MYSQL_PORT', 3306))
        self.db_user = os.getenv('MYSQL_USER', 'root')
        self.db_password = os.getenv('MYSQL_PASSWORD', 'root')
        self.db_name = os.getenv('MYSQL_DATABASE', 'ai_trend')

    def get_connection(self):
        return pymysql.connect(
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_password,
            database=self.db_name,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def aggregate_all(self):
        """저장된 모든 데이터를 바탕으로 전체 기간 통계 재산출"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                # 1. 데이터가 존재하는 모든 연/월 쌍 가져오기
                cursor.execute("""
                    SELECT DISTINCT YEAR(published_at) as year, MONTH(published_at) as month 
                    FROM articles 
                    WHERE published_at IS NOT NULL
                    ORDER BY year, month
                """)
                periods = cursor.fetchall()
                
                print(f"[Aggregator] 총 {len(periods)}개 기간의 통계를 산출합니다.")

                for period in periods:
                    y, m = period['year'], period['month']
                    self.aggregate_for_period(cursor, y, m)
                    
            print("[Aggregator] 전체 통계 집계 작업이 완료되었습니다.")
        finally:
            conn.close()

    def aggregate_for_period(self, cursor, year, month):
        """특정 연/월에 대한 기술별 통계 및 순위 산출"""
        print(f" -> {year}년 {month}월 통계 집계 중...")

        # 1. 해당 월의 기술별 총 언급 수 및 기사 수 집계
        sql_summary = """
            SELECT 
                at.tech_id,
                SUM(at.mention_count) as total_mentions,
                COUNT(DISTINCT at.article_id) as article_count
            FROM article_technologies at
            JOIN articles a ON at.article_id = a.id
            WHERE YEAR(a.published_at) = %s AND MONTH(a.published_at) = %s
            GROUP BY at.tech_id
            ORDER BY total_mentions DESC
        """
        cursor.execute(sql_summary, (year, month))
        tech_stats = cursor.fetchall()

        # 2. 전월 데이터 조회 (변화율 및 이전 순위 계산용)
        # 전월 계산 로직
        p_year = year if month > 1 else year - 1
        p_month = month - 1 if month > 1 else 12
        
        cursor.execute("""
            SELECT tech_id, mention_count, rank_current 
            FROM trends 
            WHERE year = %s AND month = %s
        """, (p_year, p_month))
        prev_month_data = {row['tech_id']: row for row in cursor.fetchall()}

        # 3. 데이터 업데이트/삽입 (Upsert)
        for index, stat in enumerate(tech_stats):
            tech_id = stat['tech_id']
            mentions = stat['total_mentions']
            articles = stat['article_count']
            rank_current = index + 1 # 1등부터 시작
            
            p_data = prev_month_data.get(tech_id)
            p_count = p_data['mention_count'] if p_data else 0
            p_rank = p_data['rank_current'] if p_data else None
            
            # 변화율 계산: ((이번달 - 지난달) / 지난달) * 100
            change_rate = 0
            if p_count > 0:
                change_rate = ((mentions - p_count) / p_count) * 100
            
            sql_upsert = """
                INSERT INTO trends 
                (tech_id, year, month, mention_count, article_count, prev_month_count, change_rate, rank_current, rank_prev)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    mention_count = VALUES(mention_count),
                    article_count = VALUES(article_count),
                    prev_month_count = VALUES(prev_month_count),
                    change_rate = VALUES(change_rate),
                    rank_current = VALUES(rank_current),
                    rank_prev = VALUES(rank_prev)
            """
            cursor.execute(sql_upsert, (
                tech_id, year, month, mentions, articles, p_count, change_rate, rank_current, p_rank
            ))

if __name__ == "__main__":
    aggregator = TrendsAggregator()
    aggregator.aggregate_all()
