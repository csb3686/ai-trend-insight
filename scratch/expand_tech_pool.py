import os
import pymysql
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

def expand_pool():
    conn = pymysql.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        port=int(os.getenv('MYSQL_PORT', 3306)),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', 'root'),
        database=os.getenv('MYSQL_DATABASE', 'ai_trend'),
        autocommit=True
    )

    new_techs = [
        # Language
        ('Mojo', 'Language', '["mojo-lang"]'),
        ('Zig', 'Language', '[]'),
        ('Elixir', 'Language', '[]'),
        
        # Framework
        ('Svelte', 'Framework', '["SvelteKit"]'),
        ('Bun', 'Framework', '["bun.sh"]'),
        ('Deno', 'Framework', '[]'),
        ('Hono', 'Framework', '[]'),
        ('SolidJS', 'Framework', '[]'),
        
        # AI_ML
        ('HuggingFace', 'AI_ML', '["hf.co", "transformers"]'),
        ('Autogen', 'AI_ML', '[]'),
        ('CrewAI', 'AI_ML', '[]'),
        ('Ollama', 'AI_ML', '[]'),
        ('vLLM', 'AI_ML', '[]'),
        ('Groq', 'AI_ML', '[]'),
        
        # DevOps / Infra
        ('Supabase', 'Cloud', '[]'),
        ('Vercel', 'Cloud', '[]'),
        ('Pulumi', 'DevOps', '[]'),
        
        # Database
        ('SurrealDB', 'Database', '[]'),
        ('TiDB', 'Database', '[]'),
        ('Dragonfly', 'Database', '[]')
    ]

    try:
        with conn.cursor() as cursor:
            print("기술 풀 확장 작업을 시작합니다...")
            inserted_count = 0
            for name, category, aliases in new_techs:
                # 이미 존재하는지 확인
                cursor.execute("SELECT id FROM technologies WHERE name = %s", (name,))
                if cursor.fetchone():
                    # print(f" - {name}: 이미 존재함 필드 패스")
                    continue
                
                # 신규 삽입
                sql = "INSERT INTO technologies (name, category, aliases, is_active) VALUES (%s, %s, %s, 1)"
                cursor.execute(sql, (name, category, aliases))
                inserted_count += 1
                print(f" + {name} ({category}) 추가 완료")
            
            print(f"\n총 {inserted_count}개의 새로운 기술이 정예 멤버로 소집되었습니다! 🚀")
            
    finally:
        conn.close()

if __name__ == "__main__":
    expand_pool()
