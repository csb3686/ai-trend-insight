# 환경 설치 스크립트 (Windows PowerShell)

Write-Host "--- 백엔드 환경 설정 시작 ---" -ForegroundColor Cyan

# 1. 가상환경 생성
if (!(Test-Path -Path ".venv")) {
    Write-Host "가상환경(.venv) 생성 중..."
    python -m venv .venv
}

# 2. 의존성 설치
Write-Host "의존성 설치 중 (backend/requirements.txt)..."
$python_exe = ".\.venv\Scripts\python.exe"
& $python_exe -m pip install --upgrade pip
& $python_exe -m pip install -r backend/requirements.txt

# 3. Playwright 브라우저 설치
Write-Host "Playwright 브라우저 설치 중..."
& $python_exe -m playwright install chromium

Write-Host "--- 프론트엔드 환경 설정 시작 ---" -ForegroundColor Cyan

# 4. 프론트엔드 의존성 설치
Set-Location frontend
Write-Host "npm 패키지 설치 중 (frontend/)..."
npm install
Set-Location ..

Write-Host "`n모든 환경 설치가 완료되었습니다!" -ForegroundColor Green
Write-Host "이제 '.\dev.ps1'을 실행하여 모든 서비스를 켤 수 있습니다."
