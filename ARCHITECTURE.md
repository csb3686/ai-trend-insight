# 🏗️ 전체 아키텍처 흐름도 (ARCHITECTURE.md)

> AI 기술 트렌드 인사이트 플랫폼의 시스템 구성 요소와 데이터 흐름을 설명합니다.  
> **모든 서비스는 Docker 없이 로컬에 직접 설치하여 실행합니다.**

---

## 1. 전체 시스템 구성도

```
┌─────────────────────────────────────────────────────────────────┐
│                        외부 데이터 소스                           │
│   [긱뉴스 RSS]   [Hacker News RSS]   [GitHub Trending API]      │
└────────┬───────────────┬──────────────────┬──────────────────────┘
         │               │                  │
         ▼               ▼                  ▼
┌─────────────────────────────────────────────────────────────────┐
│             데이터 수집 레이어 (n8n — npm 로컬 실행)              │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ RSS 수집 Flow│  │ RSS 수집 Flow│  │   GitHub API Flow    │  │
│  │  (긱뉴스)    │  │  (HN)        │  │  (Playwright 보조)   │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
│         └──────────────────┴──────────────────────┘             │
│                            │                                     │
│                    HTTP POST /ingest                             │
└────────────────────────────┼────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   데이터 처리 레이어                               │
│                                                                  │
│   [FastAPI /ingest 엔드포인트]                                    │
│           │                                                      │
│           ▼                                                      │
│   ┌───────────────┐                                              │
│   │ Pandas 정제   │  ← HTML 제거, 중복 제거, 기술 키워드 추출     │
│   └───────┬───────┘                                              │
│           │                                                      │
│     ┌─────┴──────┐                                               │
│     ▼            ▼                                               │
│  [MySQL]      [GoogleGenerativeAI Embedder]                      │
│  정형 저장    (models/embedding-001)                              │
│                  ▼                                               │
│             [Chroma DB]                                          │
│             벡터 저장 (로컬 Persistent)                           │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   백엔드 API 레이어 (FastAPI)                     │
│                                                                  │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │                  REST API Endpoints                       │  │
│   │                                                          │  │
│   │  GET  /api/v1/trends/heatmap   → MySQL 집계 쿼리         │  │
│   │  GET  /api/v1/trends/top5      → MySQL 변화율 계산        │  │
│   │  GET  /api/v1/trends/monthly   → MySQL 월별 데이터        │  │
│   │  GET  /api/v1/news             → MySQL 뉴스 목록          │  │
│   │  POST /api/v1/chat             → Langflow RAG 파이프라인  │  │
│   │  POST /api/v1/ingest/news      → 데이터 수신 및 처리      │  │
│   └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │         RAG 서비스 (LangChain + Langflow + Gemini)        │  │
│   │                                                          │  │
│   │  질문 입력                                                │  │
│   │     → 임베딩 변환 (GoogleGenerativeAIEmbeddings)          │  │
│   │     → Chroma 유사도 검색 (Top-K 문서)                    │  │
│   │     → 컨텍스트 조합                                       │  │
│   │     → LLM 답변 생성 (gemini-2.0-flash)                   │  │
│   │     → 출처 URL 포함 답변 반환                              │  │
│   └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   프론트엔드 레이어 (React)                        │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  대시보드     │  │  RAG 챗봇    │  │  월별 트렌드 차트     │  │
│  │  (히트맵 +   │  │  채팅 UI     │  │  (라인 차트)         │  │
│  │   Top5 카드) │  │              │  │                      │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│                                                                  │
│                      http://localhost:3000                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. 데이터 흐름 상세

### 2-1. 데이터 수집 흐름

```
[Cron: 매일 06:00]
      │
      ├─→ n8n (npm 로컬): 긱뉴스 RSS 파싱
      │         → HTTP GET https://news.hada.io/rss
      │         → XML 파싱 (title, link, pubDate, description)
      │         → HTTP POST http://localhost:8000/api/v1/ingest/news
      │
      ├─→ n8n (npm 로컬): Hacker News RSS 파싱
      │         → HTTP GET https://hnrss.org/frontpage
      │         → XML 파싱
      │         → HTTP POST http://localhost:8000/api/v1/ingest/news
      │
      └─→ n8n (npm 로컬): GitHub Trending API (07:00)
                → HTTP GET https://api.github.com/search/repositories
                  ?q=created:>2025-01-01&sort=stars&order=desc
                → repo name, description, language, stars 추출
                → HTTP POST http://localhost:8000/api/v1/ingest/github
```

### 2-2. 데이터 처리 흐름

```
[FastAPI /ingest 수신]
      │
      ▼
[Pandas 전처리]
  1. HTML 태그 제거 (BeautifulSoup)
  2. 특수문자 정규화
  3. URL 기반 중복 체크 (MySQL 조회)
  4. 기술 키워드 추출
     - tech_dictionary.yaml 로드 (200+ 기술명)
     - 제목 + 본문에서 키워드 매칭
     - 매칭된 기술명 목록 및 횟수 집계
      │
      ├─→ [MySQL 저장] (로컬 MySQL 8.0)
      │     - articles 테이블 INSERT
      │     - article_technologies 테이블 INSERT (다:다 관계)
      │     - trends 테이블 월별 집계 갱신
      │
      └─→ [LangChain 임베딩]
            - 청킹: RecursiveCharacterTextSplitter
              (chunk_size=500, chunk_overlap=50)
            - 임베딩: GoogleGenerativeAIEmbeddings (models/embedding-001)
            - Chroma 저장 (로컬 Persistent, 컬렉션: tech_news / github_repos)
            - 메타데이터: {article_id, source, date, url, technologies}
```

### 2-3. RAG 챗봇 흐름

```
[사용자 질문 입력]
      │
      ▼
[FastAPI POST /api/v1/chat]
      │
      ▼
[Langflow RAG 파이프라인 (localhost:7860)]
      │
      ├─ 1. 질문 임베딩 (GoogleGenerativeAIEmbeddings)
      │
      ├─ 2. Chroma 유사도 검색
      │      - 컬렉션: tech_news + github_repos
      │      - Top-K: 5개 문서 반환
      │      - 메타데이터 필터 (날짜 범위 선택 가능)
      │
      ├─ 3. 컨텍스트 프롬프트 조합
      │      System: "당신은 기술 트렌드 분석 전문가입니다..."
      │      Context: [검색된 5개 문서 내용]
      │      Question: [사용자 질문]
      │
      ├─ 4. LLM 답변 생성 (gemini-2.0-flash)
      │
      └─ 5. 응답 반환 (SSE 스트리밍)
             - answer: "..."
             - sources: [{title, url, date}, ...]
```

### 2-4. 트렌드 집계 흐름

```
[스케줄: 매일 00:00 또는 수집 후]
      │
      ▼
[MySQL 집계 쿼리]
      │
      ├─ 이번 달 기술 언급 수 집계 (히트맵)
      │    SELECT t.name, COUNT(*) as count
      │    FROM article_technologies at
      │    JOIN technologies t ON at.tech_id = t.id
      │    WHERE YEAR(at.created_at) = YEAR(NOW())
      │      AND MONTH(at.created_at) = MONTH(NOW())
      │    GROUP BY t.name ORDER BY count DESC LIMIT 10
      │
      └─ 지난달 대비 변화율 집계 (Top5 트렌드)
           이번달 count - 지난달 count / 지난달 count * 100
           → trends 테이블 갱신
```

---

## 3. 로컬 서비스 구성 (Docker 미사용)

```
로컬 머신 (localhost)
│
├── MySQL 8.0                  port: 3306  (로컬 직접 설치)
│     데이터 경로: OS 기본 MySQL 데이터 디렉토리
│
├── Chroma (chromadb)          port: 8001  (pip install chromadb)
│     데이터 경로: ./chroma-data/
│
├── n8n                        port: 5678  (npm install -g n8n)
│     실행: n8n start
│     데이터: ~/.n8n/
│
├── Langflow                   port: 7860  (pip install langflow)
│     실행: langflow run
│
├── FastAPI (backend)          port: 8000  (uvicorn)
│     실행: uvicorn app.main:app --reload
│
└── React (frontend)           port: 3000  (npm run dev)
      실행: npm run dev
```

---

## 4. 접속 URL 목록

| 서비스 | URL | 실행 방법 |
|--------|-----|-----------|
| 프론트엔드 | http://localhost:3000 | `npm run dev` |
| FastAPI Docs | http://localhost:8000/docs | `uvicorn app.main:app --reload` |
| n8n 워크플로 | http://localhost:5678 | `n8n start` |
| Langflow | http://localhost:7860 | `langflow run` |
| Chroma | http://localhost:8001 | `chromadb run` |

---

## 5. 기술 선택 이유

| 기술 | 선택 이유 |
|------|-----------|
| **n8n (npm)** | 노코드 워크플로, Docker 없이 npm으로 로컬 실행 가능, RSS/HTTP 노드 내장 |
| **Gemini 2.0 Flash** | Google Gemini API 무료 할당량 활용, 빠른 응답 속도, 한국어 지원 우수 |
| **GoogleGenerativeAIEmbeddings** | Gemini 임베딩 모델 (`models/embedding-001`), GEMINI_API_KEY 단일 키 관리 |
| **Langflow** | LangChain 파이프라인을 시각적으로 구성, JSON으로 버전 관리 |
| **Chroma** | 경량 벡터 DB, Python 네이티브, 로컬 Persistent 모드 지원 |
| **FastAPI** | 비동기 지원, 자동 Swagger 문서, Pydantic 타입 안전성 |
| **MySQL** | 집계 쿼리와 관계형 데이터에 최적, 트렌드 통계 계산에 적합 |
| **React + Recharts** | 빠른 UI 개발, Recharts로 히트맵·라인 차트 쉽게 구현 |
