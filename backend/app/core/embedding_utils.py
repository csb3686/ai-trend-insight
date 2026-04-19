import os
import requests
import time
from typing import List
from dotenv import load_dotenv

load_dotenv()

class LocalEmbeddings:
    """
    로컬 SentenceTransformer 모델을 사용하는 임베딩 클래스.
    비용 0원, 무제한 학습, 한국어 성능(ko-sroberta) 최적화 버전.
    """
    def __init__(self, model_name="jhgan/ko-sroberta-multitask"):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # GPU/CPU 자원을 사용하여 로컬에서 직접 수치화 (매우 빠름)
        embeddings = self.model.encode(texts)
        return embeddings.tolist()

    def embed_query(self, text: str) -> List[float]:
        embedding = self.model.encode([text])[0]
        return embedding.tolist()

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
        """여러 문서들을 한 번의 API 호출로 배치 임베딩합니다."""
        # Gemini Batch 임베딩 API 엔드포인트
        batch_api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:batchEmbedContents?key={self.api_key}"
        
        # 기사들을 20개씩 끊어서 배치 처리 (한 번에 너무 많으면 서버 에러 날 수 있으므로)
        batch_size = 30
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            
            requests_payload = []
            for text in batch_texts:
                requests_payload.append({
                    "model": f"models/{self.model}",
                    "content": {"parts": [{"text": text}]}
                })
            
            payload = {"requests": requests_payload}
            headers = {'Content-Type': 'application/json'}
            
            try:
                response = requests.post(batch_api_url, json=payload, headers=headers, timeout=30)
                if response.status_code != 200:
                    print(f"[Google Batch Debug] Error: {response.text}")
                response.raise_for_status()
                
                result = response.json()
                # 결과에서 각 임베딩 값만 추출
                for item in result['embeddings']:
                    all_embeddings.append(item['values'])
                
                # 가성비 모델을 위한 강제 휴식 (RPM 제한 방지)
                time.sleep(2)
                    
            except Exception as e:
                print(f"[GoogleBatchEmbeddings Error] {e}")
                # 실패 시 개별 임베딩으로 재시도하거나 에러 발생
                raise e
        
        return all_embeddings

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
