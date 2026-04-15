import os
import re
import json
import requests
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

class AIAnalyst:
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        
        # 1단계: Heuristic Noise Keywords
        self.noise_keywords = [
            'awesome-', 'interview', 'roadmap', 'list', 'free-books', 
            'collection', 'resources', 'guide', 'tutorial', 'course',
            'cheat-sheet', 'curated', 'handbook', 'top-10', 'best-of'
        ]

    def is_obvious_noise(self, title, description):
        """1단계: 코드 기반 휴리스틱 필터링 (비용 0원)"""
        text = f"{title} {description}".lower()
        for kw in self.noise_keywords:
            if kw in text:
                return True
        return False

    def analyze_potential_tech(self, title, description, content):
        """2-3단계: AI 기반 정밀 분석 (Gemini 1.5 Flash 활용)"""
        if not self.gemini_api_key:
            print("[AI Analyst] Gemini API Key가 없어 분석을 건너뜁니다.")
            return None

        # 프롬프트 설계: 토큰 절약을 위해 아주 짧은 응답(JSON) 요구
        prompt = f"""
        Analyze the following GitHub repository information. 
        Determine if this is a 'Software Technology' (Library, Framework, Tool, Language) 
        OR 'Content/Noise' (Book, Tutorial, Interview Prep, Awesome list, generic collection).

        Respond ONLY in JSON format like this:
        {{
          "is_tech": true/false,
          "tech_name": "Name of the tech if new, else null",
          "category": "One of: Language, Framework, AI_ML, DevOps, Database, Cloud, Other",
          "reason": "1-sentence reason"
        }}

        Title: {title}
        Description: {description}
        Snippet: {content[:500]}
        """

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.gemini_api_key}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            if response.status_code != 200:
                print(f"[AI Analyst Debug] Error Body: {response.text}")
            response.raise_for_status()
            res_json = response.json()
            
            # AI 응답 텍스트 추출 및 정제 (JSON 부분만)
            ai_text = res_json['candidates'][0]['content']['parts'][0]['text']
            # ```json ... ``` 형태 제거
            clean_json = re.sub(r'```json\s*|\s*```', '', ai_text).strip()
            
            return json.loads(clean_json)
        except Exception as e:
            print(f"[AI Analyst Error] {e}")
            return None

if __name__ == "__main__":
    # 테스트용 코드
    analyst = AIAnalyst()
    test_repo = {
        "title": "GitHub Trending: mojo-lang/mojo",
        "description": "The Mojo Programming Language",
        "content": "Mojo is a new programming language that bridges the gap between research and production by combining the best of Python syntax with systems programming and metaprogramming."
    }
    
    print("--- 1단계 테스트 (Heuristic) ---")
    print(f"Is Noise? {analyst.is_obvious_noise(test_repo['title'], test_repo['description'])}")
    
    print("\n--- 3단계 테스트 (AI Analysis) ---")
    result = analyst.analyze_potential_tech(test_repo['title'], test_repo['description'], test_repo['content'])
    print(json.dumps(result, indent=2, ensure_ascii=False))
