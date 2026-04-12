import React from 'react';
import Header from '../components/layout/Header';
import StatCards from '../components/dashboard/StatCards';
import TechHeatmap from '../components/dashboard/TechHeatmap';
import TopTrends from '../components/dashboard/TopTrends';
import NewsFeed from '../components/dashboard/NewsFeed';
import './DashboardPage.css';

const DashboardPage: React.FC = () => {
  return (
    <div className="app-container">
      <div className="main-content page-container">
        <Header />
        
        <main>
          <StatCards />
          <TechHeatmap />
          
          <div className="dashboard-bottom-grid">
            <TopTrends />
            <NewsFeed />
          </div>
        </main>
      </div>
    </div>
  );
};

export default DashboardPage;
