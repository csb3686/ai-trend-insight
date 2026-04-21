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
    trace: 'on', // 모든 테스트 과정 기록 (Trace View용)
    screenshot: 'on', // 모든 단계 스크린샷 캡처
    video: 'on', // 모든 테스트 수행 영상 녹화
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

  /* 이미 npm run dev가 실행 중이므로 자동 서버 시작은 비활성화합니다. */
  // webServer: {
  //   command: 'npm run dev',
  //   url: 'http://localhost:5173',
  //   reuseExistingServer: !process.env.CI,
  // },
});
