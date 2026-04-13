import re
import json
import pymysql
import os
from dotenv import load_dotenv

# 로컬 DB 설정을 위해 .env 로드
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..', '.env')
load_dotenv(dotenv_path=env_path)

class KeywordExtractor:
    def __init__(self, db_conn=None):
        self.db_conn = db_conn
        self.tech_patterns = [] # (tech_id, tech_name, regex_pattern)
        self._load_technologies()

    def _load_technologies(self):
        """DB에서 기술 마스터 데이터를 읽어와서 정규표현식 패턴 생성"""
        should_close = False
        if not self.db_conn:
            self.db_conn = pymysql.connect(
                host=os.getenv('MYSQL_HOST', 'localhost'),
                port=int(os.getenv('MYSQL_PORT', 3306)),
                user=os.getenv('MYSQL_USER', 'root'),
                password=os.getenv('MYSQL_PASSWORD', 'root'),
                database=os.getenv('MYSQL_DATABASE', 'ai_trend'),
                cursorclass=pymysql.cursors.DictCursor
            )
            should_close = True

        try:
            with self.db_conn.cursor() as cursor:
                cursor.execute("SELECT id, name, aliases FROM technologies WHERE is_active = 1")
                techs = cursor.fetchall()
                
                for tech in techs:
                    tech_id = tech['id']
                    tech_name = tech['name']
                    # aliases는 JSON 문자열일 수 있으므로 파싱
                    aliases = tech['aliases']
                    if isinstance(aliases, str):
                        aliases = json.loads(aliases)
                    elif not aliases:
                        aliases = []
                    
                    # 모든 별칭과 원본 이름을 합쳐서 하나의 정규식 패턴 생성
                    all_names = [tech_name] + aliases
                    # 특수문자(C++, .NET 등)를 안전하게 처리하기 위해 re.escape 사용
                    escaped_names = [re.escape(name) for name in all_names]
                    
                    # 단어 경계 처리를 위해 Negative Look-behind/Look-ahead 사용 (고정 길이 에러 방지)
                    # (?<![a-zA-Z0-9]) : 앞에 영문/숫자가 없을 것 (시작점 포함)
                    # (?![a-zA-Z0-9]) : 뒤에 영문/숫자가 없을 것 (끝점 포함)
                    pattern_str = r'(?i)(?<![a-zA-Z0-9])(' + '|'.join(escaped_names) + r')(?![a-zA-Z0-9])'
                    
                    # Go, R, C 같이 너무 짧은 언어는 별도 처리 (대소문자 구분 권장하나 여기서는 패턴으로 보편화)
                    if len(tech_name) <= 2:
                        # 짧은 단어는 조금 더 엄격하게 (대문자 시작 등 고려 가능하지만 일단 유지)
                        pass
                        
                    self.tech_patterns.append({
                        'id': tech_id,
                        'name': tech_name,
                        'pattern': re.compile(pattern_str)
                    })
        finally:
            if should_close:
                self.db_conn.close()
                self.db_conn = None

    def extract_keywords(self, text: str):
        """텍스트에서 언급된 기술 키워드와 횟수 추출"""
        results = {}
        
        if not text:
            return results

        for item in self.tech_patterns:
            tech_id = item['id']
            # 본문에서 해당 패턴이 몇 번 나타나는지 찾기
            matches = item['pattern'].findall(text)
            if matches:
                results[tech_id] = {
                    'name': item['name'],
                    'mention_count': len(matches)
                }
        
        return results

if __name__ == "__main__":
    # 테스트용 코드
    extractor = KeywordExtractor()
    test_text = "I love Python and React. Next.js is also great with TypeScript and C++."
    found = extractor.extract_keywords(test_text)
    print("추출된 기술 키워드:", found)
