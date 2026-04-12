-- ============================================================
-- AI 기술 트렌드 인사이트 플랫폼 — MySQL 초기화 스크립트
-- 실행 방법: mysql -u root -p ai_trend < init.sql
-- ============================================================

USE ai_trend;

-- 타임존 설정 (한국 시간)
SET time_zone = '+09:00';

-- ============================================================
-- 1. sources — 데이터 수집 출처
-- ============================================================
CREATE TABLE IF NOT EXISTS sources (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL COMMENT '출처명 (긱뉴스, HackerNews, GitHub)',
    type        ENUM('rss', 'api', 'crawl') NOT NULL COMMENT '수집 방식',
    url         VARCHAR(500) NOT NULL COMMENT '원본 피드/API URL',
    is_active   TINYINT(1) DEFAULT 1 COMMENT '활성 여부',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY uq_source_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='데이터 수집 출처';

-- 초기 데이터
INSERT INTO sources (name, type, url) VALUES
('긱뉴스',         'rss', 'https://news.hada.io/rss'),
('HackerNews',     'rss', 'https://hnrss.org/frontpage'),
('GitHub Trending','api', 'https://api.github.com/search/repositories');

-- ============================================================
-- 2. articles — 수집된 뉴스 및 GitHub 저장소
-- ============================================================
CREATE TABLE IF NOT EXISTS articles (
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

-- ============================================================
-- 3. technologies — 기술 키워드 마스터
-- ============================================================
CREATE TABLE IF NOT EXISTS technologies (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL COMMENT '기술명',
    category    ENUM('language','framework','database','devops','ai_ml','cloud','tool','other')
                NOT NULL DEFAULT 'other',
    aliases     JSON COMMENT '별칭 목록 (["k8s", "Kubernetes"])',
    description VARCHAR(500) COMMENT '기술 설명',
    is_active   TINYINT(1) DEFAULT 1 COMMENT '추적 활성 여부',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY uq_tech_name (name),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='기술 키워드 마스터 테이블';

-- 초기 기술 키워드 데이터
INSERT INTO technologies (name, category, aliases) VALUES
('Python',         'language',  '["python3", "py"]'),
('JavaScript',     'language',  '["JS", "js", "ECMAScript"]'),
('TypeScript',     'language',  '["TS", "ts"]'),
('Rust',           'language',  '["rust-lang"]'),
('Go',             'language',  '["Golang", "golang"]'),
('Java',           'language',  '["java8", "java11", "java17"]'),
('C++',            'language',  '["cpp", "c-plus-plus"]'),
('React',          'framework', '["ReactJS", "React.js"]'),
('Next.js',        'framework', '["NextJS", "next"]'),
('Vue',            'framework', '["Vue.js", "VueJS"]'),
('FastAPI',        'framework', '["fast-api"]'),
('Django',         'framework', '["django-rest"]'),
('Spring',         'framework', '["SpringBoot", "Spring Boot"]'),
('LangChain',      'ai_ml',     '["langchain"]'),
('LLM',            'ai_ml',     '["Large Language Model", "대형언어모델"]'),
('Gemini',         'ai_ml',     '["gemini-2.0-flash", "Google AI"]'),
('RAG',            'ai_ml',     '["Retrieval Augmented Generation"]'),
('Kubernetes',     'devops',    '["k8s", "K8s"]'),
('Docker',         'devops',    '["docker-compose", "container"]'),
('PostgreSQL',     'database',  '["Postgres", "pg"]'),
('MySQL',          'database',  '["mysql8"]'),
('Redis',          'database',  '["redis-server"]'),
('MongoDB',        'database',  '["mongo"]'),
('AWS',            'cloud',     '["Amazon Web Services", "EC2", "S3"]'),
('GCP',            'cloud',     '["Google Cloud", "BigQuery"]'),
('Terraform',      'devops',    '["tf", "IaC"]'),
('GitHub Actions', 'devops',    '["GHA", "CI/CD"]');

-- ============================================================
-- 4. article_technologies — 기사-기술 연결 (다대다)
-- ============================================================
CREATE TABLE IF NOT EXISTS article_technologies (
    id            BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    article_id    BIGINT UNSIGNED NOT NULL COMMENT '기사 FK',
    tech_id       INT UNSIGNED NOT NULL COMMENT '기술 FK',
    mention_count INT UNSIGNED DEFAULT 1 COMMENT '해당 기사 내 언급 횟수',
    in_title      TINYINT(1) DEFAULT 0 COMMENT '제목에서 언급',
    in_content    TINYINT(1) DEFAULT 0 COMMENT '본문에서 언급',
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
    FOREIGN KEY (tech_id) REFERENCES technologies(id) ON DELETE CASCADE,
    UNIQUE KEY uq_article_tech (article_id, tech_id),
    INDEX idx_tech_id (tech_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='기사-기술 다대다 연결';

-- ============================================================
-- 5. trends — 월별 기술 트렌드 집계
-- ============================================================
CREATE TABLE IF NOT EXISTS trends (
    id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    tech_id           INT UNSIGNED NOT NULL COMMENT '기술 FK',
    year              SMALLINT UNSIGNED NOT NULL COMMENT '연도',
    month             TINYINT UNSIGNED NOT NULL COMMENT '월 (1~12)',
    mention_count     INT UNSIGNED DEFAULT 0 COMMENT '해당 월 전체 언급 수',
    article_count     INT UNSIGNED DEFAULT 0 COMMENT '언급된 기사 수',
    prev_month_count  INT UNSIGNED DEFAULT 0 COMMENT '전월 언급 수',
    change_rate       DECIMAL(8, 2) COMMENT '변화율 % (+증가, -감소)',
    rank_current      INT UNSIGNED COMMENT '이번달 순위',
    rank_prev         INT UNSIGNED COMMENT '전월 순위',
    last_updated      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (tech_id) REFERENCES technologies(id) ON DELETE CASCADE,
    UNIQUE KEY uq_trend_tech_month (tech_id, year, month),
    INDEX idx_year_month (year, month),
    INDEX idx_change_rate (change_rate)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='월별 기술 트렌드 집계';

-- ============================================================
-- 6. collection_logs — 수집 작업 이력
-- ============================================================
CREATE TABLE IF NOT EXISTS collection_logs (
    id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    source_id   INT UNSIGNED COMMENT '출처 FK',
    status      ENUM('started', 'success', 'failed') NOT NULL DEFAULT 'started',
    item_count  INT UNSIGNED DEFAULT 0 COMMENT '수집된 항목 수',
    error_msg   TEXT COMMENT '오류 메시지 (실패 시)',
    started_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    finished_at DATETIME COMMENT '완료 시각',

    FOREIGN KEY (source_id) REFERENCES sources(id) ON DELETE SET NULL,
    INDEX idx_source_status (source_id, status),
    INDEX idx_started_at (started_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='수집 작업 이력';

-- ============================================================
-- 7. chat_sessions — RAG 챗봇 세션
-- ============================================================
CREATE TABLE IF NOT EXISTS chat_sessions (
    id          VARCHAR(36) PRIMARY KEY COMMENT 'UUID',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='챗봇 대화 세션';

-- ============================================================
-- 8. chat_messages — RAG 챗봇 메시지
-- ============================================================
CREATE TABLE IF NOT EXISTS chat_messages (
    id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    session_id  VARCHAR(36) NOT NULL COMMENT '세션 FK',
    role        ENUM('user', 'assistant') NOT NULL COMMENT '발화자',
    content     TEXT NOT NULL COMMENT '메시지 내용',
    sources     JSON COMMENT '참조 기사 목록 [{id, title, url}]',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (session_id) REFERENCES chat_sessions(id) ON DELETE CASCADE,
    INDEX idx_session_id (session_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='챗봇 대화 메시지';

-- ============================================================
-- 완료 확인
-- ============================================================
SELECT 'init.sql 완료! 생성된 테이블 목록:' AS message;
SHOW TABLES;
