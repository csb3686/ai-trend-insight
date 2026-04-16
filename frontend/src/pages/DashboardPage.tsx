import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import Header from '../components/layout/Header';
import StatCards from '../components/dashboard/StatCards';
import TechHeatmap from '../components/dashboard/TechHeatmap';
import TopTrends from '../components/dashboard/TopTrends';
import NewsFeed from '../components/dashboard/NewsFeed';
import AdminPotentialTech from '../components/dashboard/AdminPotentialTech';
import TechDetailModal from '../components/dashboard/TechDetailModal';
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

  const [selectedTechId, setSelectedTechId] = useState<number | null>(null);
  const [modalMode, setModalMode] = useState<'standard' | 'growth'>('standard');

  const handleOpenStandard = (techId: number) => {
    setModalMode('standard');
    setSelectedTechId(techId);
  };

  const handleOpenGrowth = (techId: number) => {
    setModalMode('growth');
    setSelectedTechId(techId);
  };

  return (
    <div className="app-container">
      <div className="main-content page-container">
        <Header isAdmin={isAdmin} />
        
        <main>
          <StatCards />
          <TechHeatmap isAdmin={isAdmin} onTechClick={handleOpenStandard} />
          
          <div className="dashboard-bottom-grid">
            <TopTrends onTechClick={handleOpenGrowth} />
            <NewsFeed />
          </div>

          {/* 관리자 모드일 때만 나타나는 비밀 섹션 */}
          {isAdmin && <AdminPotentialTech secret={ADMIN_SECRET} />}
        </main>
      </div>

      {/* [최상위 레이어] 기술 상세 딥다이버 모달 */}
      <TechDetailModal 
        techId={selectedTechId} 
        mode={modalMode}
        onClose={() => setSelectedTechId(null)} 
      />
    </div>
  );
};

export default DashboardPage;
