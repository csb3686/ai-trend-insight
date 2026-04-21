import { test, expect } from '@playwright/test';

test.describe('Ecosystem Map 시각화 검증', () => {
  
  test.beforeEach(async ({ page }) => {
    // 테스트 시작 전 에코시스템 페이지로 이동
    await page.goto('/ecosystem');
    // 페이지 로딩 대기
    await page.waitForLoadState('networkidle');
  });

  test('페이지 제목 및 기본 레이아웃이 로드되어야 한다', async ({ page }) => {
    // 내부 <h1> 제목 확인 (브라우저 타이틀 대신 실제 요소 확인)
    const header = page.locator('h1.clean-title');
    await expect(header).toContainText('Technology Ecosystem Map');
    
    // 네비게이션 버튼 확인
    const backBtn = page.locator('.back-btn-clean');
    await expect(backBtn).toBeVisible();
  });

  test('사이트스케이프(Cytoscape) 그래프 컨테이너가 렌더링되어야 한다', async ({ page }) => {
    // 실제 클래스명인 .cytoscape-container 존재 여부 확인
    const cyContainer = page.locator('.cytoscape-container');
    await expect(cyContainer).toBeVisible();

    // 그래프 캔버스 요소가 실제로 생성되었는지 확인
    // (Cytoscape는 레이어 처리를 위해 내부에 여러 개의 canvas 요소를 생성할 수 있음)
    const canvas = cyContainer.locator('canvas');
    await expect(canvas.first()).toBeVisible({ timeout: 10000 });
    
    // 최소 1개 이상의 canvas가 존재하는지 확인
    const count = await canvas.count();
    expect(count).toBeGreaterThanOrEqual(1);
  });

  test('범례(Legend) 정보가 표시되어야 한다', async ({ page }) => {
    // 그래프 하단의 범례 섹션 가시성 확인
    const legend = page.locator('.category-legend-clean');
    await expect(legend).toBeVisible();
    
    // 주요 카테고리 포함 여부 확인
    await expect(legend).toContainText('AI & Machine Learning');
    await expect(legend).toContainText('Languages');
  });
});
