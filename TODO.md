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

### 3-1. GitHub 실시간 수집기 (Playwright)
- [x] `pipeline/collectors/github_trending_collector.py` 작성
- [x] `Playwright` 기반 깃허브 트렌딩 페이지 크롤링 로직 구현 (Top 25)
- [x] 레포지토리 정보 및 가중치(Weight: 10) 부여 시스템 구축
- [x] `github_master_sync.py`를 통한 역사적 데이터(150개) 보강 완성

### 3-2. RSS 뉴스 수집기 (GeekNews, HackerNews)
- [x] `pipeline/collectors/geek_news_collector.py` 작성 (RSS Parser)
- [x] `pipeline/collectors/hacker_news_collector.py` 작성
- [x] 뉴스 제목 및 본문 기반 기술 키워드 매핑 로직 완성

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

### 5-2. LangChain 기반 RAG 엔진 직접 구현 (완료) 🏆
- [x] LangChain `Chroma` 벡터 스토어 직접 연동 완료
- [x] `GoogleGenerativeAIEmbeddings` 기반 검색 로직 구축 완료
- [x] `rag_service.py` 내 커스텀 프롬프트 템플릿 설계 및 적용 완료
- [x] **Gemini 2.0 Flash** 모델 연동을 통한 최종 답변 생성 파이프라인 완성
- [x] 참조 문서(Sources) 및 컨텍스트 메타데이터 추출 로직 구현 완료

> **💡 Decision Note**: 시각적 도구(Langflow)의 제약을 벗어나, 하이브리드 임베딩 로직의 세밀한 제어와 서버 경량화를 위해 **LangChain 직접 코딩(FastAPI 내장형)** 방식으로 최적화하여 구현함.

---

## Phase 6 — FastAPI 백엔드 & RAG 챗봇 (예상: 4~5일)

### 6-1. 프로젝트 기초 설정
- [x] `backend/app/main.py` 작성 (FastAPI 앱 초기화, CORS, 라우터 등록)
- [x] `backend/app/core/config.py` — Pydantic Settings 설정
- [x] `backend/app/core/database.py` — SQLAlchemy 엔진, 세션 팩토리
- [x] `backend/app/models/` — SQLAlchemy ORM 모델 정의
- [x] `backend/app/schemas/` — Pydantic 요청/응답 스키마 정의
- [x] FastAPI 서버 기동 확인 (`uvicorn app.main:app --reload`)

### 6-2. 트렌드 API
- [x] `backend/app/api/trends.py` 라우터 생성
- [x] `GET /trends/heatmap` 구현
- [x] `GET /trends/top5` 구현
- [x] `GET /trends/timeline` 구현
- [x] `GET /trends/keywords` 구현
- [x] Swagger UI에서 각 엔드포인트 테스트

### 6-3. 기사 API
- [x] `backend/app/api/articles.py` 라우터 생성
- [x] `GET /articles` (페이지네이션) 구현
- [x] `GET /articles/{id}` 구현
- [x] `GET /articles/search` 구현 (목록 페이지에서 필터로 통합 구현됨)

### 6-4. RAG 챗봇 API
- [x] `backend/app/rag/retriever.py` 작성 (rag_service.py로 통합 구현)
- [x] `backend/app/rag/prompts.py` 작성 (rag_service.py로 통합 구현)
- [x] `backend/app/rag/rag_chain.py` 작성 (Gemini-Embedding + Groq-LLM 하이브리드)
- [x] `backend/app/api/chat.py` 라우터 생성
- [x] `POST /chat` 구현 (ChatRequest/Response 구조)

### 6-5. 관리 및 헬스체크 API
- [x] `backend/app/api/admin.py` 라우터 생성
- [x] `POST /admin/collect` 구현 (Background Task 적용)
- [x] `POST /admin/embed` 구현 (Background Task 적용)
- [x] `POST /admin/recompute-stats` 구현 (Background Task 적용)
- [x] `GET /admin/collection-logs` 구현 (수집 이력 확인)
- [x] `GET /health`, `GET /health/detail` 구현 (시스템 정밀 진단)

### 6-6. 테스트
- [x] pytest 설치 및 기본 설정 완료 (test_api_v1.py 등)

---

## Phase 7 — 프론트엔드 실제 API 연결 (예상: 2~3일)

> 💡 Phase 2에서 Mock으로 완성한 UI를 실제 FastAPI 엔드포인트에 연결합니다.

### 7-1. Mock → 실제 API 교체
- [x] `frontend/src/api/client.ts` — Axios 공통 클라이언트 작성
- [x] `frontend/src/api/hooks/` — 도메인별(Trends, Articles, Chat) 훅 작성
- [x] 히트맵 리스트 Mock → 실제 API 연결 (`useTrendHeatmap`)
- [x] 트렌드 Top 5 Mock → 실제 API 연결 (`useTopTrends`)
- [x] 최신 소식 Mock → 실제 API 연결 (`useArticles`)

### 7-2. AI 챗봇 실제 연동
- [x] `useChatMutation` — Groq RAG 서비스 연결
- [x] 시스템 메시지 및 사용자 질문/응답 대응 UI 구현
- [x] 답변 로딩 상태 및 에러 핸들링 추가

### 7-3. 전체 흐름 통합 테스트
- [x] 데이터 수집 → MySQL → API → 프론트 렌더링 E2E 확인
- [x] RAG 챗봇 질문 → 실제 AI 텍스트 응답 정상 노출 테스트
- [x] 크로스 브라우징 확인 (Chrome, Edge 등)

---

## Phase 8 — QA 자동화 테스트 및 CI 파이프라인 구축 (완료) 🏆

### 8-1. Pytest 기반 QA 테스트 자동화
- [x] `backend/tests/` 구조 세팅 및 `pytest.ini` 환경 설정 완료
- [x] 핵심 API 동작 검증 (Health, Trends, Articles, Chat) 테스트 작성
- [x] `conftest.py` 기반 비동기 테스트 클라이언트(`httpx`) 인프라 구축
- [x] 실제 서버 스펙과 테스트 코드 100% 동기화 완료

### 8-2. Playwright 기반 E2E 테스트 자동화
- [x] 프론트엔드 E2E 테스트 환경 구축 및 `playwright.config.ts` 최적화
- [x] 에코시스템 시각화 맵 및 유동적 캔버스(Cytoscape) 검증 로직 구현
- [x] 로컬 환경 안정성을 위한 `retries` 및 `workers` 설정 고도화

### 8-3. GitHub Actions CI 파이프라인
- [x] `.github/workflows/qa_automation.yml` 워크플로우 명세 작성
- [x] 코드 Push 시 백엔드/프론트엔드 자동 테스트 수행 체계 구축

---

### 9-1. 데이터 정교화 및 마스터피스 폴리싱 (완료) 🏆
- [x] **하이브리드 전략**: 실제 크롤링 + 3개월 역사 데이터 보강
- [x] **데이터 무결성**: 404 링크 제거 및 구글/GitHub 검색 엔진 연동
- [x] **통합 마스터 싱크**: `/debug/final-polish` 원클릭 정화 및 주입 구현
- [x] **UI/UX 정교화**: 오표기된 소스 이름 전수 교정 및 정합성 확보

### 9-2. 관리자 시스템 조종석(Cockpit) 2.0 및 AI 엔진 복구 (완료) 🏆
- [x] **조종석 2.0 UI**: 프리미엄 다크 테마 및 실시간 시스템 헬스체크 대시보드 구현
- [x] **시스템 로그 고도화**: 상세 에러 조회(🔍) 및 ✅/❌ 상태 실시간 모니터링 적용
- [x] **AI 엔진 정상화**: 404 Not Found 해결을 위한 `GoogleDirectEmbeddings` 직접 호출 구현
- [x] **모델 최적화**: `gemini-embedding-001` 및 최신형 **Gemini 2.0 Flash** 엔진 장착
- [x] **성능 상향**: AI 학습 배치 처리량을 20개에서 **100개**로 5배 강화
- [x] **DB 정합성**: `collection_logs` 스키마 수정 및 `source_id` 연동 완료

---

## 빠른 현황 체크
- [x] Phase 1 ~ 12 모든 단계 완료 (Post-Optimization 포함)

```
Phase 1  [x]  환경 구성 & 로컬 설치
Phase 2  [x]  React 프론트 (Mock)
Phase 3  [x]  데이터 수집 파이프라인
Phase 4  [x]  데이터 정제 & MySQL
Phase 5  [x]  벡터 임베딩 & Chroma
Phase 6  [x]  FastAPI 백엔드 & RAG
Phase 7  [x]  프론트 실제 API 연결
Phase 8  [x]  QA 자동화 테스트 & CI 구축
Phase 9  [x]  대시보드 마스터피스 폴리싱
Phase 10 [x]  조종석 2.0 & AI 엔진 복구 (Hotfix 완료)
Phase 11 [x]  네온 시각화 및 시스템 안정성 끝판왕 고도화
Phase 12 [x]  빌보드급 시인성 확보 및 정밀 로딩 시스템 구축 (Final 🚀)
```

---

### 🕙 Phase 11 — 울트라 프리미엄 고도화 & 시스템 안정성 강화 (완료) 🏆
- [x] **고밀도 스파크라인**: Top 5 트렌드 카드 내 Recharts 네온 글로우(Neon Glow) 차트 이식 완료
- [x] **디자인 폴리싱**: 불필요한 뉴스 제목, 돋보기, 아이콘 제거 및 미니멀리즘 프리미엄 UI 완성
- [x] **시스템 복원력**: 프론트엔드 API 개별 생존(Individual Fetch) 로직 및 10초 타임아웃 적용 완료
- [x] **백엔드 최적화**: SQLAlchemy 커넥션 풀(`pool_size=10`, `max_overflow=20`) 및 DB 락(Lock) 방지 로직 강화 완료
- [x] **문서 동기화**: 프로젝트의 모든 설계 문서를 실제 구현 코드와 100% 동기화 완료

### 🕙 Phase 12 — 빌보드급 시인성 확보 및 정밀 로딩 시스템 구축 (완료) 🏆
- [x] **빌보드 UI**: 사이토스케이프(Cytoscape) 노드 및 폰트 크기를 극대화(24-32px)하여 전광판급 시인성 확보 완료
- [x] **정밀 로깅 시스템**: `logger.py` 신설 및 모든 수집 파이프라인에 파일 기반 로그 기록 체계 도입 완료
- [x] **안정성 강화**: 수집기 예외 처리 강화로 네트워크 지연 및 에러 시 스케줄러 생존 로직 보강 완료
- [x] **포트폴리오 폴리싱**: 면접관 대응용 기술 설명서 작성 및 문서 최종 업데이트 완료

---

> 💡 **팁**: 각 Phase가 끝날 때마다 `git commit`으로 진행 상황을 저장하세요.
> Phase 2(프론트 Mock)는 Phase 3~5와 병렬 진행이 가능합니다.

---

### 🕙 Phase 13 — 서비스 컨테이너화 및 배포 인프라 구축 (최종 완료) 🏆
- [x] **전체 시스템 컨테이너화**: Backend, Frontend, Scheduler, DB를 Docker Compose로 통합
- [x] **데이터 영속성 확보**: MySQL 볼륨 바인딩(`./mysql_data`) 설정을 통한 데이터 보존 체계 구축
- [x] **인프라 최적화**: Nginx 리버스 프록시 설계 및 Node.js 20 LTS 빌드 환경 고도화
- [x] **코드 정제**: TypeScript 엄격 빌드 검사 통과를 위한 코드 리팩토링 및 타입 보강 완료
- [x] **원클릭 구동**: `docker-compose up -d --build` 명령어를 통한 무결점 자동 배포 확인

### 🕙 Phase 14 — 챗봇 3대 난제(가짜 링크, 중복, 한자 혼용) 완벽 수술 (완료) 🏆
- [x] **도커 인코딩 복원**: `Dockerfile` 로케일 및 `PYTHONIOENCODING=utf-8` 주입 완료
- [x] **중복 & 환각 방어**: 코드 레벨(Python) 중복 처리 및 가짜 구글 검색 링크 차단 로직 도입
- [x] **언어 규칙 재정립**: 영문 System Prompt 변환 및 강력어조 주입으로 100% 한국어 출력 강제
- [x] **최후의 방어선**: CJK 문자 정규식(Regex) 필터링으로 잠재적 한자/일본어 파편 원천 소거 완료
