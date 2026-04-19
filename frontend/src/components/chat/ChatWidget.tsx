import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, X, Send, Loader2, BookOpen } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { useChatMutation } from '../../api/hooks/useChat';
import './ChatWidget.css';

interface Message {
  role: 'user' | 'ai';
  content: string;
  sources?: string[]; // 답변에 사용된 참고 기사 제목들
}

const ChatWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [inputText, setInputText] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    { 
      role: 'ai', 
      content: '안녕하세요! **TrendRadar AI** 어시스턴트입니다. \n\n제가 수집한 수만 개의 기술 뉴스를 바탕으로 궁금하신 점을 분석해 드릴게요. 무엇을 도와드릴까요?' 
    }
  ]);
  
  const chatBodyRef = useRef<HTMLDivElement>(null);
  const chatMutation = useChatMutation();

  useEffect(() => {
    if (chatBodyRef.current) {
      chatBodyRef.current.scrollTop = chatBodyRef.current.scrollHeight;
    }
  }, [messages, chatMutation.isPending]);

  const handleSend = async () => {
    if (!inputText.trim() || chatMutation.isPending) return;

    const userMsg = inputText.trim();
    setInputText('');
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);

    try {
      const response = await chatMutation.mutateAsync({ message: userMsg });
      setMessages(prev => [...prev, { 
        role: 'ai', 
        content: response.answer,
        sources: response.sources 
      }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'ai', content: '죄송합니다. 서버와 통신하는 도중 오류가 발생했습니다.' }]);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-widget-container">
      {isOpen && (
        <div className="chat-window-extended glass-panel animate-in">
          <div className="chat-header-v2">
            <div className="chat-title-group">
              <div className="status-indicator">
                <div className="status-dot"></div>
                <div className="status-ring"></div>
              </div>
              <div className="title-text">
                <h3>TrendRadar AI</h3>
                <span>RAG-powered Intelligence</span>
              </div>
            </div>
            <button className="close-btn-v2" onClick={() => setIsOpen(false)}>
              <X size={20} />
            </button>
          </div>
          
          <div className="chat-body-v2" ref={chatBodyRef}>
            {messages.map((msg, idx) => (
              <div key={idx} className={`message-bubble-wrapper ${msg.role}`}>
                <div className="message-bubble">
                  {msg.role === 'ai' ? (
                    <div className="markdown-content">
                      <ReactMarkdown 
                        remarkPlugins={[remarkGfm]}
                        components={{
                          a: ({node, ...props}) => (
                            <a {...props} target="_blank" rel="noopener noreferrer" />
                          )
                        }}
                      >
                        {msg.content}
                      </ReactMarkdown>
                    </div>
                  ) : (
                    <div className="user-text">{msg.content}</div>
                  )}
                </div>
              </div>
            ))}
            {chatMutation.isPending && (
              <div className="message-bubble-wrapper ai">
                <div className="message-bubble loading">
                  <div className="loading-dots">
                    <span></span><span></span><span></span>
                  </div>
                  <span className="loading-text">뉴스를 분석하며 답변을 생성 중입니다...</span>
                </div>
              </div>
            )}
          </div>

          <div className="chat-input-v2">
            <textarea 
              placeholder="질문을 입력하세요" 
              className="chat-textarea"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={handleKeyPress}
              rows={1}
            />
            <button className="send-btn-v2" onClick={handleSend} disabled={chatMutation.isPending || !inputText.trim()}>
              <Send size={18} />
            </button>
          </div>
        </div>
      )}
      
      {!isOpen && (
        <button className="chat-trigger-fab pulse-animation" onClick={() => setIsOpen(true)}>
          <MessageSquare size={28} />
          <span className="tooltip">AI 분석가에게 물어보기</span>
        </button>
      )}
    </div>
  );
};

export default ChatWidget;
