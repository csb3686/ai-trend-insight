import React from 'react';
import { TrendingUp, TrendingDown, Loader2 } from 'lucide-react';
import { useTopTrends } from '../../api/hooks/useTrends';
import './TopTrends.css';

const TopTrends: React.FC = () => {
  const { data, isLoading, isError } = useTopTrends();

  if (isLoading) {
    return (
      <div className="glass-panel p-8 flex-center">
        <Loader2 className="animate-spin" size={24} color="var(--color-ai)" />
      </div>
    );
  }

  if (isError || !data) {
    return <div className="glass-panel p-8 text-center text-gray-500 text-sm">트렌드 순위를 가져오지 못했습니다.</div>;
  }

  // 급상승(rising) 상위 5개를 메인으로 표시
  const displayTrends = data.rising.slice(0, 5);

  return (
    <div className="glass-panel">
      <div className="section-header">
        <div>
          <h2 className="section-title">Top 5 급상승 트렌드</h2>
          <p className="section-subtitle">전월 대비 언급량 변화</p>
        </div>
      </div>

      <div className="trend-list">
        {displayTrends.map((trend, index) => {
          const change = trend.change_rate;
          const isUp = change > 0.1;
          const isDown = change < -0.1;

          return (
            <div key={trend.name} className="trend-card-new">
              <div className="trend-rank-hero">{String(index + 1).padStart(2, '0')}</div>
              
              <div className="trend-content-main">
                <div className="trend-header-row">
                  <span className="trend-name-bold">{trend.name}</span>
                  <span className={`category-pill-small ${trend.category.replace('/', '-').toLowerCase()}`}>
                    {trend.category}
                  </span>
                </div>
                <div className="trend-one-liner">최근 관련 분야에서 언급량이 {Math.abs(change).toFixed(0)}% 변화하며 급부상 중입니다.</div>
              </div>

              <div className={`trend-indicator-box ${isUp ? 'up' : isDown ? 'down' : 'new'}`}>
                <span className="indicator-icon">{isUp ? '↑' : isDown ? '↓' : '•'}</span>
                <span className="indicator-value">{Math.abs(change).toFixed(0)}%</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default TopTrends;
