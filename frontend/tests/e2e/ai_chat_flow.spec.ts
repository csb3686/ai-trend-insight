import { test, expect } from '@playwright/test';

test.describe('AI 챗봇 인터랙션 검증', () => {
  test.beforeEach(async ({ page }) => {
    // 모든 페이지에 플로팅 위젯이 있으므로 홈으로 이동
    await page.goto('/');
  });

  test('플로팅 챗봇 트리거 버튼(FAB)이 노출되어야 한다', async ({ page }) => {
    const chatTrigger = page.locator('.chat-trigger-fab');
    await expect(chatTrigger).toBeVisible();
    await expect(page.getByText('AI 분석가에게 물어보기')).toBeVisible();
  });

  test('버튼 클릭 시 챗봇 창이 열리고 인사말이 표시되어야 한다', async ({ page }) => {
    const chatTrigger = page.locator('.chat-trigger-fab');
    await chatTrigger.click();
    
    // 챗봇 창(유리 패널) 노출 확인
    const chatWindow = page.locator('.chat-window-extended');
    await expect(chatWindow).toBeVisible();
    
    // 타이틀 확인 (h3 태그 내의 텍스트로 한정)
    await expect(page.locator('.title-text h3')).toHaveText('TrendRadar AI');
    
    // 기본 인사말 확인 (마크다운 볼드 처리가 포함되어 있으므로 포함 여부로 확인)
    await expect(page.getByText('안녕하세요!', { exact: false })).toBeVisible();
    await expect(page.locator('.markdown-content')).toContainText('TrendRadar AI');
  });

  test('메시지 입력 시 전송 버튼이 활성화되고 답변이 생성되어야 한다', async ({ page }) => {
    // 위젯 오픈
    await page.locator('.chat-trigger-fab').click();
    
    const textarea = page.locator('.chat-textarea');
    const sendButton = page.locator('.send-btn-v2');
    
    // 초기에는 전송 버튼 비활성 상태 (텍스트가 없으므로)
    // await expect(sendButton).toBeDisabled(); // 실제 코드에서 disabled 처리가 되어 있는지 확인 필요
    
    // 'TypeScript' 입력
    await textarea.fill('TypeScript에 대해 알려줘');
    
    // 전송 버튼 클릭
    await sendButton.click();
    
    // 로딩 인디케이터 등장 확인
    await expect(page.locator('.loading-dots')).toBeVisible();
    await expect(page.getByText('뉴스를 분석하며 답변을 생성 중입니다...')).toBeVisible();
    
    // 답변이 올 때까지 대기 (최대 30초 설정)
    const aiMessage = page.locator('.message-bubble-wrapper.ai').last();
    await expect(aiMessage).toContainText('TypeScript', { timeout: 30000 });
    
    // '📚 주요 참고 소식' 섹션이 포함되어 있는지 확인 (RAG 무결성 검증)
    await expect(aiMessage).toContainText('📚 주요 참고 소식');
  });

  test('챗봇 창을 닫을 수 있어야 한다', async ({ page }) => {
    await page.locator('.chat-trigger-fab').click();
    const closeButton = page.locator('.close-btn-v2');
    
    await closeButton.click();
    
    // 창이 사라졌는지 확인
    await expect(page.locator('.chat-window-extended')).not.toBeVisible();
  });
});
