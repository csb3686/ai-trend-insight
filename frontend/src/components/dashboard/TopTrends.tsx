import React from 'react';
import { Loader2 } from 'lucide-react';
import { ResponsiveContainer, AreaChart, Area, YAxis } from 'recharts';
import { useTopTrends } from '../../api/hooks/useTrends';
import './TopTrends.css';

interface TopTrendsProps {
  onTechClick?: (techId: number) => void;
}

const TopTrends: React.FC<TopTrendsProps> = ({ onTechClick }) => {
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

  const displayTrends = data.rising.slice(0, 5);

  return (
    <div className="glass-panel top-trends-container">
      <div className="section-header-advanced">
        <div className="header-content">
          {/* 별 문양 제거됨 */}
          <div>
            <h2 className="section-title">Top 5 급상승 트렌드</h2>
            <p className="section-subtitle">전월 대비 언급량 및 성장 실시간 추이</p>
          </div>
        </div>
      </div>

      <div className="trend-list-ultra">
        {displayTrends.map((trend, index) => {
          const change = Number(trend.change_rate);
          
          const colors = [
            { main: '#fbbf24', shadow: 'rgba(251, 191, 36, 0.5)' }, // 1위 골드
            { main: '#e2e8f0', shadow: 'rgba(226, 232, 240, 0.5)' }, // 2위 실버
            { main: '#fb923c', shadow: 'rgba(251, 146, 60, 0.5)' }, // 3위 브론즈
            { main: '#10b981', shadow: 'rgba(16, 185, 129, 0.5)' }, // 4위 그린
            { main: '#3b82f6', shadow: 'rgba(59, 130, 246, 0.5)' }, // 5위 블루
          ];
          const color = colors[index] || colors[3];

          return (
            <div 
              key={`${trend.name}-${index}`} 
              className={`trend-card-ultra rank-${index + 1}`}
              onClick={() => onTechClick?.(trend.tech_id)}
              style={{ cursor: onTechClick ? 'pointer' : 'default' }}
            >
              {/* 배경에 깔리는 고해상도 미니 차트 (Sparkline) - 높이 상향 */}
              <div className="sparkline-bg-ultra">
                <ResponsiveContainer width="100%" height={120}>
                  <AreaChart data={trend.timeline} margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
                    <defs>
                      <linearGradient id={`gradient-${index}`} x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor={color.main} stopOpacity={0.5}/>
                        <stop offset="100%" stopColor={color.main} stopOpacity={0}/>
                      </linearGradient>
                      <filter id={`glow-${index}`} x="-20%" y="-20%" width="140%" height="140%">
                        <feGaussianBlur stdDeviation="4" result="blur" />
                        <feComposite in="SourceGraphic" in2="blur" operator="over" />
                      </filter>
                    </defs>
                    <YAxis hide domain={['dataMin - 5', 'dataMax + 5']} />
                    <Area 
                      type="monotone" 
                      dataKey="mention_count" 
                      stroke={color.main} 
                      strokeWidth={4}
                      fillOpacity={1} 
                      fill={`url(#gradient-${index})`} 
                      filter={`url(#glow-${index})`}
                      isAnimationActive={true}
                      animationDuration={2000}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>

              <div className="trend-glass-overlay">
                <div className="trend-rank-hero-large">{index + 1}</div>
                
                <div className="trend-info-premium">
                  <div className="name-and-tag">
                    <span className="tech-name-rich">{trend.name}</span>
                    <span className={`premium-pill ${trend.category.toLowerCase().replace('/', '-')}`}>
                      {trend.category.replace('ai_ml', 'AI/ML').toUpperCase()}
                    </span>
                  </div>
                  {/* 뉴스 한 줄 요약 부분 삭제됨 */}
                </div>

                <div className="growth-score-box">
                  <div className="metric-pill" style={{ borderColor: color.shadow, background: `rgba(${parseInt(color.main.slice(1,3), 16)}, ${parseInt(color.main.slice(3,5), 16)}, ${parseInt(color.main.slice(5,7), 16)}, 0.1)` }}>
                    <span className="arrow">▲</span>
                    <span className="percentage">{Math.abs(change).toFixed(0)}%</span>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default TopTrends;
