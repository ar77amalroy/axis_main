import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import TaskInput from "../components/TaskInput";
import TaskList from "../components/TaskList";

export default function Dashboard() {
  const [tasks, setTasks] = useState([]);
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  const fetchUser = useCallback(async () => {
    try {
      const { data } = await api.get("/auth/me");
      setUser(data);
    } catch {
      localStorage.removeItem("token");
      navigate("/login");
    }
  }, [navigate]);

  const fetchTasks = useCallback(async () => {
    try {
      const { data } = await api.get("/tasks");
      setTasks(data);
    } catch {
      // Token expired or invalid
      localStorage.removeItem("token");
      navigate("/login");
    }
  }, [navigate]);

  useEffect(() => {
    fetchUser();
    fetchTasks();
  }, [fetchUser, fetchTasks]);

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>AXIS AI</h1>
        <div className="user-profile">
          {user?.picture && (
            <img
              src={user.picture}
              alt={user.name || "User"}
              className="user-avatar"
              referrerPolicy="no-referrer"
            />
          )}
          {user?.name && <span className="user-name">{user.name}</span>}
          <button className="logout-btn" onClick={logout}>
            Sign Out
          </button>
        </div>
      </header>
      <TaskInput onCreated={fetchTasks} />
      <TaskList tasks={tasks} onTasksChange={fetchTasks} />
    </div>
  );
}
