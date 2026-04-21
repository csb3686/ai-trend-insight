# [STAGE 1] Build & Dependency Setup
FROM python:3.11-slim

# 기본 시스템 패키지 및 Playwright 의존성 설치
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 2. 작업 디렉토리 설정 (기존 소스 경로 유지)
WORKDIR /
COPY requirements.txt /backend/requirements.txt
RUN pip install --no-cache-dir -r /backend/requirements.txt

# 3. Playwright & 브라우저 설치
RUN playwright install --with-deps chromium

# 4. 소스 코드 복사 (backend 폴더 구조 유지)
COPY . /backend/

# 5. 실행 환경 설정
WORKDIR /backend
ENV PYTHONPATH=/:/backend

# 환경 변수 설정 (Docker 내부 네트워크 호스트 기본값)
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8

# 서버 실행 (FastAPI)
# 포트는 docker-compose에서 제어하거나 8000 기본 사용
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
