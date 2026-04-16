import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Shield, RefreshCw } from 'lucide-react';
import './AdminPotentialTech.css';

interface PendingTech {
  id: number;
  name: string;
  category: string;
  description: string;
  created_at: string;
}

interface Props {
  secret: string;
}

const AdminPotentialTech: React.FC<Props> = ({ secret }) => {
  const [pendingList, setPendingList] = useState<PendingTech[]>([]);
  const [stats, setStats] = useState<{total:number, embedded:number, percent:number} | null>(null);
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const API_BASE_URL = "http://localhost:8000/api/v1";

  // 시스템 통합 데이터(대기목록, 통계, 로그) 가져오기
  const fetchAdminData = async () => {
    if (!secret) return;
    setLoading(true);
    setErrorMsg(null);

    const config = { 
      headers: { 'x-admin-token': secret },
      timeout: 10000 
    };

    // 개별적으로 요청하여 하나가 실패해도 나머지는 표시되도록 함
    const fetchPending = async () => {
      try {
        const res = await axios.get(`${API_BASE_URL}/admin/pending-tech`, config);
        setPendingList(res.data);
      } catch (err: any) {
        console.error("Pending tech fetch failed", err);
        // 개별 에러는 콘솔에만 기록하거나 작은 표시만 남김
      }
    };

    const fetchStats = async () => {
      try {
        const res = await axios.get(`${API_BASE_URL}/admin/stats`, config);
        setStats(res.data);
      } catch (err: any) { console.error("Stats fetch failed", err); }
    };

    const fetchLogs = async () => {
      try {
        const res = await axios.get(`${API_BASE_URL}/admin/collection-logs`, config);
        setLogs(res.data);
      } catch (err: any) { console.error("Logs fetch failed", err); }
    };

    await Promise.allSettled([fetchPending(), fetchStats(), fetchLogs()]);
    setLoading(false);
  };

  useEffect(() => {
    fetchAdminData();
  }, [secret]);

  // 승인 처리
  const handleApprove = async (id: number) => {
    if (!window.confirm("이 기술을 정식 기술 풀에 등록하시겠습니까?")) return;
    try {
      await axios.post(`${API_BASE_URL}/admin/approve-tech/${id}`, {}, {
        headers: { 'x-admin-token': secret }
      });
      alert("정식 기술로 등록되었습니다! 🎉");
      fetchAdminData(); // 목록 및 통계 갱신
    } catch (err) {
      alert("승인 처리 중 오류 발생");
    }
  };

  // 거절 처리
  const handleReject = async (id: number) => {
    if (!window.confirm("이 후보를 삭제하시겠습니까?")) return;
    try {
      await axios.post(`${API_BASE_URL}/admin/reject-tech/${id}`, {}, {
        headers: { 'x-admin-token': secret }
      });
      alert("거절 처리되었습니다.");
      fetchAdminData(); // 목록 및 통계 갱신
    } catch (err) {
      alert("거절 처리 중 오류 발생");
    }
  };

  // 시스템 수동 작업 트리거 (수집, 임베딩, 통계, 리셋)
  const handleSystemTask = async (task: 'collect' | 'embed' | 'recompute-stats' | 'reset-db') => {
    const taskName = task === 'reset-db' ? '지식 저장소 리셋' : task;
    if (!window.confirm(`[${taskName}] 작업을 즉시 실행하시겠습니까?`)) return;
    
    try {
      const res = await axios.post(`${API_BASE_URL}/admin/${task}`, {}, {
        headers: { 'x-admin-token': secret }
      });
      alert(res.data.message);
      fetchAdminData(); // 로그 및 상태 갱신
    } catch (err) {
      alert("작업 요청 중 오류 발생");
    }
  };

  // 날짜 포맷팅 함수 (MM.DD HH:mm)
  const formatLogDate = (dateStr: string) => {
    const d = new Date(dateStr);
    const mm = String(d.getMonth() + 1).padStart(2, '0');
    const dd = String(d.getDate()).padStart(2, '0');
    const hh = String(d.getHours()).padStart(2, '0');
    const min = String(d.getMinutes()).padStart(2, '0');
    return `${mm}.${dd} ${hh}:${min}`;
  };

  if (!secret) return null;

  return (
    <section className="admin-tech-section glass-panel">
      <div className="admin-dashboard-header">
        <div className="header-left">
          <h2 className="admin-title">
            <Shield className="admin-shield-icon" size={20} fill="var(--color-ai)" />
            시스템 지휘 본부 (Cockpit 2.0)
          </h2>
          {stats && (
            <div className="stats-mini-panel">
              <div className="stat-pill">전체 뉴스: <strong>{stats.total}</strong></div>
              <div className="stat-pill">학습 완료: <strong>{stats.embedded}</strong> ({stats.percent}%)</div>
            </div>
          )}
        </div>
        <div className="admin-actions-group">
          <button onClick={() => handleSystemTask('collect')} className="control-btn collect">전체 수집</button>
          <button onClick={() => handleSystemTask('embed')} className="control-btn embed">AI 학습</button>
          <button onClick={() => handleSystemTask('recompute-stats')} className="control-btn stats">통계 갱신</button>
          <button onClick={fetchAdminData} className="refresh-btn">새로고침</button>
        </div>
      </div>

      {/* 실시간 상태 알림 바 (글로벌 로딩만 표시, 에러 배너는 카드 내부로 이동) */}
      {loading && (
        <div className="admin-loading-banner">
          <div className="spinner-mini"></div>
          <span>최신 데이터 동기화 중...</span>
        </div>
      )}

      <div className="admin-grid-layout">
        {/* 신기술 승인 대기열 */}
        <div className="admin-card pending-queue">
          <h3 className="card-title">🆕 신기술 승인 대기열 ({pendingList.length})</h3>
          <div className="tech-waitlist">
            {loading && pendingList.length === 0 ? (
              <div className="loading-state">데이터 분석 중...</div>
            ) : pendingList.length === 0 ? (
              <div className="empty-state-box">
                <p className="empty-msg">대기 중인 후보가 없습니다.</p>
                <p className="info-msg-sub">백엔드 응답이 지연될 수 있습니다.</p>
              </div>
            ) : (
             pendingList.map(tech => (
                <div key={tech.id} className="tech-item-card">
                  <div className="tech-info">
                    <span className={`category-tag ${tech.category.toLowerCase()}`}>
                      {tech.category.replace('ai_ml', 'AI/ML').replace('_', ' ').toUpperCase()}
                    </span>
                    <h3 className="tech-name">{tech.name}</h3>
                    <p className="tech-desc">{tech.description}</p>
                  </div>
                  <div className="tech-actions">
                    <button onClick={() => handleApprove(tech.id)} className="btn-approve">승인</button>
                    <button onClick={() => handleReject(tech.id)} className="btn-reject">거절</button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* 최근 시스템 로그 */}
        <div className="admin-card logs-panel">
          <h3 className="card-title">📝 최근 시스템 로그</h3>
          <div className="log-table-container">
            <table className="log-table">
              <thead>
                <tr>
                  <th>시각</th>
                  <th>작업</th>
                  <th>상태</th>
                </tr>
              </thead>
              <tbody>
                {logs.length === 0 ? (
                  <tr><td colSpan={3} className="empty-msg">로그가 없습니다.</td></tr>
                ) : (
                  logs.map(log => (
                    <React.Fragment key={log.id}>
                      <tr className={`status-${log.status.toLowerCase()}`}>
                        <td>{formatLogDate(log.start_time)}</td>
                        <td>
                          {log.task_type.toUpperCase() === 'COLLECT' ? '전체 수집' :
                           log.task_type.toUpperCase() === 'EMBED' ? 'AI 학습' :
                           log.task_type.toUpperCase() === 'RECOMPUTE-STATS' || log.task_type.toUpperCase() === 'STATS' ? '통계 갱신' : 
                           log.task_type.toUpperCase() === 'RESET-DB' ? '저장소 리셋' : log.task_type}
                        </td>
                        <td>
                          {log.status === 'SUCCESS' ? '✅' : (
                          <div className="status-fail-row">
                            <span>❌</span>
                          </div>
                        )}
                       </td>
                      </tr>
                    </React.Fragment>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* 위험 구역 */}
      <div className="danger-zone">
        <h3 className="danger-title">⚠️ 위험 구역 (Danger Zone)</h3>
        <p className="danger-desc">모델 불일치나 검색 오류 발생 시 지식 저장소를 초기화해야 합니다.</p>
        <button onClick={() => handleSystemTask('reset-db')} className="btn-reset-db">벡터 DB 초기화 및 전체 재학습 예약</button>
      </div>
    </section>
  );
};

export default AdminPotentialTech;
