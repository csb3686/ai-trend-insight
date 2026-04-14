# Phase 6-2: 트렌드 API 구현 작업 현황

- `[x]` 6-2. 트렌드 API 인프라 구축
    - `[x]` `backend/app/schemas/trend.py` 생성 (응답 규격 정의)
    - `[x]` `backend/app/services/trend_service.py` 생성 (DB 조회 로직)
    - `[x]` `backend/app/api/v1/endpoints/trends.py` 생성 (라우터)
    - `[x]` API 통합 등록 (`app.api.v1.__init__.py`)
- `[x]` 기능별 엔드포인트 구현
    - `[x]` `GET /trends/heatmap`: 기술별 언급 횟수 (히트맵용)
    - `[x]` `GET /trends/top5`: 급상승/급하락 기술 (변화율 기준)
    - `[x]` `GET /trends/timeline/{tech_id}`: 특정 기술의 월별 변동 추이
    - `[x]` `GET /trends/keywords`: 검색용 모든 기술 키워드 목록
- `[ ]` 최종 확인 및 연동
    - `[ ]` Swagger UI 테스트 및 JSON 구조 확인
    - `[ ]` TODO.md 관련 항목 체크 [x] 업데이트
