import { test, expect } from '@playwright/test';

test.describe('뉴스 아카이브 및 검색 기능 검증', () => {
  test.beforeEach(async ({ page }) => {
    // 뉴스 페이지로 이동 (Header 메뉴 클릭 시뮬레이션 대신 직접 이동)
    await page.goto('/news');
  });

  test('뉴스 페이지의 기본 영웅 섹션과 검색바가 노출되어야 한다', async ({ page }) => {
    await expect(page.locator('.news-page-title')).toBeVisible();
    await expect(page.getByPlaceholder('관심 있는 기사 제목을 검색해 보세요...')).toBeVisible();
  });

  test('뉴스 결과 그리드가 최소 하나 이상의 기사를 포함해야 한다', async ({ page }) => {
    // 뉴스 그리드가 로드될 때까지 대기
    const newsGrid = page.locator('.news-grid-master');
    await expect(newsGrid).toBeVisible();
    
    // 기사 카드가 최소 1개는 있어야 함 (수집된 데이터가 있다는 가정)
    const cards = page.locator('.news-card-master');
    const count = await cards.count();
    console.log(`수집된 뉴스 개수: ${count}`);
    expect(count).toBeGreaterThan(0);
  });

  test('검색어 입력 시 결과 목록이 반응해야 한다', async ({ page }) => {
    const searchInput = page.getByPlaceholder('관심 있는 기사 제목을 검색해 보세요...');
    
    // 'TypeScript' 검색 입력
    await searchInput.fill('TypeScript');
    
    // 로딩 처리나 결과 업데이트를 위한 짧은 대기
    await page.waitForTimeout(1000);
    
    // 검색 결과가 나타나야 함 (제목에 해당 키워드가 포함된 카드가 있는지 확인)
    const titles = page.locator('.card-title-master');
    const firstTitle = await titles.first().innerText();
    console.log(`검색된 첫 번째 제목: ${firstTitle}`);
    // 대소문자 구분 없이 포함 여부 확인
    expect(firstTitle.toLowerCase()).toContain('typescript');
  });

  test('뉴스/GitHub 타입 필터링이 동작해야 한다', async ({ page }) => {
    const newsFilter = page.getByText('뉴스', { exact: false });
    const githubFilter = page.getByText('GitHub', { exact: false });
    
    // GitHub 필터 클릭
    await githubFilter.click();
    await page.waitForTimeout(1000);
    
    // 소스 라벨 등에 'GitHub' 혹은 관련 정보가 있는지 확인 (필요시 데이터 id 등으로 더 정밀하게 체크 가능)
    const sourceLabel = page.locator('.source-label-mini').first();
    await expect(sourceLabel).toBeVisible();
  });
});
