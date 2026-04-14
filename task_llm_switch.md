# Phase: LLM 공급자 전환 (Gemini -> Groq)

- `[x]` 1. 서비스 환경 설정 업데이트
    - `[x]` `.env` 파일에 `GROQ_API_KEY` 항목 추가
    - `[x]` `backend/app/core/config.py`에 Groq 설정 반영
- `[x]` 2. RAG 서비스 로직 교체
    - `[x]` `backend/app/services/rag_service.py` 수정 (Groq API 연동)
    - `[x]` 모델 및 메시지 포맷 최적화 (Llama 3 기반)
- `[x]` 3. 프로젝트 문서 최신화
    - `[x]` `PLAN.md` 기술 스택 업데이트
    - `[x]` `README.md` 주요 기능 설명 업데이트
    - `[x]` `TODO.md` 체크박스 시스템 동기화
- `[ ]` 4. 최종 검증
    - `[ ]` Swagger UI를 통한 실시간 대화 테스트
    - `[ ]` 응답 속도 및 할당량 에러 여부 확인
