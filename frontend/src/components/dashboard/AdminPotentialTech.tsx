import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Shield, Loader2 } from 'lucide-react';
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
  const pollingRef = useRef<NodeJS.Timeout | null>(null);

  const API_BASE_URL = "http://localhost:8000/api/v1";

  // 현재 진행 중인 작업 찾기
  const activeTask = logs.find(log => log.status === 'IN_PROGRESS');

  const fetchAdminData = async (isSilent = false) => {
    if (!secret) return;
    if (!isSilent) setLoading(true);

    const config = { 
      headers: { 'x-admin-token': secret },
      timeout: 10000 
    };

    const fetchPending = async () => {
      try {
        const res = await axios.get(`${API_BASE_URL}/admin/pending-tech`, config);
        setPendingList(res.data);
      } catch (err: any) { console.error("Pending tech fetch failed", err); }
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
    if (!isSilent) setLoading(false);
  };

  // 실시간 모니터링 폴링 로직
  useEffect(() => {
    if (activeTask) {
      if (!pollingRef.current) {
        console.log(">>> [Polling] Start monitoring active task...");
        pollingRef.current = setInterval(() => {
          fetchAdminData(true); // 배경에서 조용히 업데이트
        }, 2000);
      }
    } else {
      if (pollingRef.current) {
        console.log("<<< [Polling] Task finished. Stopping...");
        clearInterval(pollingRef.current);
        pollingRef.current = null;
        fetchAdminData(true); // 최종 상태 동기화
      }
    }

    return () => {
      if (pollingRef.current) {
        clearInterval(pollingRef.current);
        pollingRef.current = null;
      }
    };
  }, [activeTask]);

  useEffect(() => {
    fetchAdminData();
  }, [secret]);

  const handleApprove = async (id: number) => {
    if (!window.confirm("이 기술을 정식 기술 풀에 등록하시겠습니까?")) return;
    try {
      await axios.post(`${API_BASE_URL}/admin/approve-tech/${id}`, {}, {
        headers: { 'x-admin-token': secret }
      });
      alert("정식 기술로 등록되었습니다! 🎉");
      fetchAdminData();
    } catch (err) { alert("승인 처리 중 오류 발생"); }
  };

  const handleReject = async (id: number) => {
    if (!window.confirm("이 후보를 삭제하시겠습니까?")) return;
    try {
      await axios.post(`${API_BASE_URL}/admin/reject-tech/${id}`, {}, {
        headers: { 'x-admin-token': secret }
      });
      alert("거절 처리되었습니다.");
      fetchAdminData();
    } catch (err) { alert("거절 처리 중 오류 발생"); }
  };

  const handleSystemTask = async (task: 'collect' | 'embed' | 'recompute-stats' | 'reset-db') => {
    if (activeTask) {
      alert("이미 진행 중인 작업이 있습니다. 잠시만 기다려 주세요.");
      return;
    }
    const taskName = task === 'reset-db' ? '지식 저장소 리셋' : task;
    if (!window.confirm(`[${taskName}] 작업을 즉시 실행하시겠습니까?`)) return;
    try {
      const res = await axios.post(`${API_BASE_URL}/admin/${task}`, {}, {
        headers: { 'x-admin-token': secret }
      });
      alert(res.data.message);
      fetchAdminData();
    } catch (err) { alert("작업 요청 중 오류 발생"); }
  };

  const formatLogDate = (dateStr: string) => {
    const d = new Date(dateStr);
    const mm = String(d.getMonth() + 1).padStart(2, '0');
    const dd = String(d.getDate()).padStart(2, '0');
    const hh = String(d.getHours()).padStart(2, '0');
    const min = String(d.getMinutes()).padStart(2, '0');
    return `${mm}.${dd} ${hh}:${min}`;
  };

  const getButtonText = (type: string, defaultText: string) => {
    if (activeTask && activeTask.task_type === type) {
      return `${defaultText} (${activeTask.progress || 0}%)`;
    }
    return defaultText;
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
          <button 
            onClick={() => handleSystemTask('collect')} 
            className={`control-btn collect ${activeTask?.task_type === 'COLLECT' ? 'processing' : ''}`}
            disabled={!!activeTask}
          >
            {activeTask?.task_type === 'COLLECT' && <Loader2 className="animate-spin" size={14} />}
            {getButtonText('COLLECT', '전체 수집')}
          </button>
          <button 
            onClick={() => handleSystemTask('embed')} 
            className={`control-btn embed ${activeTask?.task_type === 'EMBED' ? 'processing' : ''}`}
            disabled={!!activeTask}
          >
            {activeTask?.task_type === 'EMBED' && <Loader2 className="animate-spin" size={14} />}
            {getButtonText('EMBED', 'AI 학습')}
          </button>
          <button 
            onClick={() => handleSystemTask('recompute-stats')} 
            className={`control-btn stats ${activeTask?.task_type === 'STATS' ? 'processing' : ''}`}
            disabled={!!activeTask}
          >
            {activeTask?.task_type === 'STATS' && <Loader2 className="animate-spin" size={14} />}
            {getButtonText('STATS', '통계 갱신')}
          </button>
          <button onClick={() => fetchAdminData()} className="refresh-btn" disabled={loading}>새로고침</button>
        </div>
      </div>

      {loading && !activeTask && (
        <div className="admin-loading-banner">
          <div className="spinner-mini"></div>
          <span>최신 데이터 동기화 중...</span>
        </div>
      )}

      <div className="admin-grid-layout">
        <div className="admin-card pending-queue">
          <h3 className="card-title">🆕 신기술 승인 대기열 ({pendingList.length})</h3>
          <div className="tech-waitlist">
            {pendingList.length === 0 ? (
              <div className="empty-state-box"><p className="empty-msg">대기 중인 후보가 없습니다.</p></div>
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

        <div className="admin-card logs-panel">
          <h3 className="card-title">📝 최근 시스템 로그</h3>
          <div className="log-table-container">
            <table className="log-table">
              <thead>
                <tr><th>시각</th><th>작업</th><th>상태</th></tr>
              </thead>
              <tbody>
                {logs.length === 0 ? (
                  <tr><td colSpan={3} className="empty-msg">로그가 없습니다.</td></tr>
                ) : (
                  logs.map(log => (
                    <tr key={log.id} className={`status-${log.status.toLowerCase()}`}>
                      <td>{formatLogDate(log.start_time)}</td>
                      <td>{log.task_type.toUpperCase()}</td>
                      <td>
                        {log.status === 'SUCCESS' ? '✅' : 
                         log.status === 'IN_PROGRESS' ? (
                           <div className="progress-cell">
                             <div className="spinner-tiny"></div>
                             <span>{log.progress || 0}%</span>
                           </div>
                         ) : '❌'}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div className="danger-zone">
        <h3 className="danger-title">⚠️ 위험 구역 (Danger Zone)</h3>
        <button onClick={() => handleSystemTask('reset-db')} className="btn-reset-db" disabled={!!activeTask}>벡터 DB 초기화 및 전체 재학습 예약</button>
      </div>
    </section>
  );
};

export default AdminPotentialTech;
