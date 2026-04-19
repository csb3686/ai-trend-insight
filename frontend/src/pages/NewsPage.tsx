import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/layout/Header';
import { useArticles } from '../api/hooks/useArticles';
import { useTopTrends } from '../api/hooks/useTrends';
import { Search, Loader2, ExternalLink, Calendar, Code, Newspaper, ArrowLeft } from 'lucide-react';
import './NewsPage.css';

const PAGE_SIZE = 12;

const NewsPage: React.FC = () => {
  const navigate = useNavigate();
  const [q, setQ] = useState('');
  const [activeType, setActiveType] = useState<'all' | 'news' | 'github_repo'>('all');
  const [skip, setSkip] = useState(0);
  const [allArticles, setAllArticles] = useState<any[]>([]);

  // 실시간 급상승 트렌드 데이터 가져오기
  const { data: trendData } = useTopTrends();
  const risingTrends = trendData?.rising || [];
  
  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQ(e.target.value);
    setSkip(0);
  };

  const { data, isLoading, isFetching } = useArticles(
    skip, 
    PAGE_SIZE, 
    activeType === 'all' ? undefined : activeType, 
    q || undefined, 
    undefined // 카테고리 필터 제거
  );

  useEffect(() => {
    if (data?.items) {
      if (skip === 0) {
        setAllArticles(data.items);
      } else {
        setAllArticles(prev => [...prev, ...data.items]);
      }
    }
  }, [data, skip]);

  useEffect(() => {
    setSkip(0);
  }, [activeType]);

  const loadMore = () => {
    if (!isFetching && data && allArticles.length < data.total) {
      setSkip(prev => prev + PAGE_SIZE);
    }
  };

  const formatDate = (dateStr?: string | null) => {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return `${date.getFullYear()}.${date.getMonth() + 1}.${date.getDate()}`;
  };

  return (
    <div className="app-container">
      <div className="main-content">
        <Header />
        
        <main className="page-container news-archive-container">
          <section className="news-hero glass-panel">
            <div className="hero-top-row">
              <button className="back-btn" onClick={() => navigate(-1)}>
                <ArrowLeft size={20} />
                <span>뒤로가기</span>
              </button>
            </div>
            
            <div className="hero-content">
              <h2 className="news-page-title">기술 뉴스 & 트렌드 아카이브</h2>
              <p className="news-page-subtitle">전 세계 AI 생태계의 소식을 핀포인트로 탐색하세요.</p>
            </div>
            
            <div className="search-and-filter-bar">
              <div className="search-box-premium">
                <Search className="search-icon" size={20} />
                <input 
                  type="text" 
                  placeholder="관심 있는 기사 제목을 검색해 보세요..." 
                  value={q}
                  onChange={handleSearchChange}
                  className="premium-search-input"
                />
              </div>

              {/* 급상승 트렌드: 검색창 아래 중앙 배치 */}
              <div className="trending-tags-container animate-fade-in">
                <div className="trending-label">
                  <span className="fire-icon">🔥</span>
                  <span>지금 뜨는 기술 키워드</span>
                </div>
                <div className="trending-tags-list">
                  {risingTrends.length > 0 ? (
                    risingTrends.map((trend: any) => (
                      <button 
                        key={trend.tech_id} 
                        className="trend-tag"
                        onClick={() => {
                          setQ(trend.name);
                          setSkip(0);
                        }}
                      >
                        {trend.name}
                      </button>
                    ))
                  ) : (
                    <span className="trending-placeholder">분석 중...</span>
                  )}
                </div>
              </div>
            </div>
          </section>

          {/* 리스트 필터: 데이터 그리드 바로 위로 이동 */}
          <div className="type-toggle-row">
            <div className="type-toggle-group">
              <button className={`type-btn ${activeType === 'all' ? 'active' : ''}`} onClick={() => setActiveType('all')}>전체</button>
              <button className={`type-btn ${activeType === 'news' ? 'active' : ''}`} onClick={() => setActiveType('news')}><Newspaper size={14} /> 뉴스</button>
              <button className={`type-btn ${activeType === 'github_repo' ? 'active' : ''}`} onClick={() => setActiveType('github_repo')}><Code size={14} /> GitHub</button>
            </div>
          </div>

          <div className="news-grid-master">
            {allArticles.map((item, idx) => (
              <a key={`${item.id}-${idx}`} href={item.url} target="_blank" rel="noopener noreferrer" className="news-card-master glass-panel animate-fade-in">
                <div className="card-top">
                  <span className="source-label-mini">{item.source_name}</span>
                </div>
                <h3 className="card-title-master">{item.title}</h3>
                <div className="card-bottom">
                  <span className="card-date-mini"><Calendar size={12} /> {formatDate(item.published_at || item.created_at)}</span>
                  <ExternalLink size={14} className="card-link-icon" />
                </div>
              </a>
            ))}
          </div>

          {isLoading && skip === 0 ? (
            <div className="loader-center py-20"><Loader2 className="animate-spin" size={48} color="var(--color-ai)" /></div>
          ) : (
            data && allArticles.length < data.total && (
              <div className="load-more-container">
                <button className="btn-load-more" onClick={loadMore} disabled={isFetching}>
                  {isFetching ? <Loader2 className="animate-spin" size={18} /> : '더 많은 소식 불러오기'}
                </button>
              </div>
            )
          )}
        </main>
      </div>
    </div>
  );
};

export default NewsPage;
