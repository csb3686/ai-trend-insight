# 1. 모든 파이썬 프로세스 강제 종료 (유령 스케줄러 포함)
Write-Host "🧹 모든 파이썬 유령 프로세스를 정리 중..." -ForegroundColor Cyan
taskkill /F /IM python.exe /T 2>$null

# 2. 데이터베이스 교착 상태 해제 스크립트 실행
Write-Host "🔓 데이터베이스 락 해제 중..." -ForegroundColor Cyan
python scratch/kill_locks.py

# 3. 완료 메시지
Write-Host "✅ 모든 정리가 완료되었습니다. 이제 백엔드와 프론트엔드를 다시 켜주세요!" -ForegroundColor Green
