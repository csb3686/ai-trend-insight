import React from 'react';
import { Newspaper, GitBranch, Cpu, RefreshCw } from 'lucide-react';
import { dashboardStats } from '../../mocks/dashboardData';
import './StatCards.css';

const StatCards: React.FC = () => {
  return (
    <div className="stat-cards-grid">
      <div className="stat-card glass-panel">
        <div className="icon-wrapper bg-blue">
          <Newspaper size={20} color="var(--color-ai)" />
        </div>
        <div className="stat-value">{dashboardStats.newsCount.toLocaleString()}</div>
        <div className="stat-label">수집된 뉴스</div>
        <div className="stat-subtext">+ {dashboardStats.newsAddedToday} today</div>
      </div>

      <div className="stat-card glass-panel">
        <div className="icon-wrapper bg-gray">
          <GitBranch size={20} color="#cbd5e1" />
        </div>
        <div className="stat-value">{dashboardStats.githubRepos.toLocaleString()}</div>
        <div className="stat-label">GitHub 레포</div>
        <div className="stat-subtext">+ {dashboardStats.githubAddedToday} today</div>
      </div>

      <div className="stat-card glass-panel">
        <div className="icon-wrapper bg-blue">
          <Cpu size={20} color="var(--color-ai)" />
        </div>
        <div className="stat-value">{dashboardStats.analyzedTechs.toLocaleString()}</div>
        <div className="stat-label">분석된 기술</div>
        <div className="stat-subtext">+ {dashboardStats.techsAddedThisWeek} this week</div>
      </div>

      <div className="stat-card glass-panel">
        <div className="icon-wrapper bg-blue">
          <RefreshCw size={20} color="var(--color-ai)" />
        </div>
        <div className="stat-value">{dashboardStats.lastUpdated}</div>
        <div className="stat-label">오늘 업데이트</div>
        <div className="stat-subtext">{dashboardStats.updatedMinutesAgo}분 전</div>
      </div>
    </div>
  );
};

export default StatCards;
