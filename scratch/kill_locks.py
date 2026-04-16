import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def kill_hanging_processes():
    print("🧹 데이터베이스 교착 상태 정리 시작...")
    try:
        conn = pymysql.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', 'adminuser'),
            database=os.getenv('MYSQL_DATABASE', 'ai_trend'),
            connect_timeout=5
        )
        
        with conn.cursor() as cursor:
            # 현재 실행 중인 프로세스 목록 조회
            cursor.execute("SHOW PROCESSLIST")
            processes = cursor.fetchall()
            
            killed_count = 0
            for proc in processes:
                proc_id = proc[0]
                user = proc[1]
                time = proc[5]
                state = proc[6]
                info = proc[7]
                
                # 30초 이상 실행 중인 쿼리 혹은 Sleep 상태인 연결 정리 (필요 시 기준 조정)
                if time > 30 and user != 'event_scheduler':
                    print(f"🧨 종료 중: ID {proc_id} | 시간 {time}s | 상태 {state}")
                    cursor.execute(f"KILL {proc_id}")
                    killed_count += 1
            
            print(f"✅ 총 {killed_count}개의 정체된 프로세스를 정리했습니다.")
            
        conn.close()
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    kill_hanging_processes()
