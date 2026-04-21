import React, { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import cytoscape from 'cytoscape';
import Header from '../components/layout/Header';
import { Loader2, Maximize2, RefreshCw, ArrowLeft } from 'lucide-react';
import './EcosystemPage.css';

const EcosystemPage: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyInstance = useRef<any>(null);
  const pulseInterval = useRef<any>(null);
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 전설의 6fc1570 네온 컬러 팔레트
  const natureColors: any = {
    'ai_ml': '#60a5fa',       // Sky Blue
    'language': '#34d399',    // Emerald Green
    'framework': '#a78bfa',   // Soft Purple
    'devops': '#fb923c',      // Bright Orange
    'database': '#fbbf24',    // Amber
    'cloud': '#2dd4bf'         // Teal
  };

  const initGraph = (nodes: any[], edges: any[]) => {
    console.log('--- [PROPER RECOVERY] Graph Initializing ---');
    if (!containerRef.current) return;

    // [철벽 방어] 이중 널 체크 및 배열 강제 할당
    const safeNodes = Array.isArray(nodes) ? nodes : [];
    const safeEdges = Array.isArray(edges) ? edges : [];

    if (cyInstance.current) {
      cyInstance.current.destroy();
    }
    if (pulseInterval.current) {
      clearInterval(pulseInterval.current);
    }

    try {
      const nodeMap: any = {};
      
      // [안정성] 전통적인 for 루프 사용
      for (let i = 0; i < safeNodes.length; i++) {
        const n = safeNodes[i];
        if (n && n.data) {
          n.data.degree = 0;
          nodeMap[n.data.id] = n;
        }
      }

      for (let j = 0; j < safeEdges.length; j++) {
        const e = safeEdges[j];
        if (e && e.data && nodeMap[e.data.source] && nodeMap[e.data.target]) {
          nodeMap[e.data.source].data.degree++;
          nodeMap[e.data.target].data.degree++;
        }
      }

      const cy = cytoscape({
        container: containerRef.current,
        elements: { nodes: safeNodes, edges: safeEdges },
        style: [
          {
            selector: 'node',
            style: {
              'label': 'data(name)',
              'width': (ele: any) => 280 + (ele.data('degree') * 10), // 240 -> 280 대폭 확장
              'height': (ele: any) => 280 + (ele.data('degree') * 10),
              'background-color': '#111827',
              'border-width': 5,
              'border-color': (ele: any) => natureColors[ele.data('category')] || '#64748b',
              'color': '#fff',
              'font-size': (ele: any) => Math.min(80, 44 + (ele.data('degree') * 3)), // 36 -> 44 시작 (최대 80px)
              'font-family': 'Inter, system-ui, sans-serif',
              'font-weight': 800,
              'text-valign': 'center',
              'text-halign': 'center',
              'text-wrap': 'wrap',
              'text-max-width': (ele: any) => ((280 + (ele.data('degree') * 10)) * 0.72) + 'px', // 80% -> 72%로 더 좁혀서 원형 안착 유도
            }
          },
          {
            selector: 'node[degree > 8]', // 핵심 허브 강조
            style: {
              'border-width': 8,
              'font-weight': 900,
              'border-color': (ele: any) => natureColors[ele.data('category')] || '#ffffff',
            }
          },
          {
            selector: 'edge',
            style: {
              'width': (ele: any) => 3 + (Math.sqrt(ele.data('weight') || 1) * 3), // 연관성 선도 더 굵게
              'line-color': '#475569',
              'line-opacity': 0.5,
              'curve-style': 'bezier',
              'target-arrow-shape': 'triangle',
              'target-arrow-color': '#94a3b8',
              'arrow-scale': 2
            }
          },
          {
            selector: '.highlighted',
            style: {
              'border-width': 12,
              'border-color': '#3b82f6',
              'line-opacity': 1,
              'line-color': '#3b82f6',
              'target-arrow-color': '#3b82f6',
              'z-index': 999,
              'transition-property': 'border-width, border-color, line-color, line-opacity',
              'transition-duration': 300
            }
          },
          {
            selector: '.faded',
            style: {
              'opacity': 0.1,
              'text-opacity': 0
            }
          }
        ],
        layout: {
          name: 'cose',
          animate: true,
          nodeRepulsion: 400000, // 광활한 우주 배치를 위한 강력한 반발력
          idealEdgeLength: 500,  // 넓찍한 간격 확보
          gravity: 0.01,         // 거의 없는 중력으로 화면 가득 뻗어나가게 함
          nodeOverlap: 200,      // 노드가 커진 만큼 겹침 방지 강도도 극대화
          refresh: 20,
          componentSpacing: 250
        },
        wheelSensitivity: 0.2
      });

      cyInstance.current = cy;

      // [인터랙션] 탭(Tap) 시 인접 노드 강조 복구
      cy.on('tap', 'node', (e: any) => {
        const node = e.target;
        const neighborhood = node.neighborhood().add(node);
        cy.elements().addClass('faded');
        neighborhood.removeClass('faded').addClass('highlighted');
      });

      cy.on('tap', (e: any) => {
        if (e.target === cy) {
          cy.elements().removeClass('faded highlighted');
        }
      });

    } catch (err) {
      console.error('Graph critical error:', err);
      setError('시각화 엔진 복구 중 오류 발생: ' + String(err));
    }
  };

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      // [안정성] 프록시 경로 사용
      const response = await axios.get('/api/v1/analysis/tech-ecosystem');
      console.log('[PROPER] Ecosystem data received:', response.data);
      initGraph(response.data.nodes || [], response.data.edges || []);
    } catch (err) {
      console.error('Fetch Error:', err);
      setError('데이터를 불러올 수 없습니다. 서버 상태를 확인해 주세요.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    return () => {
      if (cyInstance.current) cyInstance.current.destroy();
    };
  }, []);

  return (
    <div className="app-container ecosystem-page-root natural-theme">
      <div className="main-content page-container ecosystem-layout">
        <Header />
        
        <div className="ecosystem-top-bar">
          <button className="back-btn-clean" onClick={() => navigate('/')}>
            <ArrowLeft size={16} />
            <span>DASHBOARD</span>
          </button>
          
          <div className="ecosystem-info-card-clean">
            <div className="info-text-clean">
              <h1 className="clean-title">Technology Ecosystem Map</h1>
              <p>Visualizing the interconnected world of modern software development</p>
            </div>
          </div>

          <div className="ecosystem-actions">
            <button className="clean-icon-btn" onClick={() => cyInstance.current?.fit()} title="Fitting View">
              <Maximize2 size={18} />
            </button>
            <button className="clean-icon-btn" onClick={fetchData} title="Rescan Hubs">
              <RefreshCw size={18} />
            </button>
          </div>
        </div>

        <section className="graph-theater-section-clean">
          {loading && (
            <div className="graph-overlay-loader-clean">
              <Loader2 className="animate-spin" size={60} />
              <p>ANALYZING ECOSYSTEM...</p>
            </div>
          )}
          
          {error && (
            <div className="graph-overlay-loader-clean text-red-400">
              <p>{error}</p>
              <button className="back-btn-clean mt-4" onClick={fetchData}>다시 시도</button>
            </div>
          )}

          <div className="cytoscape-container" ref={containerRef}></div>
          
          <div className="graph-floating-footer-clean">
            <div className="category-legend-clean">
              <div className="leg-item-clean"><span className="color-dot ai"></span> AI & Machine Learning</div>
              <div className="leg-item-clean"><span className="color-dot language"></span> Languages</div>
              <div className="leg-item-clean"><span className="color-dot framework"></span> Frameworks</div>
              <div className="leg-item-clean"><span className="color-dot devops"></span> DevOps & Ops</div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default EcosystemPage;
