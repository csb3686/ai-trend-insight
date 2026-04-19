import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import DashboardPage from './pages/DashboardPage';
import NewsPage from './pages/NewsPage';
import EcosystemPage from './pages/EcosystemPage';
import ChatWidget from './components/chat/ChatWidget';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/news" element={<NewsPage />} />
        <Route path="/ecosystem" element={<EcosystemPage />} />
      </Routes>
      <ChatWidget />
    </Router>
  );
}

export default App;
