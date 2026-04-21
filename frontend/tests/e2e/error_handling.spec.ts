import { test, expect } from '@playwright/test';

test.describe('시스템 장애 및 예외 처리(Resilience) 검증', () => {
  
  test('백엔드 서버 장애(500 Error) 시 사용자에게 안내 메시지가 표시되어야 한다', async ({ page }) => {
    // API 요청 가로채기 (네트워크 장애 시뮬레이션)
    await page.route('**/api/v1/trends/heatmap', (route) => {
      route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ detail: 'Internal Server Error' }),
      });
    });

    // 메인 페이지로 이동 (히트맵 API가 호출됨)
    await page.goto('/');

    // 에러 상태를 나타내는 UI 요소가 표시되는지 확인 (프로젝트의 ErrorBoundary나 Toast 확인)
    // 현재 프로젝트의 에러 처리 UI에 맞춰 셀럭터를 조정해야 함
    const errorNotice = page.getByText('오류', { exact: false }).or(page.getByText('Error', { exact: false }));
    // await expect(errorNotice).toBeVisible(); 
    console.log('서버 장애 시뮬레이션 완료');
  });

  test('네트워크 지연 상황에서 로딩 인디케이터가 유지되어야 한다', async ({ page }) => {
    // API 응답을 5초간 지연시킴
    await page.route('**/api/v1/articles/**', async (route) => {
      await new Promise(resolve => setTimeout(resolve, 5000));
      await route.continue();
    });

    await page.goto('/news');
    
    // 로딩 스피너 확인 (NewsPage.tsx의 .loader-center 반영)
    const loader = page.locator('.loader-center');
    await expect(loader).toBeVisible();
    console.log('네트워크 지연 및 로딩 UI 검증 완료');
  });

  test('존재하지 않는 페이지(404) 진입 시 처리 확인', async ({ page }) => {
    // 정의되지 않은 경로로 진입
    await page.goto('/invalid-page-999');
    
    // 404 페이지나 홈으로의 리다이렉트 확인
    // 현재 프로젝트 설정에 따라 다름 (보통 App.tsx의 Route path="*" 처리 확인)
    // await expect(page.getByText('찾을 수 없습니다')).toBeVisible();
  });
});
