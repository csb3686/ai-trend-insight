import React from 'react';
import { techHeatmapData } from '../../mocks/dashboardData';
import './TechHeatmap.css';

const TechHeatmap: React.FC = () => {
  return (
    <div className="section-container glass-panel">
      <div className="section-header">
        <div>
          <h2 className="section-title">기술 스택 히트맵</h2>
          <p className="section-subtitle">이번달 가장 많이 언급된 기술 Top 10</p>
        </div>
        <div className="legend-container">
          <div className="legend-item"><span className="legend-dot ai"></span>AI/ML</div>
          <div className="legend-item"><span className="legend-dot frontend"></span>Frontend</div>
          <div className="legend-item"><span className="legend-dot devops"></span>DevOps</div>
          <div className="legend-item"><span className="legend-dot backend"></span>Backend</div>
          <div className="legend-item"><span className="legend-dot data"></span>Data</div>
        </div>
      </div>

      <div className="heatmap-grid">
        {techHeatmapData.map((tech, index) => {
          let className = "heatmap-item";
          // 카테고리별 클래스
          if (tech.category === 'AI/ML') className += " ai";
          if (tech.category === 'Frontend') className += " frontend";
          if (tech.category === 'Backend') className += " backend";
          if (tech.category === 'DevOps') className += " devops";
          if (tech.category === 'Data') className += " data";

          // 순위별 크기 (1,2위는 크게, 나머지는 일반)
          if (index === 0) className += " large";
          if (index === 1) className += " medium";

          return (
            <div key={tech.id} className={className}>
              <div className="heatmap-content">
                <div className="heatmap-name">{tech.name}</div>
                <div className="heatmap-value">
                  {tech.mentions.toLocaleString()} <span className="heatmap-unit">mentions</span>
                </div>
                <div className="heatmap-category">{tech.category}</div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default TechHeatmap;
