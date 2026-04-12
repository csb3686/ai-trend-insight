# 🤖 AI 기술 트렌드 인사이트 플랫폼

> 뉴스 + GitHub 트렌딩 데이터를 자동 수집·분석하고, RAG 기반으로 기술 트렌드를 탐색하는 플랫폼

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://react.dev/)

---

## 📌 프로젝트 개요

**AI 기술 트렌드 인사이트 플랫폼**은 긱뉴스 RSS, Hacker News RSS, GitHub API 등 다양한 데이터 소스에서 기술 트렌드 데이터를 자동 수집하고, 이를 분석·시각화하며 RAG(Retrieval-Augmented Generation) 기반 챗봇으로 자연어 질의응답을 제공하는 플랫폼입니다.

개발자와 기술 리더가 매달 변화하는 기술 생태계를 한눈에 파악하고, 구체적인 데이터를 근거로 의사결정을 내릴 수 있도록 돕습니다.

---

## ✨ 핵심 기능

### 1. 📊 기술 스택 히트맵
- 이번 달 가장 많이 언급된 기술 **Top 10** 히트맵 시각화
- 뉴스·GitHub 데이터를 통합하여 기술별 언급 빈도 집계
- 월별 트렌드 추이 차트 제공

### 2. 🤖 RAG 챗봇
- 수집된 뉴스 + GitHub 데이터 기반 벡터 검색
- LangChain + Chroma를 활용한 문서 임베딩 및 유사도 검색
- Langflow 기반 LLM 파이프라인으로 자연어 질의응답
- 답변 출처 원문 링크 제공

### 3. 📈 Top 5 트렌드 변화율
- 지난달 대비 기술 언급량 **변화율(%)** 계산
- 급상승/급하락 기술 자동 감지 및 강조 표시
- 트렌드 이유 AI 요약 제공

---

## 🛠️ 기술 스택

| 영역 | 기술 |
|------|------|
| **데이터 수집** | n8n (npm 로컬 실행), Playwright |
| **LLM** | Gemini 2.0 Flash (Google Gemini API) |
| **LLM 파이프라인** | Langflow + LangChain |
| **RAG / Vector DB** | LangChain + Chroma (로컬 설치) |
| **임베딩** | GoogleGenerativeAIEmbeddings (`models/embedding-001`) |
| **데이터 정제** | Pandas |
| **백엔드 API** | FastAPI (Python 3.11+) |
| **프론트엔드** | React 18 + Recharts |
| **정형 DB** | MySQL 8.0 (로컬 설치) |

---

## 📡 데이터 소스

| 소스 | 설명 | 수집 주기 |
|------|------|-----------|
| [긱뉴스](https://news.hada.io/) RSS | 국내 개발자 커뮤니티 뉴스 | 매일 06:00 |
| [Hacker News](https://news.ycombinator.com/) RSS | 글로벌 기술 커뮤니티 뉴스 | 매일 06:00 |
| [GitHub API](https://github.com/trending) | 트렌딩 저장소 | 매일 07:00 |

---

## 🏗️ 아키텍처 개요

```
[데이터 수집 - n8n]
  긱뉴스 RSS / HN RSS / GitHub API
         │
         ▼
[데이터 정제 - Pandas]
  텍스트 클렌징 · 기술 키워드 추출
         │
    ┌────┴────┐
    ▼         ▼
[MySQL]    [Chroma]
 정형 데이터   벡터 임베딩
    │         │
    └────┬────┘
         ▼
[FastAPI 백엔드]
  REST API 서빙
         │
         ▼
[React 프론트엔드]
  히트맵 · 챗봇 · 트렌드 대시보드
```

> 상세 아키텍처 → [ARCHITECTURE.md](./ARCHITECTURE.md)

---

## 📁 프로젝트 구조

```
automation-project/
├── backend/                  # FastAPI 백엔드
│   ├── app/
│   │   ├── api/             # 라우터 (뉴스, 트렌드, 챗봇)
│   │   ├── models/          # SQLAlchemy 모델
│   │   ├── schemas/         # Pydantic 스키마
│   │   ├── services/        # 비즈니스 로직
│   │   └── main.py
│   ├── requirements.txt
│
├── frontend/                 # React 프론트엔드
│   ├── src/
│   │   ├── components/      # 히트맵, 챗봇, 트렌드 컴포넌트
│   │   ├── pages/
│   │   └── App.jsx
│   ├── package.json
│
├── data-pipeline/            # 데이터 수집 · 정제
│   ├── crawlers/            # Playwright 크롤러
│   ├── processors/          # Pandas 정제 로직
│   └── n8n/                 # n8n 워크플로 JSON
│
├── langflow/                 # Langflow 파이프라인 설정
│   └── flows/
│
├── README.md
├── PLAN.md
├── ARCHITECTURE.md
├── DB_SCHEMA.md
├── API_SPEC.md
└── TODO.md
```

---

## 🚀 빠른 시작

### 사전 요구사항

- Python 3.11+
- Node.js 18+
- MySQL 8.0 (로컬 설치)
- n8n (`npm install -g n8n`)

### 환경 변수 설정

```bash
cp .env.example .env
# .env 파일에 아래 값 입력
# GITHUB_TOKEN=your_github_token
# GEMINI_API_KEY=your_gemini_api_key
# MYSQL_ROOT_PASSWORD=your_mysql_password
# MYSQL_DATABASE=ai_trend
```

### 실행

```bash
# 1. MySQL 로컬 서버 기동 (설치 후)
mysql -u root -p < init.sql

# 2. n8n 실행
n8n start

# 3. Langflow 실행
pip install langflow
langflow run

# 4. 백엔드 실행
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# 5. 프론트엔드 실행
cd frontend
npm install
npm run dev
```

### 접속 URL

| 서비스 | URL |
|--------|-----|
| 프론트엔드 | http://localhost:3000 |
| FastAPI Docs | http://localhost:8000/docs |
| n8n 워크플로 | http://localhost:5678 |
| Langflow | http://localhost:7860 |

---

## 📋 개발 계획

개발은 총 **7단계** MVP로 진행됩니다.

| 단계 | 내용 | 상태 |
|------|------|------|
| 1단계 | 환경 구성 & 로컬 서비스 설치 | 🔲 예정 |
| 2단계 | React 프론트엔드 개발 (Mock 데이터) | 🔲 예정 |
| 3단계 | 데이터 수집 파이프라인 | 🔲 예정 |
| 4단계 | 데이터 정제 & MySQL 저장 | 🔲 예정 |
| 5단계 | 벡터 임베딩 & Chroma 저장 | 🔲 예정 |
| 6단계 | FastAPI 백엔드 & RAG 챗봇 (Gemini) | 🔲 예정 |
| 7단계 | 프론트엔드 실제 API 연결 | 🔲 예정 |

> 상세 계획 → [PLAN.md](./PLAN.md)  
> 개발 체크리스트 → [TODO.md](./TODO.md)

---

## 📄 문서 목록

| 문서 | 설명 |
|------|------|
| [PLAN.md](./PLAN.md) | 단계별 개발 계획 |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | 전체 아키텍처 흐름도 |
| [DB_SCHEMA.md](./DB_SCHEMA.md) | MySQL 테이블 설계 |
| [API_SPEC.md](./API_SPEC.md) | FastAPI 엔드포인트 명세 |
| [TODO.md](./TODO.md) | 개발 순서 체크리스트 |

---

## 🤝 기여 방법

1. 이 저장소를 Fork합니다.
2. 기능 브랜치를 생성합니다: `git checkout -b feature/amazing-feature`
3. 변경사항을 커밋합니다: `git commit -m 'feat: add amazing feature'`
4. 브랜치에 Push합니다: `git push origin feature/amazing-feature`
5. Pull Request를 생성합니다.

---

## 📜 라이선스

이 프로젝트는 [MIT License](LICENSE)를 따릅니다.

---

<p align="center">Made with ❤️ for the developer community</p>
