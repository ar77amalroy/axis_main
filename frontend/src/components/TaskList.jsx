import { useState, useEffect, useRef } from "react";
import api from "../api";

export default function TaskList({ tasks, onTasksChange }) {
  const [expandedId, setExpandedId] = useState(null);
  const [steps, setSteps] = useState([]);
  const [loadingSteps, setLoadingSteps] = useState(false);
  const intervalRef = useRef(null);

  const formatDate = (iso) =>
    new Date(iso).toLocaleString(undefined, {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });

  // Poll steps every 2s while expanded task is pending/running
  useEffect(() => {
    clearInterval(intervalRef.current);
    if (!expandedId) return;

    const task = tasks.find((t) => t.id === expandedId);
    if (!task || (task.status !== "pending" && task.status !== "running")) return;

    intervalRef.current = setInterval(async () => {
      try {
        const { data } = await api.get(`/tasks/${expandedId}/steps`);
        setSteps(data);
      } catch {
        /* ignore */
      }
      if (onTasksChange) onTasksChange();
    }, 2000);

    return () => clearInterval(intervalRef.current);
  }, [expandedId, tasks, onTasksChange]);

  const handleClick = async (task) => {
    if (expandedId === task.id) {
      setExpandedId(null);
      setSteps([]);
      return;
    }
    setExpandedId(task.id);
    setLoadingSteps(true);
    try {
      const { data } = await api.get(`/tasks/${task.id}/steps`);
      setSteps(data);
    } catch {
      setSteps([]);
    } finally {
      setLoadingSteps(false);
    }
  };

  return (
    <section className="task-list">
      <h2>Task History</h2>
      {tasks.length === 0 ? (
        <p className="empty">No tasks yet. Describe something above to get started.</p>
      ) : (
        tasks.map((t) => (
          <div key={t.id}>
            <div
              className={`task-card ${expandedId === t.id ? "expanded" : ""}`}
              onClick={() => handleClick(t)}
              style={{ cursor: "pointer" }}
            >
              <div className="task-info">
                <div className="command">{t.command_text}</div>
                <div className="meta">
                  {formatDate(t.created_at)} · {t.input_mode}
                  {t.file_ids.length > 0 && ` · ${t.file_ids.length} file(s)`}
                </div>
              </div>
              <span className={`status-badge ${t.status}`}>{t.status}</span>
            </div>

            {expandedId === t.id && (
              <div className="step-list">
                {loadingSteps ? (
                  <div className="step-loading">Loading steps…</div>
                ) : steps.length === 0 ? (
                  <div className="step-empty">No steps yet.</div>
                ) : (
                  steps.map((s) => (
                    <div className="step-card" key={s.id}>
                      <div className="step-header">
                        <span className="step-agent">{s.agent}</span>
                        <span className={`status-badge ${s.status}`}>{s.status}</span>
                      </div>
                      <div className="step-instruction">{s.instruction}</div>
                      {s.result && (
                        <div className="step-result">{s.result}</div>
                      )}
                    </div>
                  ))
                )}
              </div>
            )}
          </div>
        ))
      )}
    </section>
  );
}
