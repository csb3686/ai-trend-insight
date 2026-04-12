# 📋 개발 단계별 계획 (PLAN.md)

> AI 기술 트렌드 인사이트 플랫폼 — 포폴용 MVP 7단계 로드맵

---

## 📅 전체 일정 요약

| 단계 | 내용 | 예상 기간 |
|------|------|-----------|
| 1단계 | 환경 구성 & 로컬 서비스 설치 | 0.5주 |
| 2단계 | React 프론트엔드 개발 (Mock) | 1.5주 |
| 3단계 | 데이터 수집 파이프라인 | 1주 |
| 4단계 | 데이터 정제 & MySQL 저장 | 1주 |
| 5단계 | 벡터 임베딩 & Chroma 저장 | 1주 |
| 6단계 | FastAPI 백엔드 & RAG 챗봇 | 2주 |
| 7단계 | 프론트엔드 실제 API 연결 | 0.5주 |

---

## 🟦 1단계 — 환경 구성 & 로컬 서비스 설치

### 목표
로컬 개발 환경을 세팅합니다. (**Docker 미사용**, 모든 서비스는 로컬에 직접 설치)

### 작업 내역
1. **로컬 서비스 설치**
   - Python 3.11+, Node.js 18+ 설치 확인
   - MySQL 8.0 로컬 설치 및 초기 DB 세팅 (`init.sql`)
   - Chroma 로컬 설치 (`pip install chromadb`)
   - n8n npm 설치 (`npm install -g n8n`) 및 실행 (`n8n start`)
   - Langflow 설치 (`pip install langflow`) 및 실행 (`langflow run`)

2. **프로젝트 구조 & 환경 변수 설정**
   - 디렉토리 구조 생성 (`backend/`, `frontend/`, `pipeline/`, `n8n/`, `langflow/`)
   - `.env.example` 작성 (GEMINI_API_KEY, GITHUB_TOKEN, MYSQL_…)
   - `.gitignore` 설정

### 산출물
- `.env.example`
- `init.sql` (MySQL 스키마 초기화 스크립트)

### 완료 기준
- 모든 서비스 로컬 실행 확인 (MySQL, Chroma, n8n, Langflow)

---

## 🟦 2단계 — React 프론트엔드 개발 (Mock 데이터)

### 목표
**실제 API 없이 Mock 데이터**로 UI를 먼저 완성합니다.
나중에 7단계에서 실제 API로 교체만 하면 되도록 구조를 잡습니다.

### 작업 내역
1. **프로젝트 초기화**
   - Vite + React 18 + TypeScript 설정
   - 의존성: `react-router-dom`, `@tanstack/react-query`, `recharts`, `d3`, `axios`, `zustand`

2. **Mock 데이터 구성**
   - `frontend/src/mocks/` 디렉토리에 각 API 응답 형태로 JSON 작성
   - 히트맵 mock, Top5 트렌드 mock, 뉴스 목록 mock, 챗봇 응답 mock

3. **공통 레이아웃 & 컴포넌트**
   - `Layout.tsx` — 사이드바 + 헤더
   - `LoadingSpinner.tsx`, `ErrorMessage.tsx`
   - 다크 모드 토글, CSS Variables / Google Fonts

4. **히트맵 페이지 (Mock)**
   - D3.js 기반 기술 히트맵 컴포넌트
   - 언급 빈도에 따른 색상 강도, 호버 툴팁
   - 기간(주간/월간) 필터 UI

5. **트렌드 페이지 (Mock)**
   - Top 5 변화율 카드 (상승↑ 초록, 하락↓ 빨강)
   - Recharts 멀티라인 차트

6. **RAG 챗봇 페이지 (Mock)**
   - 채팅 UI (메시지 버블, 출처 카드)
   - 스트리밍 타이핑 애니메이션 (setTimeout 시뮬레이션)

7. **뉴스 페이지 (Mock)**
   - 기사 카드 컴포넌트, 필터 UI, 무한 스크롤

8. **반응형 & 다크 모드**

### 산출물
- `frontend/src/mocks/*.json`
- `frontend/src/pages/` (HeatmapPage, TrendPage, ChatPage, NewsPage)
- `frontend/src/components/` (TechHeatmap, Top5Card, ChatWindow, ArticleCard 등)

### 완료 기준
- Mock 데이터로 히트맵·트렌드·챗봇·뉴스 네 화면 모두 렌더링 확인
- 모바일/데스크톱 반응형 레이아웃 정상 동작

---

## 🟦 3단계 — 데이터 수집 파이프라인

### 목표
n8n 워크플로와 Playwright 크롤러로 자동 데이터 수집 파이프라인을 구성합니다.

### 작업 내역
1. **RSS/API 수집기 구현**
   - `pipeline/collectors/geek_news_collector.py` — 긱뉴스 RSS
   - `pipeline/collectors/hacker_news_collector.py` — Hacker News RSS
   - `pipeline/collectors/github_trending_collector.py` — Playwright 크롤링

2. **n8n 워크플로 구성**
   - 긱뉴스 RSS 수집 워크플로 (매일 06:00 Cron)
   - Hacker News RSS 수집 워크플로 (매일 06:00 Cron)
   - GitHub Trending API 수집 워크플로 (매일 07:00 Cron)
   - 수집 결과 → `articles` 테이블 저장

### 산출물
- `data-pipeline/collectors/*.py`
- `data-pipeline/n8n/` 워크플로 JSON 파일 3개

### 완료 기준
- n8n 워크플로 수동 실행 시 `articles` 테이블에 데이터 정상 저장 확인

---

## 🟦 4단계 — 데이터 정제 & MySQL 저장

### 목표
수집된 원시 데이터를 정제하고 MySQL에 구조화하여 저장합니다.

### 작업 내역
1. **Pandas 기반 정제 파이프라인**
   - HTML 태그 제거, 특수문자 정규화
   - 중복 기사 제거 (URL 기준)
   - `articles`(is_processed=0) → 정제 후 is_processed=1 업데이트

2. **기술 키워드 추출**
   - `technologies` 테이블 기반 사전 매칭 (200+ 기술명)
   - `article_technologies` 테이블에 언급 횟수 저장

3. **트렌드 통계 집계**
   - `trends` 테이블 월별 집계 upsert
   - 지난달 대비 변화율(change_rate) 계산

### 산출물
- `data-pipeline/processors/cleaner.py`
- `data-pipeline/processors/keyword_extractor.py`
- `data-pipeline/processors/stats_aggregator.py`
- `backend/app/models/*.py`

### 완료 기준
- 수집 데이터 100건 이상 MySQL 저장 확인

---

## 🟦 5단계 — 벡터 임베딩 & Chroma 저장

### 목표
정제된 문서를 Gemini 임베딩으로 변환하여 Chroma 벡터 DB에 저장합니다.

### 작업 내역
1. **임베딩 파이프라인 구현**
   - LangChain `GoogleGenerativeAIEmbeddings` (`models/embedding-001`)
   - `RecursiveCharacterTextSplitter` (chunk_size=500, overlap=50)
   - `articles`(is_embedded=0) 기사 배치 처리
   - 임베딩 완료 후 `is_embedded=1` 업데이트

2. **Chroma 벡터 저장소 설정** (로컬 Persistent)
   - 컬렉션: `tech_news`, `github_repos`
   - 메타데이터: source, date, url, technologies

3. **증분 업데이트 로직**
   - 새로운 문서만 임베딩 추가 (article_id 기준 스킵)

### 산출물
- `data-pipeline/processors/embedder.py`
- `data-pipeline/processors/vector_store.py`

### 완료 기준
- Chroma에 1,000건 이상 문서 벡터 저장 확인
- 유사 문서 검색 응답 시간 < 500ms

---

## 🟦 6단계 — FastAPI 백엔드 & RAG 챗봇

### 목표
프론트엔드에 실제 데이터를 제공하는 REST API와 Gemini 기반 RAG 챗봇을 구현합니다.

### 작업 내역
1. **FastAPI 앱 구조 설정**
   - 라우터 분리: `/trends`, `/articles`, `/chat`, `/admin`
   - SQLAlchemy 세션 설정, Pydantic 스키마 정의

2. **트렌드 & 뉴스 API**
   - `GET /trends/heatmap`, `GET /trends/top5`, `GET /trends/timeline`
   - `GET /articles`, `GET /articles/{id}`, `GET /articles/search`

3. **RAG 챗봇 파이프라인**
   - LangChain `GoogleGenerativeAIEmbeddings` + Chroma 리트리버
   - `gemini-2.0-flash` LLM 연결
   - Langflow 플로우 구성 및 JSON 저장
   - `POST /chat/sessions/{id}/messages` (SSE 스트리밍)

4. **관리 & 헬스체크 API**
   - `POST /admin/collect`, `POST /admin/embed`, `GET /health`

### 산출물
- `backend/app/api/*.py` (trends, articles, chat, admin)
- `backend/app/services/rag_service.py`
- `langflow/flows/rag_chat_flow.json`

### 완료 기준
- Swagger UI (`/docs`)에서 모든 엔드포인트 동작 확인
- "이번 달 가장 핫한 기술은?" 질문에 Gemini 기반 답변 확인

---

## 🟦 7단계 — 프론트엔드 실제 API 연결

### 목표
2단계에서 Mock 데이터로 완성한 UI를 **실제 FastAPI 엔드포인트**에 연결합니다.

### 작업 내역
1. **Mock → 실제 API 교체**
   - `frontend/src/mocks/` → `frontend/src/api/` 훅으로 전환
   - TanStack Query 훅에서 실제 axios 요청으로 연결
   - 히트맵, Top5, 타임라인, 뉴스 목록, 챗봇 순서로 연결

2. **SSE 스트리밍 챗봇 연결**
   - `EventSource` 또는 `fetch` ReadableStream으로 실시간 응답 수신
   - 기존 시뮬레이션 코드 → 실제 스트리밍으로 교체

3. **전체 흐름 통합 테스트**
   - 데이터 수집 → MySQL → API → 프론트 렌더링 E2E 확인
   - RAG 챗봇 질문 → 스트리밍 응답 확인

### 산출물
- `frontend/src/api/*.ts` (trends, articles, chat)
- 업데이트된 `frontend/src/hooks/*.ts`

### 완료 기준
- Mock 없이 실제 데이터로 전체 화면 정상 동작 확인
- 챗봇 스트리밍 응답 브라우저에서 확인
