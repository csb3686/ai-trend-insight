import React from 'react';
import { Loader2 } from 'lucide-react';
import { useTrendHeatmap } from '../../api/hooks/useTrends';
import './TechHeatmap.css';

interface Props {
  isAdmin?: boolean;
  onTechClick: (techId: number) => void;
}

const TechHeatmap: React.FC<Props> = ({ isAdmin, onTechClick }) => {
  const { data: heatmapRes, isLoading, isError } = useTrendHeatmap();

  if (isLoading) {
    return (
      <div className="section-container glass-panel flex-center p-8">
        <Loader2 className="animate-spin" size={40} color="var(--color-ai)" />
        <p className="mt-4 text-gray-400">최신 기술 지도를 그리는 중...</p>
      </div>
    );
  }

  if (isError || !heatmapRes) {
    return <div className="section-container glass-panel flex-center">트렌드 데이터를 불러올 수 없습니다.</div>;
  }

  const heatmapData = heatmapRes.data.slice(0, 10); // 상위 10개만 표시

  return (
    <div className="section-container glass-panel">
      <div className="section-header">
        <div>
          <div className="title-row">
            <h2 className="section-title">기술 스택 히트맵</h2>
          </div>
          <p className="section-subtitle">
            {heatmapRes.year || new Date().getFullYear()}년 {heatmapRes.month || new Date().getMonth() + 1}월 가장 많이 언급된 기술 Top 10
          </p>
        </div>
        <div className="legend-container">
          <div className="legend-item"><span className="legend-dot ai"></span>AI/ML</div>
          <div className="legend-item"><span className="legend-dot frontend"></span>Frontend</div>
          <div className="legend-item"><span className="legend-dot backend"></span>Backend</div>
          <div className="legend-item"><span className="legend-dot devops"></span>DevOps</div>
          <div className="legend-item"><span className="legend-dot data"></span>Data</div>
          <div className="legend-item"><span className="legend-dot language"></span>Language</div>
          <div className="legend-item"><span className="legend-dot framework"></span>Framework</div>
          <div className="legend-item"><span className="legend-dot other"></span>OTHERS</div>
        </div>
      </div>

      <div className="heatmap-grid">
        {heatmapData.map((tech, index) => {
          let className = "heatmap-item";
          // 카테고리별 클래스
          const categoryLower = tech.category.toLowerCase().trim();
          
          if (categoryLower === 'ai/ml' || categoryLower === 'ai_ml' || categoryLower.includes('ai')) className += " ai";
          else if (categoryLower.includes('frontend')) className += " frontend";
          else if (categoryLower.includes('backend')) className += " backend";
          else if (categoryLower.includes('devops')) className += " devops";
          else if (categoryLower.includes('data') || categoryLower.includes('database')) className += " data";
          else if (categoryLower.includes('language')) className += " language";
          else if (categoryLower.includes('framework')) className += " framework";
          else className += " other"; // 위 도메인에 해당하지 않으면 기타(다크그레이) 처리

          // 순위 기반 농도 조절 (1위가 1.0, 10위로 갈수록 옅어짐)
          const opacity = 1.0 - (index * 0.07); // 0.3 ~ 1.0 범위 조절

          return (
            <div 
              key={tech.tech_id} 
              className={className}
              style={{ opacity: opacity, cursor: 'pointer' }}
              onClick={() => onTechClick(tech.tech_id)}
            >
              <div className="card-rank">{index + 1}위</div>
              
              <div className="card-center">
                <h3 className="tech-name-large">{tech.name}</h3>
                <div className="mention-stats-center">
                  <span className="mention-value-small">{tech.mention_count.toLocaleString()}</span>
                  <span className="mention-unit-small">mentions</span>
                </div>
              </div>

              <div className="card-footer-tag">
                <span className="category-pill">
                  {tech.category.replace('ai_ml', 'AI/ML').replace('_', ' ').toUpperCase()}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default TechHeatmap;
