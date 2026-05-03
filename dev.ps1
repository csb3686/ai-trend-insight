# 통합 실행 스크립트 (Windows PowerShell)

Write-Host "--- AI Trend Insight 플랫폼 구동 시작 ---" -ForegroundColor Cyan

# 1. 백엔드 실행 (FastAPI)
Write-Host "백엔드(FastAPI) 시작 중... (포트 8000)"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; ..\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload" -WindowStyle Normal

# 2. 스케줄러 실행
Write-Host "스케줄러 시작 중..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; ..\.venv\Scripts\python.exe pipeline/scheduler.py" -WindowStyle Normal

# 3. 프론트엔드 실행 (Vite)
Write-Host "프론트엔드(Vite) 시작 중... (포트 5173)"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev" -WindowStyle Normal

Write-Host "`n모든 서비스가 별도의 창에서 실행되었습니다." -ForegroundColor Green
Write-Host "Backend API: http://localhost:8000/docs"
Write-Host "Frontend UI: http://localhost:5173"
