# ✅ 개발 순서 체크리스트 (TODO.md)

> AI 기술 트렌드 인사이트 플랫폼 — 실행 가능한 개발 순서 체크리스트
> 체크박스를 채우며 진행하세요: `[ ]` → `[x]`

---

## Phase 1 — 환경 구성 & 로컬 서비스 설치 (예상: 2~3일)

### 1-1. 로컬 서비스 설치 및 확인
- [ ] Python 3.11+ 설치 확인
- [ ] Node.js 18+ 설치 확인
- [ ] MySQL 8.0 로컬 설치 및 실행 확인
- [ ] `pip install chromadb` 설치 확인
- [ ] `npm install -g n8n` 설치 확인
- [ ] `pip install langflow` 설치 확인

### 1-2. 데이터베이스 초기화
- [ ] `init.sql` 작성 (DB 생성, 사용자 권한 설정)
- [ ] `sources` 테이블 생성 + 초기 데이터 INSERT (긱뉴스, HN, GitHub)
- [ ] `articles` 테이블 생성 (type 컬럼으로 뉴스/github_repo 구분)
- [ ] `technologies` 테이블 생성 + 초기 키워드 50개 INSERT
- [ ] `article_technologies` 테이블 생성
- [ ] `trends` 테이블 생성
- [ ] `chat_sessions`, `chat_messages` 테이블 생성
- [ ] `collection_logs` 테이블 생성
- [ ] MySQL Workbench 또는 DBeaver로 스키마 확인

### 1-3. 프로젝트 구조 및 환경 설정
- [ ] 프로젝트 디렉토리 구조 생성 (`backend/`, `frontend/`, `pipeline/`, `n8n/`, `langflow/`)
- [ ] `backend/requirements.txt` 작성 (FastAPI, LangChain, SQLAlchemy, Pandas 등)
- [ ] Python 가상환경 생성 및 패키지 설치
- [ ] `.env.example` 파일 작성 (모든 환경 변수 목록)
- [ ] `.env` 파일 생성 (실제 값 입력)
- [ ] `.gitignore` 설정 (`.env`, `__pycache__`, `node_modules` 등)

---

## Phase 2 — React 프론트엔드 개발 / Mock 데이터 (예상: 5~7일)

> 💡 실제 API 없이 Mock 데이터로 UI를 먼저 완성합니다.
> Phase 7에서 실제 API로 교체만 하면 되도록 구조를 잡습니다.

### 2-1. 프로젝트 초기화
- [ ] `npx create-vite frontend --template react-ts` 실행
- [ ] 의존성 설치: `react-router-dom`, `@tanstack/react-query`, `zustand`
- [ ] 시각화 라이브러리 설치: `recharts` + `d3`
- [ ] HTTP 클라이언트: `axios` 설치
- [ ] `frontend/src/api/client.ts` — Axios 인스턴스 생성
- [ ] 빌드 확인: `npm run dev`

### 2-2. Mock 데이터 파일 작성
- [ ] `frontend/src/mocks/heatmap.json` — 히트맵 응답 형태
- [ ] `frontend/src/mocks/top5.json` — Top5 트렌드 응답 형태
- [ ] `frontend/src/mocks/articles.json` — 뉴스 목록 응답 형태
- [ ] `frontend/src/mocks/chat.json` — 챗봇 응답 형태
- [ ] Mock 훅 작성 (`useMockData.ts`) — 실제 훅과 동일한 인터페이스

### 2-3. 공통 컴포넌트
- [ ] `Layout.tsx` — 사이드바 + 헤더 레이아웃
- [ ] `Sidebar.tsx` — 네비게이션 메뉴
- [ ] `LoadingSpinner.tsx`
- [ ] `ErrorMessage.tsx`
- [ ] 다크 모드 토글 기능
- [ ] 전역 스타일 설정 (CSS Variables, Google Fonts)

### 2-4. 히트맵 페이지
- [ ] `pages/HeatmapPage.tsx` 생성
- [ ] `components/TechHeatmap.tsx` — D3.js 히트맵 컴포넌트
  - [ ] 언급 빈도에 따른 색상 강도
  - [ ] 키워드 hover 시 툴팁 (언급 횟수, 순위)
  - [ ] 키워드 클릭 시 관련 기사 목록 표시
- [ ] 기간 필터 UI (주간 / 월간)
- [ ] 카테고리 필터 UI

### 2-5. 트렌드 페이지
- [ ] `pages/TrendPage.tsx` 생성
- [ ] `components/Top5Card.tsx` — 상승/하락 Top 5 카드
  - [ ] 변화율 색상 표시 (상승: 초록, 하락: 빨강)
  - [ ] 화살표 아이콘 애니메이션
- [ ] `components/TimelineChart.tsx` — 멀티라인 차트 (Recharts)
  - [ ] 키워드 선택 토글
  - [ ] 줌 기능

### 2-6. RAG 챗봇 페이지
- [ ] `pages/ChatPage.tsx` 생성
- [ ] `components/ChatWindow.tsx` — 메시지 목록
- [ ] `components/ChatMessage.tsx` — 사용자/AI 메시지 버블
- [ ] `components/SourceCard.tsx` — 참조 기사 카드
- [ ] `components/ChatInput.tsx` — 입력창 + 전송 버튼
- [ ] 스트리밍 타이핑 애니메이션 (setTimeout 시뮬레이션)

### 2-7. 뉴스 페이지
- [ ] `pages/NewsPage.tsx` 생성
- [ ] `components/ArticleCard.tsx` — 기사 카드 컴포넌트
- [ ] 소스·날짜·키워드 필터 UI
- [ ] 무한 스크롤 구현 (`IntersectionObserver`)

### 2-8. 공통 마무리
- [ ] 반응형 레이아웃 확인 (모바일 768px 이하, 태블릿, 데스크탑)
- [ ] API 에러 핸들링 통일 (Toast 알림)
- [ ] 로딩 skeleton UI 적용

---

## Phase 3 — 데이터 수집 파이프라인 (예상: 3~4일)

### 3-1. RSS 수집기
- [ ] `pipeline/collectors/base_collector.py` — 공통 베이스 클래스 작성
- [ ] `pipeline/collectors/rss_parser.py` — feedparser 공통 유틸리티
- [ ] `pipeline/collectors/geek_news_collector.py` — 긱뉴스 RSS 수집
  - [ ] RSS 파싱 및 `articles` 테이블 저장
  - [ ] 중복 URL 체크 (url_hash)
  - [ ] `collection_logs` 기록
- [ ] `pipeline/collectors/hacker_news_collector.py` — Hacker News 수집
  - [ ] RSS 파싱 및 저장
- [ ] 로컬 실행 테스트 (`python -m pipeline.collectors.geek_news_collector`)

### 3-2. GitHub 트렌딩 크롤러
- [ ] Playwright 설치 (`playwright install chromium`)
- [ ] `pipeline/collectors/github_trending_collector.py` 작성
  - [ ] 트렌딩 페이지 크롤링 (daily/weekly)
  - [ ] 저장소명, 설명, 언어, 스타, 포크 수집
  - [ ] Topics 태그 수집
  - [ ] `articles` 테이블 저장 (type='github_repo')
- [ ] 헤드리스 모드 실행 확인

### 3-3. n8n 워크플로우 설정
- [ ] n8n 웹 UI 접속 확인 (`http://localhost:5678`)
- [ ] Workflow 1: 긱뉴스 RSS 자동 수집 (매시 정각)
  - [ ] Schedule Trigger 노드 설정
  - [ ] Execute Command 노드 (Python 스크립트 실행)
  - [ ] 에러 시 로그 기록 노드
- [ ] Workflow 2: Hacker News RSS 자동 수집 (매시 30분)
- [ ] Workflow 3: GitHub 트렌딩 자동 수집 (매 6시간)
- [ ] 모든 워크플로우 활성화(Activate) 및 첫 실행 확인
- [ ] n8n 워크플로우 JSON export 후 `n8n/` 폴더에 저장

---

## Phase 4 — 데이터 정제 및 통계 집계 (예상: 3~4일)

### 4-1. 데이터 정제 파이프라인
- [ ] `pipeline/processors/cleaner.py` 작성
  - [ ] HTML 태그 제거 (BeautifulSoup)
  - [ ] 특수문자·공백 정규화
  - [ ] 최소 길이 필터 (50자 미만 제거)
- [ ] `pipeline/processors/language_detector.py` 작성
  - [ ] langdetect 또는 langid 사용
- [ ] `pipeline/processors/processor.py` 작성
  - [ ] `articles`(is_processed=0) → 정제 후 is_processed=1 업데이트 파이프라인
  - [ ] 배치 처리 (한 번에 100개씩)
  - [ ] 처리 완료 시 `articles.is_processed = 1` 업데이트

### 4-2. 기술 키워드 추출
- [ ] `pipeline/processors/keyword_extractor.py` 작성
  - [ ] `technologies` 테이블에서 키워드 + aliases 로드
  - [ ] 정규식 패턴 동적 생성 (대소문자 무시, 단어 경계)
  - [ ] 기사 본문에서 키워드 매칭
  - [ ] 매칭 결과 캐싱 (키워드 목록 변경 전까지)
- [ ] 키워드 추출 정확도 수동 검증 (샘플 10개 기사)

### 4-3. 트렌드 통계 집계
- [ ] `pipeline/processors/stats_aggregator.py` 작성
  - [ ] 일별 언급 횟수 집계 쿼리
  - [ ] `trends` 테이블 upsert
  - [ ] 변화율(change_rate) 계산 로직
- [ ] 집계 스크립트 n8n Workflow 4에 연결 (매일 자정 실행)
- [ ] 집계 결과 확인 (SQL 쿼리로 검증)

---

## Phase 5 — 벡터 임베딩 & Chroma 저장 (예상: 2~3일)

### 5-1. 임베딩 파이프라인
- [ ] `pipeline/embedder/text_splitter.py` 작성
  - [ ] RecursiveCharacterTextSplitter 설정 (chunk_size=500, overlap=50)
  - [ ] 메타데이터 포함 Document 객체 생성
- [ ] `pipeline/embedder/embedder.py` 작성
  - [ ] GoogleGenerativeAIEmbeddings 초기화 (`models/embedding-001`)
  - [ ] Chroma 컬렉션 초기화 (`tech_articles`)
  - [ ] `articles` (is_embedded=0) 기사 배치 처리
  - [ ] 임베딩 완료 후 `is_embedded=1`, `embedding_id` 업데이트
- [ ] Chroma DB에 임베딩 저장 확인 (컬렉션 크기 확인)

### 5-2. Langflow 프로토타입
- [ ] Langflow 접속 (`http://localhost:7860`)
- [ ] Chroma Retriever 컴포넌트 연결
- [ ] LLM 컴포넌트 (Gemini 2.0 Flash) 연결
- [ ] Prompt Template 설정
- [ ] Langflow에서 테스트 질문 실행
- [ ] Langflow 플로우 JSON export 후 `langflow/` 폴더에 저장

---

## Phase 6 — FastAPI 백엔드 & RAG 챗봇 (예상: 4~5일)

### 6-1. 프로젝트 기초 설정
- [ ] `backend/app/main.py` 작성 (FastAPI 앱 초기화, CORS, 라우터 등록)
- [ ] `backend/app/core/config.py` — Pydantic Settings 설정
- [ ] `backend/app/core/database.py` — SQLAlchemy 엔진, 세션 팩토리
- [ ] `backend/app/models/` — SQLAlchemy ORM 모델 정의
- [ ] `backend/app/schemas/` — Pydantic 요청/응답 스키마 정의
- [ ] FastAPI 서버 기동 확인 (`uvicorn app.main:app --reload`)

### 6-2. 트렌드 API
- [ ] `backend/app/api/trends.py` 라우터 생성
- [ ] `GET /trends/heatmap` 구현
- [ ] `GET /trends/top5` 구현
- [ ] `GET /trends/timeline` 구현
- [ ] `GET /trends/keywords` 구현
- [ ] Swagger UI에서 각 엔드포인트 테스트

### 6-3. 기사 API
- [ ] `backend/app/api/articles.py` 라우터 생성
- [ ] `GET /articles` (페이지네이션) 구현
- [ ] `GET /articles/{id}` 구현
- [ ] `GET /articles/search` 구현

### 6-4. RAG 챗봇 API
- [ ] `backend/app/rag/retriever.py` 작성
  - [ ] Chroma 연결 설정
  - [ ] MMR 검색 설정 (`k=5`, `fetch_k=20`)
- [ ] `backend/app/rag/prompts.py` 작성
  - [ ] 한국어 시스템 프롬프트 (출처 인용 포함)
  - [ ] QA 프롬프트 템플릿
- [ ] `backend/app/rag/rag_chain.py` 작성
  - [ ] RetrievalQA 또는 LCEL 체인 구성 (gemini-2.0-flash)
  - [ ] 스트리밍 콜백 핸들러
- [ ] `backend/app/api/chat.py` 라우터 생성
- [ ] `POST /chat/sessions` 구현
- [ ] `POST /chat/sessions/{id}/messages` (RAG + SSE 스트리밍) 구현
- [ ] `GET /chat/sessions/{id}/messages` 구현
- [ ] 스트리밍 응답 브라우저에서 확인

### 6-5. 관리 및 헬스체크 API
- [ ] `backend/app/api/admin.py` 라우터 생성
- [ ] `POST /admin/collect` 구현
- [ ] `POST /admin/embed` 구현
- [ ] `POST /admin/recompute-stats` 구현
- [ ] `GET /admin/collection-logs` 구현
- [ ] `GET /health`, `GET /health/detail` 구현

### 6-6. 테스트
- [ ] pytest 설치 및 기본 설정
- [ ] 핵심 API 동작 확인 (수동 테스트)

---

## Phase 7 — 프론트엔드 실제 API 연결 (예상: 2~3일)

> 💡 Phase 2에서 Mock으로 완성한 UI를 실제 FastAPI 엔드포인트에 연결합니다.

### 7-1. Mock → 실제 API 교체
- [ ] `frontend/src/api/trends.ts` — 실제 트렌드 API 훅 작성
- [ ] `frontend/src/api/articles.ts` — 실제 기사 API 훅 작성
- [ ] `frontend/src/api/chat.ts` — 실제 챗봇 API 훅 작성
- [ ] 히트맵 페이지 Mock → 실제 API 연결
- [ ] 트렌드 페이지 Mock → 실제 API 연결
- [ ] 뉴스 페이지 Mock → 실제 API 연결

### 7-2. SSE 스트리밍 챗봇 연결
- [ ] `EventSource` 또는 `fetch` ReadableStream으로 스트리밍 수신 구현
- [ ] 기존 setTimeout 시뮬레이션 → 실제 스트리밍으로 교체
- [ ] 출처 카드 (SourceCard) 실제 데이터 연결

### 7-3. 전체 흐름 통합 테스트
- [ ] 데이터 수집 → MySQL → API → 프론트 렌더링 E2E 확인
- [ ] RAG 챗봇 질문 → 스트리밍 응답 브라우저 확인
- [ ] 브라우저 크로스체크 (Chrome, Firefox)

---

## 빠른 현황 체크

```
Phase 1  [ ] [ ] [ ]  환경 구성 & 로컬 설치
Phase 2  [ ] [ ] [ ]  React 프론트 (Mock)
Phase 3  [ ] [ ] [ ]  데이터 수집 파이프라인
Phase 4  [ ] [ ] [ ]  데이터 정제 & MySQL
Phase 5  [ ] [ ] [ ]  벡터 임베딩 & Chroma
Phase 6  [ ] [ ] [ ]  FastAPI 백엔드 & RAG
Phase 7  [ ] [ ] [ ]  프론트 실제 API 연결
```

---

> 💡 **팁**: 각 Phase가 끝날 때마다 `git commit`으로 진행 상황을 저장하세요.
> Phase 2(프론트 Mock)는 Phase 3~5와 병렬 진행이 가능합니다.
