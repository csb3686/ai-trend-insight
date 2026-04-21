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
        # 1. 초도 생성된 가짜 데이터(Google)가 상위권을 장악해서 뚫지 못하므로, K값을 50으로 대폭 올려 진짜 기사만 필터링되도록 보장
        raw_docs = self.vector_db.similarity_search(question, k=50)
        
        # 2. 중복 제거 및 가짜 링크 필터링 (URL 및 제목 기준)
        seen_urls = set()
        seen_titles = set()
        unique_docs = []
        for doc in raw_docs:
            url = doc.metadata.get('url', '#')
            title = doc.metadata.get('title', '제목 없음').strip()
            
            # 구글 검색 및 GitHub 링크 필터링 (순수 뉴스 기사만 통과)
            if url.startswith('https://www.google.com/search') or 'github.com' in url:
                continue
                
            if url not in seen_urls and title not in seen_titles and url != '#':
                unique_docs.append(doc)
                seen_urls.add(url)
                seen_titles.add(title)
            if len(unique_docs) >= 3: # 최종적으로는 유니크한 3개만 사용
                break

        context_str = ""
        if not unique_docs:
            context_str = "수집된 뉴스가 없습니다."
        else:
            for i, doc in enumerate(unique_docs):
                title = doc.metadata.get('title', '제목 없음')
                url = doc.metadata.get('url', '#')
                context_str += f"[{i+1}] 제목: {title}\nURL: {url}\n내용: {doc.page_content}\n\n"
        
        # 3. Groq용 메시지 구성 (OpenAI 호환 포맷)
        messages = [
            {
                "role": "system", 
                "content": (
                    "You are 'TrendRadar AI', an expert in AI technology trends.\n\n"
                    "**[CRITICAL RULE: YOU MUST OUTPUT ONLY IN SOUTH KOREAN (한국어)]**\n"
                    "1. Provide your entire response strictly in natural Korean (e.g., ending with ~습니다, ~합니다).\n"
                    "2. **NEVER** use any Chinese characters (Hanzi/汉字) or Japanese characters (Hiragana/Katakana/Kanji). Translate concepts into Korean.\n"
                    "3. For the source section ('📚 주요 참고 소식'): \n"
                    "   - If the Context is '수집된 뉴스가 없습니다.', you MUST output exactly: '\n\n📚 주요 참고 소식\n* 현재 수집된 데이터 중 관련된 뉴스가 없습니다.' and do not create any links.\n"
                    "   - If the Context has news, you MUST use the provided Titles and URLs to create clickable markdown links format EXACTLY like this: '* [Title](URL)'. DO NOT just output plain text titles. DO NOT invent links.\n\n"
                    "**[Response Style]**\n"
                    "- Use Markdown formatting.\n"
                    "- Highlight key terms in **bold**.\n"
                    "- Be highly professional and polite."
                )
            },
            {
                "role": "user", 
                "content": f"Context:\n{context_str}\n\nQuestion: {question}"
            }
        ]

        payload = {
            "model": self.model_id,
            "messages": messages,
            "temperature": 0.2,  # 약간의 다양성을 허용하여 중국어 고착화(Greedy hole) 방지
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
                
                # 강제 한자/일본어 정규식 필터링 (최후의 방어선)
                import re
                answer = re.sub(r'[\u4e00-\u9fff\u3040-\u30ff]', '', answer)
            else:
                error_msg = response.json().get('error', {}).get('message', '알 수 없는 오류')
                answer = f"Groq API 오류 ({response.status_code}): {error_msg}\n※ .env 파일에 GROQ_API_KEY가 올바르게 입력되었는지 확인해 주세요."
                
        except Exception as e:
            answer = f"챗봇 통신 중 오류 발생: {str(e)}"

        # 5. 결과 조립 및 반환
        sources = []
        if unique_docs:
            for doc in unique_docs:
                sources.append({
                    "title": doc.metadata.get('title', '제목 없음'),
                    "url": doc.metadata.get('url', '#')
                })

        return {
            "answer": answer,
            "context": context_str,
            "sources": sources[:3] # 상위 3개만 반환
        }

# 싱글톤 인스턴스
rag_service = RAGService()
