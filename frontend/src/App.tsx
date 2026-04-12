import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import DashboardPage from './pages/DashboardPage';
import ChatWidget from './components/chat/ChatWidget';
// 스타일 파일 (App.css는 비우거나 삭제)
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        {/* 추후 구현될 뉴스 페이지 공간 */}
        <Route path="/news" element={<div style={{color: 'white', padding: '2rem'}}>뉴스 상세 페이지 (준비 중)</div>} />
      </Routes>
      <ChatWidget />
    </Router>
  );
}

export default App;
