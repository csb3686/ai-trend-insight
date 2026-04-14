import React from 'react';
import { Newspaper, GitBranch, Cpu, RefreshCw, Loader2 } from 'lucide-react';
import { useDashboardSummary } from '../../api/hooks/useTrends';
import './StatCards.css';

// 타입 갱신 확인 완료: DashboardStatsResponse 적용

const StatCards: React.FC = () => {
  const { data, isLoading, isError } = useDashboardSummary();

  if (isLoading) {
    return (
      <div className="stat-cards-grid">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="stat-card glass-panel loading-skeleton">
            <Loader2 className="animate-spin" size={24} color="var(--color-ai)" />
          </div>
        ))}
      </div>
    );
  }

  if (isError || !data) {
    return <div className="stat-error">통계 데이터를 불러올 수 없습니다.</div>;
  }

  return (
    <div className="stat-cards-grid">
      <div className="stat-card glass-panel">
        <div className="icon-wrapper bg-blue">
          <Newspaper size={20} color="var(--color-ai)" />
        </div>
        <div className="stat-value">{data.news_count.toLocaleString()}</div>
        <div className="stat-label">수집된 뉴스</div>
        <div className="stat-subtext">+ {data.updated_minutes_ago}m ago</div>
      </div>

      <div className="stat-card glass-panel">
        <div className="icon-wrapper bg-gray">
          <GitBranch size={20} color="#cbd5e1" />
        </div>
        <div className="stat-value">{data.github_count.toLocaleString()}</div>
        <div className="stat-label">GitHub 레포</div>
        <div className="stat-subtext">Active checking</div>
      </div>

      <div className="stat-card glass-panel">
        <div className="icon-wrapper bg-blue">
          <Cpu size={20} color="var(--color-ai)" />
        </div>
        <div className="stat-value">{data.tech_count.toLocaleString()}</div>
        <div className="stat-label">분석된 기술</div>
        <div className="stat-subtext">Keywords in DB</div>
      </div>

      <div className="stat-card glass-panel">
        <div className="icon-wrapper bg-blue">
          <RefreshCw size={20} color="var(--color-ai)" />
        </div>
        <div className="stat-value">{data.last_updated.split(' ')[1]}</div>
        <div className="stat-label">마지막 업데이트</div>
        <div className="stat-subtext">{data.last_updated.split(' ')[0]}</div>
      </div>
    </div>
  );
};

export default StatCards;
