import { useState } from "react";
import api from "../api";
import FileUpload from "./FileUpload";

export default function TaskInput({ onCreated }) {
  const [command, setCommand] = useState("");
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!command.trim()) return;
    setLoading(true);
    try {
      await api.post("/tasks", {
        command_text: command.trim(),
        input_mode: "text",
        file_ids: files.map((f) => f.name), // placeholder: real upload in later phase
      });
      setCommand("");
      setFiles([]);
      onCreated();
    } catch (err) {
      console.error("Failed to create task", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="task-input-section">
      <textarea
        placeholder="Describe what you want AXIS to do…"
        value={command}
        onChange={(e) => setCommand(e.target.value)}
      />
      <div className="actions">
        <FileUpload files={files} onChange={setFiles} />
        <button onClick={handleSubmit} disabled={loading || !command.trim()}>
          {loading ? "Sending…" : "Run Task"}
        </button>
      </div>
    </section>
  );
}
