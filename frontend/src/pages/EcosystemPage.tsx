import React, { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import cytoscape from 'cytoscape';
import Header from '../components/layout/Header';
import { Loader2, Maximize2, RefreshCw, ArrowLeft, Activity, Compass } from 'lucide-react';
import './EcosystemPage.css';

const EcosystemPage: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyInstance = useRef<any>(null);
  const pulseInterval = useRef<any>(null);
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const natureColors: any = {
    'ai_ml': '#60a5fa',       // Sky Blue
    'language': '#34d399',    // Emerald Green
    'framework': '#a78bfa',   // Soft Purple
    'devops': '#fb923c',      // Bright Orange
    'database': '#fbbf24',    // Amber
    'cloud': '#2dd4bf'         // Teal
  };

  const initGraph = (nodes: any[], edges: any[]) => {
    if (!containerRef.current) return;

    if (cyInstance.current) {
      cyInstance.current.destroy();
    }
    if (pulseInterval.current) {
      clearInterval(pulseInterval.current);
    }

    try {
      const nodeMap: any = {};
      nodes.forEach((n: any) => {
        n.data.degree = 0;
        nodeMap[n.data.id] = n;
      });
      edges.forEach((e: any) => {
        if (nodeMap[e.data.source]) nodeMap[e.data.source].data.degree++;
        if (nodeMap[e.data.target]) nodeMap[e.data.target].data.degree++;
      });

      const cy = cytoscape({
        container: containerRef.current,
        elements: { nodes, edges },
        style: [
          {
            selector: 'node',
            style: {
              'label': 'data(name)',
              'width': (ele: any) => 150 + (ele.data('degree') * 5), // 공간 넉넉히 확보
              'height': (ele: any) => 150 + (ele.data('degree') * 5),
              'background-color': '#111827',
              'border-width': 3,
              'border-color': (ele: any) => natureColors[ele.data('category')] || '#64748b',
              'color': '#fff',
              'font-size': 24, // 18px -> 24px로 상향
              'font-family': 'Inter, system-ui, sans-serif',
              'font-weight': '700',
              'text-valign': 'center',
              'text-halign': 'center',
              'text-wrap': 'wrap',
              'text-max-width': '120px', // 글자 크기에 맞춰 더 넓게 가둠
              'text-outline-width': 0,
            }
          },
          {
            selector: 'node[degree > 8]',
            style: {
              'border-width': 5,
              'font-size': 32, // 24px -> 32px로 상향
              'font-weight': '900',
            }
          },
          {
            selector: 'edge',
            style: {
              'width': (ele: any) => 2 + (Math.sqrt(ele.data('weight')) * 1.5),
              'line-color': '#475569',
              'line-opacity': 0.8,
              'curve-style': 'bezier',
              'target-arrow-shape': 'triangle',
              'target-arrow-color': '#94a3b8',
              'arrow-scale': 1.5
            }
          },
          {
            selector: '.highlighted',
            style: {
              'border-width': 8,
              'border-color': '#3b82f6',
              'line-opacity': 1,
              'line-color': '#3b82f6',
              'target-arrow-color': '#3b82f6',
              'z-index': 999
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
          nodeRepulsion: 30000,
          idealEdgeLength: 150,
        }
      });

      cyInstance.current = cy;

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
      setError('시각화 엔진 초기화 중 오류가 발생했습니다.');
    }
  };

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/v1/analysis/tech-ecosystem');
      initGraph(response.data.nodes, response.data.edges);
    } catch (err) {
      setError('데이터를 불러올 수 없습니다.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    return () => {
      if (cyInstance.current) cyInstance.current.destroy();
      if (pulseInterval.current) clearInterval(pulseInterval.current);
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
              <Loader2 className="animate-spin text-blue-500" size={60} />
              <p>ANALYZING ECOSYSTEM...</p>
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
