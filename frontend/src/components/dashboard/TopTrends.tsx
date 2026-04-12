import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';
import { topTrendsData } from '../../mocks/dashboardData';
import './TopTrends.css';

const TopTrends: React.FC = () => {
  return (
    <div className="glass-panel">
      <div className="section-header">
        <div>
          <h2 className="section-title">Top 5 트렌드</h2>
          <p className="section-subtitle">지난달 대비 변화율</p>
        </div>
      </div>

      <div className="trend-list">
        {topTrendsData.map((trend, index) => (
          <div key={trend.id} className="trend-list-item">
            <div className="trend-rank">
              {String(index + 1).padStart(2, '0')}
            </div>
            
            <div className="trend-info">
              <div className="trend-name-row">
                <span className="trend-name">{trend.name}</span>
                <span className={`badge ${trend.category.replace('/', '-')}`}>{trend.category}</span>
              </div>
              <div className="trend-desc">{trend.desc}</div>
            </div>

            <div className={`trend-change ${trend.isUp ? 'up' : 'down'}`}>
              {trend.isUp ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
              <span>{trend.isUp ? '+' : ''}{trend.changePercent}%</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TopTrends;
