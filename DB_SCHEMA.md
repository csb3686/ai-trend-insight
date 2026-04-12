# 🗄️ MySQL 테이블 설계 (DB_SCHEMA.md)

> AI 기술 트렌드 인사이트 플랫폼 — MySQL 8.0 정형 데이터 스키마 (로컬 직접 설치)

---

## ERD (텍스트)

```
sources ──────< articles >────── article_technologies >────── technologies
                   │                                                │
                   │                                               trends
                   │
              article_tags
```

---

## 테이블 목록

| 테이블명 | 설명 |
|----------|------|
| `sources` | 데이터 출처 (긱뉴스, HN, GitHub) |
| `articles` | 수집된 뉴스 기사 및 GitHub 저장소 |
| `technologies` | 기술 키워드 마스터 테이블 |
| `article_technologies` | 기사-기술 다:다 연결 테이블 |
| `trends` | 월별 기술 언급 집계 (트렌드 캐시) |

---

## 1. `sources` — 데이터 출처

```sql
CREATE TABLE sources (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL COMMENT '출처명 (긱뉴스, HackerNews, GitHub)',
    type        ENUM('rss', 'api', 'crawl') NOT NULL COMMENT '수집 방식',
    url         VARCHAR(500) NOT NULL COMMENT '원본 피드/API URL',
    is_active   TINYINT(1) DEFAULT 1 COMMENT '활성 여부',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY uq_source_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='데이터 수집 출처';
```

### 초기 데이터

```sql
INSERT INTO sources (name, type, url) VALUES
('긱뉴스', 'rss', 'https://news.hada.io/rss'),
('HackerNews', 'rss', 'https://hnrss.org/frontpage'),
('GitHub Trending', 'api', 'https://api.github.com/search/repositories');
```

---

## 2. `articles` — 수집된 뉴스 및 저장소

```sql
CREATE TABLE articles (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    source_id       INT UNSIGNED NOT NULL COMMENT '출처 FK',
    type            ENUM('news', 'github_repo') NOT NULL DEFAULT 'news',
    title           VARCHAR(500) NOT NULL COMMENT '제목',
    url             VARCHAR(1000) NOT NULL COMMENT '원본 URL',
    description     TEXT COMMENT '요약/설명',
    content         LONGTEXT COMMENT '전문 (크롤링 시)',
    author          VARCHAR(200) COMMENT '작성자',
    published_at    DATETIME COMMENT '원본 발행 일시',
    
    -- GitHub 전용 필드
    github_stars    INT UNSIGNED COMMENT 'GitHub Stars 수',
    github_language VARCHAR(100) COMMENT '주요 프로그래밍 언어',
    github_forks    INT UNSIGNED COMMENT 'Fork 수',
    
    -- 처리 상태
    is_processed    TINYINT(1) DEFAULT 0 COMMENT '정제 완료 여부',
    is_embedded     TINYINT(1) DEFAULT 0 COMMENT '벡터 임베딩 완료 여부',
    
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (source_id) REFERENCES sources(id) ON DELETE CASCADE,
    
    UNIQUE KEY uq_article_url (url(255)),
    INDEX idx_published_at (published_at),
    INDEX idx_source_id (source_id),
    INDEX idx_is_embedded (is_embedded),
    INDEX idx_type (type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='수집된 기사 및 GitHub 저장소';
```

---

## 3. `technologies` — 기술 키워드 마스터

```sql
CREATE TABLE technologies (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL COMMENT '기술명 (Python, React, k8s 등)',
    category    ENUM(
                    'language',     -- 프로그래밍 언어
                    'framework',    -- 프레임워크
                    'database',     -- 데이터베이스
                    'devops',       -- DevOps/인프라
                    'ai_ml',        -- AI/ML
                    'cloud',        -- 클라우드
                    'tool',         -- 개발 도구
                    'other'         -- 기타
                ) NOT NULL DEFAULT 'other',
    aliases     JSON COMMENT '별칭 목록 (["k8s", "Kubernetes"])',
    description VARCHAR(500) COMMENT '기술 설명',
    is_active   TINYINT(1) DEFAULT 1 COMMENT '추적 활성 여부',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY uq_tech_name (name),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='기술 키워드 마스터 테이블';
```

### 초기 데이터 예시

```sql
INSERT INTO technologies (name, category, aliases) VALUES
('Python', 'language', '["python3", "py"]'),
('JavaScript', 'language', '["JS", "js", "ECMAScript"]'),
('TypeScript', 'language', '["TS", "ts"]'),
('Rust', 'language', '["rust-lang"]'),
('Go', 'language', '["Golang", "golang"]'),
('React', 'framework', '["ReactJS", "React.js"]'),
('Next.js', 'framework', '["NextJS", "next"]'),
('FastAPI', 'framework', '["fast-api"]'),
('LangChain', 'ai_ml', '["langchain"]'),
('LLM', 'ai_ml', '["Large Language Model", "대형언어모델"]'),
('Gemini', 'ai_ml', '["gemini-2.0-flash", "Gemini API", "Google AI"]'),
('Kubernetes', 'devops', '["k8s", "K8s"]'),
('Docker', 'devops', '["docker-compose"]'),
('PostgreSQL', 'database', '["Postgres", "pg"]'),
('MySQL', 'database', '["mysql8"]'),
('Redis', 'database', '["redis-server"]'),
('AWS', 'cloud', '["Amazon Web Services"]'),
('GCP', 'cloud', '["Google Cloud"]'),
('Terraform', 'devops', '["tf"]'),
('GitHub Actions', 'devops', '["GHA"]');
```

---

## 4. `article_technologies` — 기사-기술 연결

```sql
CREATE TABLE article_technologies (
    id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    article_id  BIGINT UNSIGNED NOT NULL COMMENT '기사 FK',
    tech_id     INT UNSIGNED NOT NULL COMMENT '기술 FK',
    mention_count INT UNSIGNED DEFAULT 1 COMMENT '해당 기사 내 언급 횟수',
    
    -- 언급 위치
    in_title    TINYINT(1) DEFAULT 0 COMMENT '제목에서 언급',
    in_content  TINYINT(1) DEFAULT 0 COMMENT '본문에서 언급',
    
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
    FOREIGN KEY (tech_id) REFERENCES technologies(id) ON DELETE CASCADE,
    
    UNIQUE KEY uq_article_tech (article_id, tech_id),
    INDEX idx_tech_id (tech_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='기사-기술 다대다 연결';
```

---

## 5. `trends` — 월별 기술 트렌드 집계

```sql
CREATE TABLE trends (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    tech_id         INT UNSIGNED NOT NULL COMMENT '기술 FK',
    year            SMALLINT UNSIGNED NOT NULL COMMENT '연도 (2025)',
    month           TINYINT UNSIGNED NOT NULL COMMENT '월 (1~12)',
    
    -- 집계 데이터
    mention_count   INT UNSIGNED DEFAULT 0 COMMENT '해당 월 전체 언급 수',
    article_count   INT UNSIGNED DEFAULT 0 COMMENT '언급된 기사 수',
    
    -- 변화율 (지난달 대비)
    prev_month_count   INT UNSIGNED DEFAULT 0 COMMENT '전월 언급 수',
    change_rate        DECIMAL(8, 2) COMMENT '변화율 % (+는 증가, -는 감소)',
    
    -- 순위
    rank_current    INT UNSIGNED COMMENT '이번달 순위',
    rank_prev       INT UNSIGNED COMMENT '전월 순위',
    
    last_updated    DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (tech_id) REFERENCES technologies(id) ON DELETE CASCADE,
    
    UNIQUE KEY uq_trend_tech_month (tech_id, year, month),
    INDEX idx_year_month (year, month),
    INDEX idx_change_rate (change_rate)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='월별 기술 트렌드 집계';
```

---

## 6. 주요 쿼리 예시

### 히트맵 — 이번 달 기술 Top 10

```sql
SELECT 
    t.name AS tech_name,
    t.category,
    tr.mention_count,
    tr.article_count,
    tr.rank_current
FROM trends tr
JOIN technologies t ON tr.tech_id = t.id
WHERE tr.year = YEAR(NOW())
  AND tr.month = MONTH(NOW())
ORDER BY tr.mention_count DESC
LIMIT 10;
```

### Top 5 트렌드 — 지난달 대비 변화율

```sql
SELECT 
    t.name AS tech_name,
    tr.mention_count,
    tr.prev_month_count,
    tr.change_rate,
    tr.rank_current,
    tr.rank_prev
FROM trends tr
JOIN technologies t ON tr.tech_id = t.id
WHERE tr.year = YEAR(NOW())
  AND tr.month = MONTH(NOW())
  AND tr.prev_month_count > 0   -- 지난달 데이터 있는 것만
ORDER BY ABS(tr.change_rate) DESC
LIMIT 5;
```

### 월별 특정 기술 언급 추이

```sql
SELECT 
    tr.year,
    tr.month,
    tr.mention_count,
    tr.article_count,
    tr.change_rate
FROM trends tr
JOIN technologies t ON tr.tech_id = t.id
WHERE t.name = 'Python'
  AND tr.year >= YEAR(DATE_SUB(NOW(), INTERVAL 12 MONTH))
ORDER BY tr.year ASC, tr.month ASC;
```

### 트렌드 집계 갱신 (매일 실행)

```sql
-- trends 테이블 이번달 집계 갱신
INSERT INTO trends (tech_id, year, month, mention_count, article_count)
SELECT 
    at.tech_id,
    YEAR(a.published_at) AS year,
    MONTH(a.published_at) AS month,
    SUM(at.mention_count) AS mention_count,
    COUNT(DISTINCT at.article_id) AS article_count
FROM article_technologies at
JOIN articles a ON at.article_id = a.id
WHERE YEAR(a.published_at) = YEAR(NOW())
  AND MONTH(a.published_at) = MONTH(NOW())
GROUP BY at.tech_id, YEAR(a.published_at), MONTH(a.published_at)
ON DUPLICATE KEY UPDATE
    mention_count = VALUES(mention_count),
    article_count = VALUES(article_count),
    last_updated = NOW();
```

---

## 7. 인덱스 전략

| 쿼리 패턴 | 인덱스 |
|-----------|--------|
| 월별 트렌드 조회 | `trends(year, month)` |
| 기술별 트렌드 조회 | `trends(tech_id, year, month)` |
| 기사 발행일 범위 조회 | `articles(published_at)` |
| 중복 기사 체크 | `articles(url)` — UNIQUE |
| 기사-기술 집계 | `article_technologies(tech_id)` |

---

## 8. 데이터베이스 설정

> MySQL 8.0을 로컬에 직접 설치 후 아래 명령으로 초기화합니다.

```sql
-- 데이터베이스 생성
CREATE DATABASE ai_trend
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE ai_trend;

-- 타임존 설정 (한국 시간)
SET GLOBAL time_zone = '+09:00';
```

```bash
# 초기 스키마 적용 방법
mysql -u root -p < init.sql
```
