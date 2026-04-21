import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright 설정 파일
 * 현업에서는 크로스 브라우징 테스트를 위해 여러 브라우저 엔진을 설정합니다.
 */
export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: false, // 로컬 안정성을 위해 순차 실행 권장
  forbidOnly: !!process.env.CI,
  retries: 1, // 실패 시 1회 재시도 (현업 표준)
  workers: 1, // 로컬 환경 부담을 줄이기 위해 1개씩 실행
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:5173', // Vite 기본 포트
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],

  /* 테스트 실행 전 로컬 서버 자동 시작 설정 (현업 권장 방식) */
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
});
