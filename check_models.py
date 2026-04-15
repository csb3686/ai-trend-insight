import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("Error: GEMINI_API_KEY not found in .env")
else:
    # v1beta에서 가용한 모델 전체 리스트 조회
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print("\n=== [사용 가능한 구글 AI 모델 목록] ===")
            for m in models:
                if 'embedding' in m['name'] or 'flash' in m['name']:
                    print(f"- {m['name']} (지원 기능: {m.get('supportedGenerationMethods')})")
            print("========================================\n")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Exception: {e}")
