import { useEffect, useState } from "react";
import { api } from "../api";
import { BriefcaseIcon } from "./Icons";

export default function JobBoard() {
  const [jobs, setJobs] = useState([]);
  const [form, setForm] = useState({ title: "", company: "", description: "" });
  const [saving, setSaving] = useState(false);

  const refresh = () => api.listJobs().then((data) => setJobs(data.results || data)).catch(console.error);

  useEffect(() => { refresh(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.title || !form.description) return;
    setSaving(true);
    try {
      await api.createJob(form);
      setForm({ title: "", company: "", description: "" });
      refresh();
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="card">
      <div className="section-title"><BriefcaseIcon /><h2>Job postings</h2></div>

      <form onSubmit={handleSubmit} className="job-form">
        <input
          placeholder="Job title"
          value={form.title}
          onChange={(e) => setForm({ ...form, title: e.target.value })}
        />
        <input
          placeholder="Company"
          value={form.company}
          onChange={(e) => setForm({ ...form, company: e.target.value })}
        />
        <textarea
          placeholder="Paste the full job description here..."
          rows={5}
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
        />
        <button type="submit" disabled={saving}>{saving ? "Saving..." : "Add job"}</button>
      </form>

      {jobs.length === 0 && <p className="empty-state">No jobs added yet — paste one above to get started.</p>}

      <ul className="job-list">
        {jobs.map((job) => (
          <li key={job.id} className="job-item">
            <div>
              <strong>{job.title}</strong> {job.company && <span className="muted"> @ {job.company}</span>}
              <div className="chip-row">
                {job.required_skills?.slice(0, 8).map((s) => <span className="chip" key={s}>{s}</span>)}
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
