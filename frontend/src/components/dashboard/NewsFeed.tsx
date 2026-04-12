import React from 'react';
import { ExternalLink } from 'lucide-react';
import { latestNewsData } from '../../mocks/dashboardData';
import './NewsFeed.css';

const NewsFeed: React.FC = () => {
  return (
    <div className="glass-panel news-panel">
      <div className="section-header">
        <div>
          <h2 className="section-title">최신 뉴스</h2>
          <p className="section-subtitle">실시간 기술 뉴스 피드</p>
        </div>
        <a href="/news" className="view-all-link">전체 보기 &rarr;</a>
      </div>

      <div className="news-list">
        {latestNewsData.map((news) => (
          <a key={news.id} href={news.url} className="news-item" target="_blank" rel="noopener noreferrer">
            <div className="news-content">
              <h3 className="news-title">{news.title}</h3>
              <div className="news-meta">
                <span className={`badge ${news.category.replace('/', '-')}`}>{news.category}</span>
                <span className="news-source">{news.source}</span>
                <span className="news-dot">&middot;</span>
                <span className="news-time">{news.timeAgo}</span>
              </div>
            </div>
            <div className="news-action">
              <ExternalLink size={16} color="var(--text-muted)" />
            </div>
          </a>
        ))}
      </div>
    </div>
  );
};

export default NewsFeed;
