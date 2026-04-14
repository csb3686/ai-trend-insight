import os
import json
import requests
from typing import List, Dict, Any
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from app.core.config import get_settings

settings = get_settings()

class RAGService:
    def __init__(self):
        # 1. 임베딩 모델 설정 (Gemini 계속 사용)
        # 이미 이 모델로 DB가 구축되어 있으므로 변경하지 않습니다.
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-2-preview",
            google_api_key=settings.gemini_api_key
        )
        
        # 2. 벡터 DB 연결
        current_dir = os.path.dirname(os.path.abspath(__file__))
        persist_directory = os.path.normpath(os.path.join(current_dir, "../../../", settings.chroma_storage_path))
        
        self.vector_db = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings,
            collection_name="trend_insight_final"
        )
        
        # 3. Groq API 설정 (대화 전용)
        self.api_key = settings.groq_api_key
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model_id = "llama-3.3-70b-versatile"  # Groq의 고성능 Llama 3 모델

    async def get_answer(self, question: str) -> Dict[str, Any]:
        """
        Gemini를 통해 정보를 검색하고, Groq을 통해 초고속으로 답변을 생성하는 하이브리드 RAG 시스템입니다.
        """
        # 1. 유사한 기사 검색 (Top 3)
        docs = self.vector_db.similarity_search(question, k=3)
        
        # 2. 컨텍스트 구성
        context_list = []
        for doc in docs:
            title = doc.metadata.get('title', '제목 없음')
            url = doc.metadata.get('url', 'N/A')
            content = doc.page_content
            context_list.append(f"--- [기사]: {title} ---\n[내용]: {content}\n[URL]: {url}")
        
        context = "\n\n".join(context_list)
        
        # 3. Groq용 메시지 구성 (OpenAI 호환 포맷)
        messages = [
            {
                "role": "system", 
                "content": (
                    "당신은 AI 기술 트렌드 분석 전문가입니다. 아래 제공된 [참고 뉴스]들을 바탕으로 질문에 대해 친절하게 답변해 주세요. "
                    "반드시 제공된 뉴스 내용을 기반으로 답변하되, 관련 내용이 부족하다면 아는 지식 내에서 최신 기술 트렌드를 친절히 알려주세요. "
                    "마지막에는 참고한 기사들 제목을 언급해 주세요."
                )
            },
            {
                "role": "user", 
                "content": f"[참고 뉴스]:\n{context}\n\n질문: {question}"
            }
        ]

        payload = {
            "model": self.model_id,
            "messages": messages,
            "temperature": 0.1,
            "max_tokens": 2048
        }

        # 4. Groq API 호출
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result['choices'][0]['message']['content']
            else:
                error_msg = response.json().get('error', {}).get('message', '알 수 없는 오류')
                answer = f"Groq API 오류 ({response.status_code}): {error_msg}\n※ .env 파일에 GROQ_API_KEY가 올바르게 입력되었는지 확인해 주세요."
                
        except Exception as e:
            answer = f"챗봇 통신 중 오류 발생: {str(e)}"

        return {
            "answer": answer,
            "context": context,
            "sources": [doc.metadata.get('title') for doc in docs if doc.metadata.get('title')]
        }

# 싱글톤 인스턴스
rag_service = RAGService()
