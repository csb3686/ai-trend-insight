import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import Header from '../components/layout/Header';
import StatCards from '../components/dashboard/StatCards';
import TechHeatmap from '../components/dashboard/TechHeatmap';
import TopTrends from '../components/dashboard/TopTrends';
import NewsFeed from '../components/dashboard/NewsFeed';
import AdminPotentialTech from '../components/dashboard/AdminPotentialTech';
import './DashboardPage.css';

const DashboardPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const [isAdmin, setIsAdmin] = useState(false);
  
  // 보안 토큰 ( .env의 ADMIN_TOKEN과 동기화 )
  const ADMIN_SECRET = "antigravity_master_key_2024";

  useEffect(() => {
    const secret = searchParams.get('secret');
    if (secret === ADMIN_SECRET) {
      console.log("🛡️ 관리자 모드 활성화됨");
      setIsAdmin(true);
    }
  }, [searchParams]);

  return (
    <div className="app-container">
      <div className="main-content page-container">
        <Header />
        
        <main>
          <StatCards />
          <TechHeatmap isAdmin={isAdmin} />
          
          <div className="dashboard-bottom-grid">
            <TopTrends />
            <NewsFeed />
          </div>

          {/* 관리자 모드일 때만 나타나는 비밀 섹션 */}
          {isAdmin && <AdminPotentialTech secret={ADMIN_SECRET} />}
        </main>
      </div>
    </div>
  );
};

export default DashboardPage;
