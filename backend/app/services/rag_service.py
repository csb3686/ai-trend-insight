import os
import json
import requests
from typing import List, Dict, Any
from langchain_community.vectorstores import Chroma
from app.core.config import get_settings
from app.core.embedding_utils import GoogleDirectEmbeddings, LocalEmbeddings

settings = get_settings()

class RAGService:
    def __init__(self):
        # 1. 임베딩 모델 설정 (설정에 따라 로컬/구글 스위칭)
        if settings.embedding_provider == "local":
            self.embeddings = LocalEmbeddings(model_name="jhgan/ko-sroberta-multitask")
            print("[RAG Service] Using Local Embedding Mode (ko-sroberta)")
        else:
            self.embeddings = GoogleDirectEmbeddings(
                model="gemini-embedding-001",
                api_key=settings.gemini_api_key
            )
            print("[RAG Service] Using Google Gemini Embedding Mode")
        
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
        context_str = ""
        for i, doc in enumerate(docs):
            title = doc.metadata.get('title', '제목 없음')
            url = doc.metadata.get('url', '#')
            context_str += f"[{i+1}] 제목: {title}\nURL: {url}\n내용: {doc.page_content}\n\n"
        
        # 3. Groq용 메시지 구성 (OpenAI 호환 포맷)
        messages = [
            {
                "role": "system", 
                "content": (
                    "당신은 AI 기술 트렌드 분석 전문가인 'TrendRadar AI'입니다. "
                    "제공된 [참고 뉴스]들을 바탕으로 질문에 대해 전문적이고 친절하게 답변해 주세요.\n\n"
                    "**[답변 규칙]**\n"
                    "1. 반드시 **마크다운(Markdown)** 형식을 사용하여 가독성을 높이세요.\n"
                    "2. 핵심 키워드는 **굵게(Bold)** 표시하세요.\n"
                    "3. 복잡한 설명은 **불렛 포인트(Bullet points)**를 활용하여 개조식으로 요약하세요.\n"
                    "4. 답변 마지막에는 반드시 참고한 기사들 중 가장 관련성이 높은 1~3개를 '**📚 주요 참고 소식**' 섹션에 마크다운 링크 형식으로 나열하세요.\n"
                    "   - 형식: [기사 제목](기사 URL)\n"
                    "5. 만약 참고 뉴스에 관련 내용이 없다면, 일반적인 기술 지식을 바탕으로 선의의 답변을 제공하되 출처가 우리 DB가 아님을 명시하세요."
                )
            },
            {
                "role": "user", 
                "content": f"[참고 뉴스]:\n{context_str}\n\n질문: {question}"
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

        # 5. 결과 조립 및 반환
        sources = []
        # 중복 제거를 위해 URL 기준으로 확인
        seen_urls = set()
        for doc in docs:
            url = doc.metadata.get('url', '#')
            if url not in seen_urls:
                sources.append({
                    "title": doc.metadata.get('title', '제목 없음'),
                    "url": url
                })
                seen_urls.add(url)

        return {
            "answer": answer,
            "context": context_str,
            "sources": sources[:3] # 상위 3개만 반환
        }

# 싱글톤 인스턴스
rag_service = RAGService()
