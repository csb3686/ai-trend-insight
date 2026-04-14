import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, X, Send, Loader2 } from 'lucide-react';
import { useChatMutation } from '../../api/hooks/useChat';
import './ChatWidget.css';

interface Message {
  role: 'user' | 'ai';
  content: string;
}

const ChatWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [inputText, setInputText] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    { role: 'ai', content: '안녕하세요! TrendRadar AI 어시스턴트입니다. 요즘 뜨는 기술이나 특정 뉴스에 대해 궁금한 점이 있으신가요?' }
  ]);
  
  const chatBodyRef = useRef<HTMLDivElement>(null);
  const chatMutation = useChatMutation();

  // 메시지 추가 시 자동 스크롤
  useEffect(() => {
    if (chatBodyRef.current) {
      chatBodyRef.current.scrollTop = chatBodyRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (!inputText.trim() || chatMutation.isPending) return;

    const userMsg = inputText.trim();
    setInputText('');
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);

    try {
      const response = await chatMutation.mutateAsync({ message: userMsg });
      setMessages(prev => [...prev, { role: 'ai', content: response.answer }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'ai', content: '죄송합니다. 답변을 생성하는 도중 오류가 발생했습니다.' }]);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') handleSend();
  };

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
          
          <div className="chat-body" ref={chatBodyRef}>
            {messages.map((msg, idx) => (
              <div key={idx} className={`chat-message ${msg.role}`}>
                {msg.content}
              </div>
            ))}
            {chatMutation.isPending && (
              <div className="chat-message ai flex items-center gap-2">
                <Loader2 size={16} className="animate-spin" />
                답변을 생각 중입니다...
              </div>
            )}
          </div>

          <div className="chat-input-area">
            <input 
              type="text" 
              placeholder="질문을 입력하세요..." 
              className="chat-input"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={chatMutation.isPending}
            />
            <button className="send-btn" onClick={handleSend} disabled={chatMutation.isPending}>
              {chatMutation.isPending ? <Loader2 size={18} className="animate-spin" /> : <Send size={18} />}
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
