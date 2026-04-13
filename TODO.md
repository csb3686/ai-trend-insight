# ✅ 개발 순서 체크리스트 (TODO.md)

> AI 기술 트렌드 인사이트 플랫폼 — 실행 가능한 개발 순서 체크리스트
> 체크박스를 채우며 진행하세요: `[ ]` → `[x]`

### 🎯 핵심 UX/기획 원칙
1. **로그인 불필요 (Public Open)**: 포트폴리오 접근성 극대화를 위해 로그인 없이 누구나 볼 수 있도록 구성. (필요 시 /admin만 HTTP 기본 인증)
2. **내장형 챗봇 (Floating Widget)**: 별도의 챗봇 페이지 대신 우측 하단에 떠 있는 슬라이드 패널 위젯으로 구현하여 사용성 향상.
3. **히트맵 상세 패널 (Drawer)**: 히트맵의 기술을 누르면 화면 전환 없이 우측에서 해당 기술의 뉴스/트렌드 요약 패널이 열리도록 구성.

---

## Phase 1 — 환경 구성 & 로컬 서비스 설치 (예상: 2~3일)

### 1-1. 로컬 서비스 설치 및 확인
- [x] Python 3.11+ 설치 확인
- [x] Node.js 18+ 설치 확인
- [x] MySQL 8.0 로컬 설치 및 실행 확인
- [x] `pip install chromadb` 설치 확인
- [x] `npm install -g n8n` 설치 확인
- [x] `pip install langflow` 설치 확인

### 1-2. 데이터베이스 초기화
- [x] `init.sql` 작성 (DB 생성, 사용자 권한 설정)
- [x] `sources` 테이블 생성 + 초기 데이터 INSERT (긱뉴스, HN, GitHub)
- [x] `articles` 테이블 생성 (type 컬럼으로 뉴스/github_repo 구분)
- [x] `technologies` 테이블 생성 + 초기 키워드 50개 INSERT
- [x] `article_technologies` 테이블 생성
- [x] `trends` 테이블 생성
- [x] `chat_sessions`, `chat_messages` 테이블 생성
- [x] `collection_logs` 테이블 생성
- [x] MySQL Workbench 또는 DBeaver로 스키마 확인

### 1-3. 프로젝트 구조 및 환경 설정
- [x] 프로젝트 디렉토리 구조 생성 (`backend/`, `frontend/`, `pipeline/`, `n8n/`, `langflow/`)
- [x] `backend/requirements.txt` 작성 (FastAPI, LangChain, SQLAlchemy, Pandas 등)
- [x] Python 가상환경 생성 및 패키지 설치
- [x] `.env.example` 파일 작성 (모든 환경 변수 목록)
- [x] `.env` 파일 생성 (실제 값 입력)
- [x] `.gitignore` 설정 (`.env`, `__pycache__`, `node_modules` 등)

---

## Phase 2 — React 프론트엔드 개발 / Mock 데이터 (예상: 5~7일)

> 💡 실제 API 없이 Mock 데이터로 UI를 먼저 완성합니다.
> Phase 7에서 실제 API로 교체만 하면 되도록 구조를 잡습니다.

### 2-1. 프로젝트 초기화
- [x] `npx create-vite frontend --template react-ts` 실행
- [x] 의존성 설치: `react-router-dom`, `@tanstack/react-query`, `zustand`
- [x] 시각화 라이브러리 설치: `recharts` + `d3`
- [x] HTTP 클라이언트: `axios` 설치
- [x] `frontend/src/api/client.ts` — Axios 인스턴스 생성
- [x] 빌드 확인: `npm run dev`

### 2-2. Mock 데이터 파일 작성
- [x] `frontend/src/mocks/heatmap.json` — 히트맵 응답 형태
- [x] `frontend/src/mocks/top5.json` — Top5 트렌드 응답 형태
- [x] `frontend/src/mocks/articles.json` — 뉴스 목록 응답 형태
- [x] `frontend/src/mocks/chat.json` — 챗봇 응답 형태
- [x] Mock 훅 작성 (`useMockData.ts`) — 실제 훅과 동일한 인터페이스

### 2-3. 공통 컴포넌트
- [x] `Layout.tsx` — 사이드바 + 헤더 레이아웃
- [x] `Sidebar.tsx` — 네비게이션 메뉴
- [x] `LoadingSpinner.tsx`
- [x] `ErrorMessage.tsx`
- [x] 다크 모드 토글 기능
- [x] 전역 스타일 설정 (CSS Variables, Google Fonts)

### 2-4. 히트맵 페이지
- [x] `pages/HeatmapPage.tsx` 대신 대시보드 컴포넌트로 통합 (`TechHeatmap.tsx`)
- [x] `components/TechHeatmap.tsx` — 히트맵 컴포넌트
  - [x] 언급 빈도에 따른 색상 강도
  - [x] 키워드 hover 시 툴팁 (언급 횟수, 순위)
- [ ] `components/TechDetailDrawer.tsx` — 키워드 클릭 시 나오는 우측 슬라이드 패널 (트렌드 미니 차트, 뉴스 3건, AI 한줄 요약)
- [x] 기간 필터 UI (주간 / 월간)
- [x] 카테고리 필터 UI

### 2-5. 트렌드 페이지
- [x] `pages/TrendPage.tsx` 생성
- [x] `components/Top5Card.tsx` — 상승/하락 Top 5 카드
  - [x] 변화율 색상 표시 (상승: 초록, 하락: 빨강)
  - [x] 화살표 아이콘 애니메이션
- [x] `components/TimelineChart.tsx` — 멀티라인 차트 (Recharts)
  - [x] 키워드 선택 토글
  - [x] 줌 기능

### 2-6. 플로팅 RAG 챗봇 위젯
- [x] `components/ChatWidget.tsx` 생성 (우측 하단 플로팅 완성)
- [x] `components/ChatWindow.tsx` — (ChatWidget 내부에 패널 구조로 통합)
- [x] `components/ChatMessage.tsx` — (사용자/AI 말풍선 UI 통합)
- [x] `components/SourceCard.tsx` — 참조 기사 카드 (구현 대기 또는 간소화)
- [x] `components/ChatInput.tsx` — 입력창 + 전송 버튼 (통합 완료)
- [ ] 스트리밍 타이핑 애니메이션 (나중에 백엔드 API 연결 시 적용)

### 2-7. 뉴스 페이지
- [x] `pages/NewsPage.tsx` 생성
- [x] `components/ArticleCard.tsx` — 기사 카드 컴포넌트
- [x] 소스·날짜·키워드 필터 UI
- [x] 무한 스크롤 구현 (`IntersectionObserver`)

### 2-8. 공통 마무리
- [x] 반응형 레이아웃 확인 (모바일 768px 이하, 태블릿, 데스크탑)
- [x] API 에러 핸들링 통일 (Toast 알림)
- [x] 로딩 skeleton UI 적용

---

## Phase 3 — 데이터 수집 파이프라인 (예상: 3~4일)

### 3-1. RSS 수집기
- [x] `pipeline/collectors/base_collector.py` — 공통 베이스 클래스 작성
- [x] `pipeline/collectors/rss_parser.py` — feedparser 공통 유틸리티
- [x] `pipeline/collectors/geek_news_collector.py` — 긱뉴스 RSS 수집
  - [x] RSS 파싱 및 `articles` 테이블 저장
  - [x] 중복 URL 체크 (url 컬럼 기반)
  - [x] `collection_logs` 기록
- [x] `pipeline/collectors/hacker_news_collector.py` — Hacker News 수집
  - [x] RSS 파싱 및 저장
- [x] 로컬 실행 테스트 (`python -m pipeline.collectors.geek_news_collector`)

### 3-2. GitHub 트렌딩 크롤러
- [x] Playwright 설치 (`playwright install chromium`)
- [x] `pipeline/collectors/github_trending_collector.py` 작성
  - [x] 트렌딩 페이지 크롤링 (daily/weekly)
  - [x] 저장소명, 설명, 언어, 스타, 포크 수집
  - [x] Topics 태그 수집
  - [x] `articles` 테이블 저장 (type='github_repo')
- [x] 헤드리스 모드 실행 확인

### 3-3. Python 자체 스케줄러 구축 (n8n 대체)
- [x] `backend/requirements.txt`에 `schedule` 라이브러리 추가
- [x] `backend/pipeline/scheduler.py` 매니저 스크립트 작성
- [x] 파이썬 코드로 각각의 크롤러 함수 import (subprocess 혹은 직접 호출)
- [x] `schedule.every(1).hours` 등 타임스케줄 세팅 및 무한 루프 런타임 적용
- [x] 백그라운드 런타임 스케줄러 정상 작동 테스트

---

## Phase 4 — 데이터 정제 및 통계 집계 (예상: 3~4일)

### 4-1. 데이터 정제 파이프라인
- [x] `pipeline/processors/cleaner.py` 작성
  - [x] HTML 태그 제거 (BeautifulSoup)
  - [x] 특수문자·공백 정규화
  - [x] 최소 길이 필터 (50자 미만 제거 혹은 플래그 처리)
- [x] `pipeline/processors/language_detector.py` 작성
  - [x] langdetect 사용
- [x] `pipeline/processors/processor.py` 작성
  - [x] `articles`(is_processed=0) → 정제 후 is_processed=1 업데이트 파이프라인
  - [x] 배치 처리 (한 번에 100개씩)
  - [x] 처리 완료 시 `articles.is_processed = 1` 업데이트 및 빈 글 필터링

### 4-2. 기술 키워드 추출
- [x] `pipeline/processors/keyword_extractor.py` 작성
  - [x] `technologies` 테이블에서 키워드 + aliases 로드
  - [x] 정규식 패턴 동적 생성 (대소문자 무시, 단어 경계)
  - [x] 기사 본문에서 키워드 매칭 및 횟수 산출
- [x] `processor.py` 연동 및 `article_technologies` 테이블 저장 로직 구현 완료

### 4-3. 트렌드 통계 집계
- [x] `pipeline/processors/stats_aggregator.py` 작성
  - [x] 월별 언급 횟수 집계 쿼리 (trends 테이블용)
  - [x] 전월 대비 변화율(change_rate) 및 순위 계산
- [x] 전체 데이터 기반 통계 재산출 로직 구현 및 검증 완료
- [x] 정기 집계 스케줄러(`scheduler.py`) 연동 완료 (전처리 1h, 통계 6h)

---

## Phase 5 — 벡터 임베딩 & Chroma 저장 (예상: 2~3일)

### 5-1. 임베딩 파이프라인
- [x] `pipeline/embedder/text_splitter.py` 작성
  - [x] RecursiveCharacterTextSplitter 설정 (chunk_size=500, overlap=50)
  - [x] 메타데이터 포함 Document 객체 생성
- [x] `pipeline/embedder/embedder.py` 작성
  - [x] GoogleGenerativeAIEmbeddings 초기화 (`models/embedding-001`)
  - [x] Chroma 컬렉션 초기화 (`tech_articles`)
  - [x] `articles` (is_embedded=0) 기사 배치 처리
  - [x] 임베딩 완료 후 `is_embedded=1` 업데이트 및 상태 관리
- [x] 스케줄러(`scheduler.py`) 연동 및 자동 임베딩 로직 완료
- [x] Chroma DB 저장 확인 (`backend/chroma_db` 폴더 생성 및 데이터 적재 완료)

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
- [ ] RAG 챗봇 질문 → 스트리밍 텍스트 응답 정상 노출 테스트
- [ ] 크로스 브라우징 확인 (Chrome, Edge 등)

---

## Phase 8 — QA 자동화 테스트 및 CI 파이프라인 구축 (이력서 보너스 트랙)

### 8-1. Pytest 기반 QA 테스트 자동화
- [ ] `backend/tests/` 구조 세팅 및 `pytest` 패키지 설치
- [ ] 수집기 단위 테스트 (RSS 통신 성공 여부 Mocking)
- [ ] 데이터베이스 저장 포맷(무결성) 검증 테스트 로직
- [ ] FastAPI 엔드포인트 응답 상태코드(200 OK) 자동 확인용 API 테스트 작성

### 8-2. GitHub Actions 자동화 파이프라인 (CI)
- [ ] `.github/workflows/qa-test.yml` 파일 생성
- [ ] GitHub에 Push 하거나 Pull Request 발생 시 자동으로 봇이 구동되도록 지시
- [ ] 클라우드 가상환경(Ubuntu) 셋업 및 Python 3.13 설치 자동화 작성
- [ ] PR 화면에 "모든 QA 테스트 합격(초록색 체크)" 마크가 뜨도록 연동
- [ ] README.md 에 `passing` 배지 부착

---

## 빠른 현황 체크
- [x] Phase 1 완료 (설치 및 DB 스키마)
- [x] Phase 2 완료 (React 퍼블리싱)
- [x] Phase 3 완료 (수집 데이터 적재)
- [x] Phase 4 완료 (Pandas 정제, 통계치 추출)
- [x] Phase 5 완료 (ChromaDB 벡터 임베딩)
- [ ] Phase 6 완료 (Gemini RAG 기반 백엔드 API 완성)
- [ ] Phase 7 완료 (프론트/백 최종 연동)
- [ ] Phase 8 완료 (QA 테스트 및 CI 파이프라인 통합)

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
