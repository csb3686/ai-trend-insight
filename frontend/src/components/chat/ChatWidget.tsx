import React, { useState } from 'react';
import { MessageSquare, X, Send } from 'lucide-react';
import './ChatWidget.css';

const ChatWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="chat-widget-container">
      {isOpen && (
        <div className="chat-window glass-panel">
          <div className="chat-header">
            <div className="chat-title">
              <span className="dot online"></span>
              AI 기술 어시스턴트
            </div>
            <button className="close-btn" onClick={() => setIsOpen(false)}>
              <X size={18} />
            </button>
          </div>
          
          <div className="chat-body">
            <div className="chat-message ai">
              안녕하세요! 무엇을 도와드릴까요? 특정 기술의 트렌드나 요약을 물어보세요.
            </div>
            {/* 임시 더미 메시지 */}
            <div className="chat-message user">
              요즘 React 서버 컴포넌트가 왜 뜨는거야?
            </div>
            <div className="chat-message ai">
              React 서버 컴포넌트(RSC)는 초기 로딩 속도 최적화와 번들 사이즈 감소, 그리고 SEO 향상 등의 장점 때문에 최근 많은 개발자들의 주목을 받고 있습니다. Next.js 13 이상에서 이 패턴을 적극 채택하면서 도입이 가속화되었습니다.
            </div>
          </div>

          <div className="chat-input-area">
            <input type="text" placeholder="질문을 입력하세요..." className="chat-input" />
            <button className="send-btn">
              <Send size={18} />
            </button>
          </div>
        </div>
      )}
      
      {!isOpen && (
        <button className="chat-fab" onClick={() => setIsOpen(true)}>
          <MessageSquare size={24} />
        </button>
      )}
    </div>
  );
};

export default ChatWidget;
