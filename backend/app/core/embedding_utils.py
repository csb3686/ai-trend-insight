import os
import requests
from typing import List
from dotenv import load_dotenv

load_dotenv()

class GoogleDirectEmbeddings:
    """
    Google AI v1 REST API를 직접 호출하는 커스텀 임베딩 클래스.
    LangChain의 Embeddings 인터페이스를 준수하여 ChromaDB와 호환됩니다.
    """
    def __init__(self, model="gemini-embedding-001", api_key=None):
        self.model = model
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:embedContent?key={self.api_key}"

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """여러 문서들을 임베딩합니다."""
        embeddings = []
        for text in texts:
            embeddings.append(self.embed_query(text))
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        """단일 쿼리(질문)를 임베딩합니다."""
        payload = {
            "model": f"models/{self.model}",
            "content": {
                "parts": [{"text": text}]
            }
        }
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=15)
            if response.status_code != 200:
                print(f"[Google AI Debug] Error Body: {response.text}")
            response.raise_for_status()
            result = response.json()
            return result['embedding']['values']
        except Exception as e:
            print(f"[GoogleDirectEmbeddings Error] {e}")
            raise e
