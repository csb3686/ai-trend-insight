import { test, expect } from '@playwright/test';

test.describe('대시보드 핵심 기능 검증', () => {
  test.beforeEach(async ({ page }) => {
    // 메인 대시보드 페이지로 이동
    await page.goto('/');
  });

  test('대시보드 레이아웃 및 헤더 정보가 표시되어야 한다', async ({ page }) => {
    // 서비스 타이틀 확인 (Header 내 요소로 한정하여 중복 방지)
    await expect(page.locator('header').getByText('TrendRadar AI')).toBeVisible();
  });

  test('주요 통계 카드(Stat Cards) 4종이 모두 렌더링되어야 한다', async ({ page }) => {
    // 통계 카드 섹션 가시성 확인 (실제 클래스명 반영)
    const statCards = page.locator('.stat-cards-grid');
    await expect(statCards).toBeVisible();
    
    // 4개의 카드가 있는지 확인 (뉴스, GitHub, 기술, 업데이트)
    const cards = page.locator('.stat-card');
    await expect(cards).toHaveCount(4);
  });

  test('기술 트렌드 히트맵이 정상적으로 그려져야 한다', async ({ page }) => {
    // 히트맵 컨테이너 확인 (실제 클래스명 반영)
    const heatmap = page.locator('.heatmap-grid');
    await expect(heatmap).toBeVisible();
    
    // 데이터가 로드되면 년/월 정보가 포함된 서브타이틀이 표시됨
    await expect(page.locator('.section-subtitle')).toContainText('가장 많이 언급된 기술');
  });

  test('급상승 트렌드 목록과 차트가 노출되어야 한다', async ({ page }) => {
    // 하단 그리드 섹션 확인
    await expect(page.locator('.top-trends-container')).toBeVisible();
    
    // Top Trends 섹션 제목 확인 (실제 텍스트 반영)
    await expect(page.getByText('Top 5 급상승 트렌드')).toBeVisible();
    
    // 최소 하나 이상의 트렌드 카드가 있는지 확인
    const trendCards = page.locator('.trend-card-ultra');
    await expect(trendCards.first()).toBeVisible();
  });
});
