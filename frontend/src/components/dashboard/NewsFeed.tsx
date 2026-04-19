import React from 'react';
import { Link } from 'react-router-dom';
import { ExternalLink, Loader2 } from 'lucide-react';
import { useArticles } from '../../api/hooks/useArticles';
import './NewsFeed.css';

const NewsFeed: React.FC = () => {
  const { data, isLoading, isError } = useArticles(0, 5);

  if (isLoading) {
    return (
      <div className="glass-panel news-panel p-8 flex-center">
        <Loader2 className="animate-spin" size={24} color="var(--color-ai)" />
      </div>
    );
  }

  if (isError || !data) {
    return <div className="glass-panel news-panel p-8 text-center text-gray-500">뉴스를 불러오지 못했습니다.</div>;
  }

  const formatDate = (dateStr?: string | null) => {
    if (!dateStr) return '날짜 정보 없음';
    const date = new Date(dateStr);
    return `${date.getMonth() + 1}월 ${date.getDate()}일`;
  };

  return (
    <div className="glass-panel news-panel">
      <div className="section-header">
        <div>
          <h2 className="section-title">최신 소식</h2>
          <p className="section-subtitle">실시간 기술 뉴스 및 GitHub 트렌드</p>
        </div>
        <Link to="/news" className="view-all-link">전체 보기 &rarr;</Link>
      </div>

      <div className="news-list">
        {data.items.map((news) => (
          <a key={news.id} href={news.url} className="news-item-modern" target="_blank" rel="noopener noreferrer">
            <div className="news-content-row">
              <div className="news-title-area">
                <span className={`category-pill-mini ${news.tech_category?.toLowerCase()?.replace('/', '-')?.trim() || 'others'}`}>
                  {news.tech_category || 'Others'}
                </span>
                <h3 className="news-title-text">{news.title}</h3>
              </div>
              
              <div className="news-meta-right">
                <span className="news-source-small">{news.source_name}</span>
                <span className="news-time-small">{formatDate(news.published_at || news.created_at)}</span>
                <ExternalLink size={14} className="news-link-icon" />
              </div>
            </div>
          </a>
        ))}
      </div>
    </div>
  );
};

export default NewsFeed;
