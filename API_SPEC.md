# 📡 FastAPI 엔드포인트 명세 (API_SPEC.md)

> AI 기술 트렌드 인사이트 플랫폼 — REST API 설계 문서
> Base URL: `http://localhost:8000/api/v1`
> 인터랙티브 문서: `http://localhost:8000/docs` (Swagger UI)

---

## 목차

- [공통 규약](#공통-규약)
- [트렌드 API](#1-트렌드-api)
- [기사 API](#2-기사-api)
- [챗봇 API](#3-챗봇-api)
- [관리 API](#4-관리-api)
- [헬스체크](#5-헬스체크)
- [에러 코드](#에러-코드)

---

## 공통 규약

### 요청 헤더

```
Content-Type: application/json
Accept: application/json
X-API-Key: {api_key}          ← 인증이 필요한 엔드포인트만
```

### 성공 응답 형식

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "total": 100,
    "page": 1,
    "per_page": 20
  }
}
```

### 에러 응답 형식

```json
{
  "success": false,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "요청한 리소스를 찾을 수 없습니다.",
    "detail": "article_id=999 not found"
  }
}
```

### 날짜 형식
- 모든 날짜/시간: **ISO 8601** (`2025-01-15T09:30:00+09:00`)
- 날짜만: `YYYY-MM-DD`

---

## 1. 트렌드 API

### 1-1. 히트맵 데이터 조회

기술 키워드별 언급 횟수를 히트맵 형태로 반환합니다.

```
GET /trends/heatmap
```

**쿼리 파라미터**

| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|----------|------|------|--------|------|
| `period` | string | ❌ | `monthly` | `daily` \| `weekly` \| `monthly` |
| `year` | int | ❌ | 현재년도 | 조회 연도 |
| `month` | int | ❌ | 현재월 | 조회 월 (1~12) |
| `category` | string | ❌ | `all` | `ai_ml` \| `frontend` \| `backend` \| `devops` \| `all` |
| `source` | string | ❌ | `all` | `geek_news` \| `hacker_news` \| `github` \| `all` |
| `limit` | int | ❌ | `10` | 반환할 키워드 수 (최대 50) |

**응답 예시**

```json
{
  "success": true,
  "data": {
    "period": "monthly",
    "year": 2025,
    "month": 1,
    "items": [
      {
        "rank": 1,
        "keyword": "LangChain",
        "category": "ai_ml",
        "mention_count": 342,
        "article_count": 87,
        "intensity": 1.0
      },
      {
        "rank": 2,
        "keyword": "React",
        "category": "frontend",
        "mention_count": 289,
        "article_count": 104,
        "intensity": 0.84
      }
    ]
  }
}
```

> `intensity`: 1위 대비 상대 강도 (0.0 ~ 1.0, 히트맵 색상 강도에 사용)

---

### 1-2. Top 5 트렌드 (변화율)

지난 기간 대비 언급 증가/감소율 기준 Top 5를 반환합니다.

```
GET /trends/top5
```

**쿼리 파라미터**

| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|----------|------|------|--------|------|
| `period` | string | ❌ | `monthly` | `weekly` \| `monthly` |
| `direction` | string | ❌ | `rising` | `rising` (상승) \| `falling` (하락) |

**응답 예시**

```json
{
  "success": true,
  "data": {
    "period": "monthly",
    "direction": "rising",
    "compared_to": "2024-12",
    "items": [
      {
        "rank": 1,
        "keyword": "Rust",
        "category": "language",
        "current_count": 156,
        "previous_count": 72,
        "change_rate": 116.67,
        "trend": "rising"
      }
    ]
  }
}
```

---

### 1-3. 시계열 데이터

특정 기술의 시간대별 언급 추이를 반환합니다.

```
GET /trends/timeline
```

**쿼리 파라미터**

| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|----------|------|------|--------|------|
| `keywords` | string | ✅ | - | 쉼표 구분 키워드 (예: `React,Vue,Svelte`) |
| `period` | string | ❌ | `daily` | `daily` \| `weekly` \| `monthly` |
| `start_date` | string | ❌ | 30일 전 | `YYYY-MM-DD` |
| `end_date` | string | ❌ | 오늘 | `YYYY-MM-DD` |

**응답 예시**

```json
{
  "success": true,
  "data": {
    "period": "daily",
    "series": [
      {
        "keyword": "React",
        "category": "frontend",
        "data": [
          { "date": "2025-01-01", "count": 23 },
          { "date": "2025-01-02", "count": 31 }
        ]
      }
    ]
  }
}
```

---

### 1-4. 키워드 목록 조회

등록된 기술 키워드 전체 목록을 반환합니다.

```
GET /trends/keywords
```

**쿼리 파라미터**

| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|----------|------|------|--------|------|
| `category` | string | ❌ | `all` | 카테고리 필터 |
| `active_only` | bool | ❌ | `true` | 활성 키워드만 |

**응답 예시**

```json
{
  "success": true,
  "data": {
    "total": 42,
    "items": [
      {
        "id": 1,
        "keyword": "React",
        "category": "frontend",
        "aliases": ["reactjs", "react.js", "리액트"],
        "is_active": true
      }
    ]
  }
}
```

---

## 2. 기사 API

### 2-1. 기사 목록 조회

```
GET /articles
```

**쿼리 파라미터**

| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|----------|------|------|--------|------|
| `page` | int | ❌ | `1` | 페이지 번호 |
| `per_page` | int | ❌ | `20` | 페이지당 항목 수 (최대 100) |
| `source` | string | ❌ | `all` | `geek_news` \| `hacker_news` \| `github` \| `all` |
| `keyword` | string | ❌ | - | 기술 키워드 필터 |
| `start_date` | string | ❌ | - | 시작일 (`YYYY-MM-DD`) |
| `end_date` | string | ❌ | - | 종료일 (`YYYY-MM-DD`) |
| `sort` | string | ❌ | `published_at` | 정렬 기준 |
| `order` | string | ❌ | `desc` | `asc` \| `desc` |

**응답 예시**

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 1234,
        "source": "geek_news",
        "title": "LangChain v0.2 릴리스: 멀티모달 RAG 지원",
        "url": "https://...",
        "summary": "LangChain 새 버전이 ...",
        "published_at": "2025-01-15T09:00:00+09:00",
        "keywords_detected": ["LangChain", "RAG", "Python"]
      }
    ]
  },
  "meta": {
    "total": 4823,
    "page": 1,
    "per_page": 20,
    "total_pages": 242
  }
}
```

---

### 2-2. 기사 상세 조회

```
GET /articles/{article_id}
```

**경로 파라미터**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| `article_id` | int | 기사 ID |

**응답 예시**

```json
{
  "success": true,
  "data": {
    "id": 1234,
    "source": "geek_news",
    "title": "LangChain v0.2 릴리스",
    "url": "https://...",
    "clean_content": "LangChain 팀이 ...",
    "language": "ko",
    "published_at": "2025-01-15T09:00:00+09:00",
    "keywords_detected": ["LangChain", "RAG", "Python"],
    "is_embedded": true
  }
}
```

---

### 2-3. 기사 검색

```
GET /articles/search
```

**쿼리 파라미터**

| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| `q` | string | ✅ | 검색어 |
| `page` | int | ❌ | 페이지 번호 |
| `per_page` | int | ❌ | 페이지당 수 |

---

## 3. 챗봇 API

### 3-1. 새 대화 세션 생성

```
POST /chat/sessions
```

**요청 본문**

```json
{
  "initial_message": "요즘 Rust가 왜 인기 있어?"  // 선택
}
```

**응답 예시**

```json
{
  "success": true,
  "data": {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2025-01-15T09:00:00+09:00"
  }
}
```

---

### 3-2. 질문 전송 (RAG 응답, 스트리밍)

```
POST /chat/sessions/{session_id}/messages
Content-Type: application/json
Accept: text/event-stream          ← 스트리밍 요청 시
```

**경로 파라미터**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| `session_id` | string (UUID) | 세션 ID |

**요청 본문**

```json
{
  "message": "요즘 Rust가 왜 인기가 많아?",
  "stream": true
}
```

**스트리밍 응답 (SSE)**

```
data: {"type": "token", "content": "Rust는"}
data: {"type": "token", "content": " 메모리"}
data: {"type": "token", "content": " 안전성과"}
...
data: {"type": "sources", "items": [{"id": 123, "title": "...", "url": "..."}]}
data: {"type": "done", "tokens_used": 412}
```

**비스트리밍 응답**

```json
{
  "success": true,
  "data": {
    "message_id": 5678,
    "role": "assistant",
    "content": "Rust는 메모리 안전성과 고성능을 동시에 보장하기 때문에 ...",
    "sources": [
      {
        "id": 1234,
        "title": "Why Rust is taking over systems programming",
        "url": "https://..."
      }
    ],
    "tokens_used": 412,
    "created_at": "2025-01-15T09:00:05+09:00"
  }
}
```

---

### 3-3. 대화 이력 조회

```
GET /chat/sessions/{session_id}/messages
```

**응답 예시**

```json
{
  "success": true,
  "data": {
    "session_id": "550e8400-...",
    "messages": [
      {
        "id": 5677,
        "role": "user",
        "content": "요즘 Rust가 왜 인기 있어?",
        "created_at": "2025-01-15T09:00:00+09:00"
      },
      {
        "id": 5678,
        "role": "assistant",
        "content": "Rust는 ...",
        "sources": [...],
        "created_at": "2025-01-15T09:00:05+09:00"
      }
    ]
  }
}
```

---

### 3-4. 세션 목록 조회

```
GET /chat/sessions
```

**쿼리 파라미터**

| 파라미터 | 타입 | 기본값 | 설명 |
|----------|------|--------|------|
| `page` | int | `1` | 페이지 번호 |
| `per_page` | int | `20` | 페이지당 수 |

---

### 3-5. 세션 삭제

```
DELETE /chat/sessions/{session_id}
```

**응답**

```json
{
  "success": true,
  "data": { "deleted": true }
}
```

---

## 4. 관리 API

> 모든 관리 API는 `X-API-Key` 헤더 인증 필요

### 4-1. 데이터 수집 수동 트리거

```
POST /admin/collect
```

**요청 본문**

```json
{
  "source": "geek_news",   // "geek_news" | "hacker_news" | "github" | "all"
  "force": false           // true: 이미 수집된 데이터도 재수집
}
```

**응답 예시**

```json
{
  "success": true,
  "data": {
    "log_id": 42,
    "source": "geek_news",
    "status": "started",
    "started_at": "2025-01-15T09:00:00+09:00"
  }
}
```

---

### 4-2. 임베딩 수동 트리거

```
POST /admin/embed
```

**요청 본문**

```json
{
  "force_reembed": false,   // true: 이미 임베딩된 기사도 재처리
  "limit": 100              // 이번 실행에서 처리할 최대 기사 수
}
```

---

### 4-3. 트렌드 통계 재집계

```
POST /admin/recompute-stats
```

**요청 본문**

```json
{
  "target_month": "2025-01"   // YYYY-MM, null이면 이번 달
}
```

---

### 4-4. 수집 이력 조회

```
GET /admin/collection-logs
```

**쿼리 파라미터**

| 파라미터 | 타입 | 기본값 | 설명 |
|----------|------|--------|------|
| `source` | string | `all` | 소스 필터 |
| `status` | string | `all` | `started` \| `success` \| `failed` |
| `page` | int | `1` | 페이지 번호 |
| `limit` | int | `50` | 최대 항목 수 |

---

## 5. 헬스체크

### 5-1. 기본 헬스체크

```
GET /health
```

**응답**

```json
{
  "status": "ok",
  "version": "1.0.0",
  "timestamp": "2025-01-15T09:00:00+09:00"
}
```

### 5-2. 상세 헬스체크

```
GET /health/detail
```

**응답**

```json
{
  "status": "ok",
  "services": {
    "mysql": { "status": "ok", "latency_ms": 3 },
    "chroma": { "status": "ok", "latency_ms": 12 },
    "gemini": { "status": "ok", "latency_ms": 245 }
  },
  "stats": {
    "total_articles": 12483,
    "embedded_articles": 12100,
    "last_collection": "2025-01-15T08:00:00+09:00"
  }
}
```

---

## 에러 코드

| HTTP 상태 | 에러 코드 | 설명 |
|-----------|-----------|------|
| 400 | `INVALID_PARAMS` | 요청 파라미터 형식 오류 |
| 401 | `UNAUTHORIZED` | API 키 누락/무효 |
| 404 | `RESOURCE_NOT_FOUND` | 요청한 리소스 없음 |
| 422 | `VALIDATION_ERROR` | Pydantic 유효성 검사 실패 |
| 429 | `RATE_LIMIT_EXCEEDED` | API 호출 제한 초과 |
| 500 | `INTERNAL_ERROR` | 서버 내부 오류 |
| 503 | `SERVICE_UNAVAILABLE` | 의존 서비스 불가 (DB, Gemini API 등) |

---

## 엔드포인트 요약

| 메서드 | 경로 | 설명 | 인증 |
|--------|------|------|------|
| GET | `/trends/heatmap` | 히트맵 데이터 | ❌ |
| GET | `/trends/top5` | Top 5 변화율 | ❌ |
| GET | `/trends/timeline` | 시계열 데이터 | ❌ |
| GET | `/trends/keywords` | 키워드 목록 | ❌ |
| GET | `/articles` | 기사 목록 | ❌ |
| GET | `/articles/{id}` | 기사 상세 | ❌ |
| GET | `/articles/search` | 기사 검색 | ❌ |
| POST | `/chat/sessions` | 세션 생성 | ❌ |
| POST | `/chat/sessions/{id}/messages` | 질문 (RAG) | ❌ |
| GET | `/chat/sessions/{id}/messages` | 대화 이력 | ❌ |
| GET | `/chat/sessions` | 세션 목록 | ❌ |
| DELETE | `/chat/sessions/{id}` | 세션 삭제 | ❌ |
| POST | `/admin/collect` | 수동 수집 | ✅ |
| POST | `/admin/embed` | 수동 임베딩 | ✅ |
| POST | `/admin/recompute-stats` | 통계 재집계 | ✅ |
| GET | `/admin/collection-logs` | 수집 이력 | ✅ |
| GET | `/health` | 헬스체크 | ❌ |
| GET | `/health/detail` | 상세 헬스체크 | ✅ |
