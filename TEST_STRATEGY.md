# 🧪 테스트 전략서 (TEST_STRATEGY.md)

> **프로젝트**: AI 테크 트렌드 인사이트 플랫폼  
> **작성자**: QA 엔지니어  
> **최종 수정일**: 2026-04-19  

---

## 1. 개요 (Overview)
본 문서는 AI 테크 트렌드 인사이트 플랫폼의 소프트웨어 품질을 보증하기 위한 전반적인 테스트 전략을 정의합니다. 데이터 수집 자동화부터 시각화 UI까지 전체 파이프라인의 안정성과 신뢰성을 확보하는 것을 목표로 합니다.

## 2. 테스트 목표 (Test Objectives)
- **수집 파이프라인 안정성**: 뉴스 및 GitHub 데이터 수집 시 에러 핸들링 및 데이터 누락 방지 확인.
- **REST API 정합성**: 백엔드 API가 정의된 스키마에 따라 정확한 데이터를 반환하는지 검증.
- **AI RAG 신뢰성**: 질문에 대해 적절한 답변과 출처 링크가 정상적으로 생성되는지 검증.
- **UI 시각화 가시성**: 핵심 레이아웃(히트맵, 대시보드)이 브라우저에서 올바르게 렌더링되는지 확인.

## 3. 테스트 범위 및 수준 (Scope & Levels)

### 3-1. API 통합 테스트 (Integration Testing)
- **도구**: `pytest`, `httpx`
- **대상**: FastAPI 엔드포인트 (`/trends`, `/articles`, `/chat`)
- **내용**: HTTP 상태 코드, JSON 스키마, DB 연동 비즈니스 로직 검증.

### 3-2. 수집 파이프라인 검증 (Component Testing)
- **도구**: `pytest`, `unittest.mock`
- **대상**: `BaseCollector` 및 개별 수집기 클래스
- **내용**: 실제 네트워크 통신 없이 Mock 데이터를 활용한 파싱 로직 및 DB 저장 함수 테스트.

### 3-3. UI 자동화 / E2E 테스트 (End-to-End Testing)
- **도구**: `Playwright`
- **대상**: 프론트엔드 주요 페이지 및 인터랙션
- **내용**: 
    - 대시보드 진입 시 차트 노출 확인.
    - 기술 생태계 지도(Ecosystem Map) 렌더링 확인.
    - 챗봇 질문 전송 및 응답 수신 시나리오 확인.

## 4. 테스트 환경 (Test Environment)
- **언어**: Python 3.11+, TypeScript
- **DB**: Local MySQL (운영 DB와 분리된 Test Database 권장)
- **CI**: GitHub Actions

## 5. 결함 관리 프로세스 (Defect Management)
1. **결함 식별**: 자동화 테스트 실패 시 로그 분석.
2. **이슈 등록**: GitHub Issues를 통한 결함 리포팅 (Reproduce Step 포함).
3. **수정 및 확인**: 개발자 수정 후 재테스트(Regression Test) 수행.
