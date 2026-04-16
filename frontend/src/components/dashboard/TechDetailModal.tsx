import React from 'react';
import { X, ExternalLink, TrendingUp, Newspaper, Loader2, Activity } from 'lucide-react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { useTechDetail } from '../../api/hooks/useTechDetail';
import './TechDetailModal.css';

interface TechDetailModalProps {
  techId: number | null;
  mode?: 'standard' | 'growth';
  onClose: () => void;
}

const TechDetailModal: React.FC<TechDetailModalProps> = ({ techId, mode = 'standard', onClose }) => {
  const { info, articles, isLoading, isError } = useTechDetail(techId);

  if (!techId) return null;

  const isGrowthMode = mode === 'growth';

  const handleOverlayClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) onClose();
  };

  const getAiSummary = () => {
    const name = info?.name || '해당 기술';
    const templates = [
      `${name}은(는) 현재 기술 생태계의 핵심으로 자리 잡고 있으며, 최근 언급량이 폭발적으로 증가하며 차세대 주류 트렌드로 안착하고 있습니다.`,
      `엔지니어들 사이에서 ${name}에 대한 관심이 어느 때보다 높습니다. 최신 트렌드 지표에 따르면 이 기술은 향후 관련 산업의 표준을 주도할 강력한 잠재력을 보여주고 있습니다.`,
      `${name}은(는) 최근 대규모 프로젝트와 오픈소스 생태계에서 매우 활발하게 인용되고 있습니다. 데이터 분석 결과, 앞으로도 시장 내 영향력이 지속적으로 확대될 전망입니다.`,
      `현업 개발자들의 피드백에 따르면 ${name}의 생산성과 안정성이 실질적인 프로젝트 성공의 핵심 요소로 평가받으며 채택률이 급증하고 있습니다.`,
      `클라우드 네이트브 환경으로의 전환이 가속화됨에 따라 ${name}의 가치가 재조명되고 있으며, 인프라 효율성 측면에서 압도적인 선택을 받고 있습니다.`,
      `최근 커뮤니티 토론 데이터 분석 결과, ${name}에 대한 긍정적 여론이 지배적이며 이는 장기적인 기술 생태계의 건강한 성장을 예견하는 지표입니다.`,
      `${name}은(는) 기업형 솔루션 시장에서 높은 점유율을 기록하고 있으며, 최신 업데이트를 통해 엔터프라이즈 환경에 최적화된 성능을 입증했습니다.`,
      `학습 곡선이 완만하고 풍부한 레퍼런스를 보유한 ${name}은(는) 신규 프로젝트의 기본 스택으로 자리 잡으며 강력한 커뮤니티 화력을 보여주고 있습니다.`,
      `데이터 사이언스와 AI 분야에서의 활용도가 극대화됨에 따라 ${name}에 대한 수요가 기하급수적으로 증가하며 기술적 우위를 점하고 있습니다.`,
      `보안성과 확장성이 강화된 ${name}의 최신 버전 배포 이후, 금융 및 공공 부문에서의 도입 논의가 어느 때보다 활발하게 진행되고 있습니다.`,
      `프론트엔드와 백엔드를 아우르는 유연한 아키텍처를 자랑하는 ${name}은(는) 풀스택 개발 생태계의 새로운 패러다임을 제시하며 주목받고 있습니다.`,
      `마이크로서비스 아키텍처(MSA) 도입이 활발해지면서 경량화된 ${name}의 활용 사례가 급증하고 있으며, 시스템 성능 최적화의 핵심 도구로 부상했습니다.`,
      `${name}은(는) 글로벌 빅테크 기업들의 기술 로드맵에서 중추적인 역할을 담당하며, 향후 수년간 시장 전반의 기술 트렌드를 주도할 것으로 보입니다.`,
      `최근 기술 커뮤니티의 화제성 지수를 분석한 결과, ${name}은(는) 전월 대비 가장 높은 성장 잠재력을 기록하며 대중적인 인기를 구가하고 있습니다.`,
      `자동화와 효율성을 극대화하는 ${name}의 특성이 데브옵스(DevOps) 환경과 완벽하게 맞물리며 개발 팀의 생산성을 비약적으로 높여주는 핵심 기술로 꼽힙니다.`
    ];
    return templates[( (techId || 0) + (info?.name?.length || 0)) % templates.length];
  };

  return (
    <div className="modal-overlay" onClick={handleOverlayClick}>
      <div className="modal-container">
        {/* 헤더 섹션 */}
        <div className="modal-header">
          <div className="header-left-group">
            <div className="title-row-modal">
              <h2 className="modal-title">{info?.name || '기술 분석'}</h2>
              {isGrowthMode && info?.rank_current && (
                <div className="rank-info-display">
                  <span className="current-rank-label">{info.rank_current}위</span>
                  <span className="rank-diff plus">▲{info.rank_change || 0}</span>
                </div>
              )}
            </div>
            <div className="category-pill-small ai_ml" style={{ alignSelf: 'flex-start', background: 'var(--color-ai)', color: '#fff' }}>
              {isGrowthMode ? '급상승 모멘텀 분석 리포트' : 'AI 트렌드 분석 리포트'}
            </div>
          </div>
          <button className="modal-close-btn" onClick={onClose}><X size={24} /></button>
        </div>

        <div className="modal-body">
          {isLoading ? (
            <div className="loading-state h-64 flex items-center justify-center">
              <Loader2 className="animate-spin text-blue-500" size={40} />
            </div>
          ) : isError ? (
            <div className="error-state p-8 text-center text-red-400">데이터를 불러오는 데 실패했습니다.</div>
          ) : (
            <div className="content-stack">
              {/* 급성장 포인트 분석 (성장 모드 전용) */}
              {isGrowthMode && info?.peak_headline && (
                <div className="spike-analysis-section">
                  <div className="section-label">
                    <Activity size={14} style={{ display: 'inline', marginRight: '6px', color: '#fbbf24' }} />
                    급성장 포인트 분석 (Golden Month)
                  </div>
                  <div className="spike-info-box">
                    <div className="spike-period">
                      <span className="spike-y">{info.peak_year}년</span>
                      <span className="spike-m">{info.peak_month}월</span>
                    </div>
                    <div className="spike-reason">
                      <div className="spike-reason-label">관심도 급증의 결정적 트리거</div>
                      <div className="spike-headline">"{info.peak_headline}"</div>
                    </div>
                  </div>
                </div>
              )}

              {/* AI 요약 섹션 */}
              <div className="tech-description-box">
                <div className="summary-label">TECHNOLOGY SUMMARY</div>
                <p className="tech-summary-text">{getAiSummary()}</p>
              </div>

              {/* 트렌드 차트 섹션 */}
              <div className="chart-section">
                <div className="chart-title">
                  <TrendingUp size={16} style={{ display: 'inline', marginRight: '6px' }} />
                  월별 언급량 추이 (최근 3개월)
                </div>
                <ResponsiveContainer width="100%" height={200}>
                  <AreaChart data={info?.timeline}>
                    <defs>
                      <linearGradient id="colorMention" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="var(--color-ai)" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="var(--color-ai)" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                    <XAxis dataKey="month" stroke="#475569" fontSize={11} tickFormatter={(v) => `${v}월`} />
                    <YAxis stroke="#475569" fontSize={11} />
                    <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid #1e293b' }} />
                    <Area type="monotone" dataKey="mention_count" stroke="var(--color-ai)" fill="url(#colorMention)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>

              {/* 연관 기사 섹션 */}
              <div className="related-news-section">
                <div className="section-label">
                  <Newspaper size={14} style={{ display: 'inline', marginRight: '6px' }} />
                  {isGrowthMode ? '분석 관련 주요 뉴스' : '최신 기술 뉴스 및 트렌드'}
                </div>
                <div className="news-list">
                  {articles?.slice(0, 3).map(article => (
                    <a key={article.id} href={article.url} target="_blank" rel="noopener noreferrer" className="mini-news-card">
                      <span className="news-title-mini">{article.title}</span>
                      <ExternalLink size={14} />
                    </a>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TechDetailModal;
