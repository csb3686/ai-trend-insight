import React from 'react';
import { NavLink } from 'react-router-dom';
import { Radar, TrendingUp, Newspaper, Shield } from 'lucide-react';
import './Header.css';

interface HeaderProps {
  isAdmin?: boolean;
}

const Header: React.FC<HeaderProps> = ({ isAdmin }) => {
  return (
    <header className="app-header glass-panel">
      <div className="logo-container">
        <Radar className="logo-icon" size={28} color="var(--color-ai)" />
        <h1 className="logo-text">TrendRadar</h1>
        {isAdmin && (
          <div className="admin-status-badge">
            <Shield size={12} fill="currentColor" />
            <span>ADMIN MODE</span>
          </div>
        )}
      </div>
      
      <nav className="nav-links">
        <NavLink 
          to="/" 
          className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}
        >
          <TrendingUp size={18} />
          <span>트렌드</span>
        </NavLink>
        <NavLink 
          to="/news" 
          className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}
        >
          <Newspaper size={18} />
          <span>뉴스</span>
        </NavLink>
      </nav>
    </header>
  );
};

export default Header;
