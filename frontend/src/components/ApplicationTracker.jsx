import { useEffect, useState } from "react";
import { api } from "../api";
import { ListChecksIcon } from "./Icons";

const STATUSES = ["saved", "applied", "interview", "offer", "rejected"];

export default function ApplicationTracker({ resume }) {
  const [applications, setApplications] = useState([]);

  const refresh = () => {
    if (!resume) return;
    api.listApplications(resume.id).then((data) => setApplications(data.results || data)).catch(console.error);
  };

  useEffect(() => { refresh(); }, [resume]);

  const handleStatusChange = async (id, status) => {
    await api.updateApplication(id, { status });
    refresh();
  };

  if (!resume) return null;

  return (
    <div className="card">
      <div className="section-title"><ListChecksIcon /><h2>Application tracker</h2></div>

      {applications.length === 0 && (
        <p className="empty-state">No applications yet — save a job match to start tracking it here.</p>
      )}

      {applications.length > 0 && (
        <table className="tracker-table">
          <thead>
            <tr><th>Job</th><th>Company</th><th>Status</th></tr>
          </thead>
          <tbody>
            {applications.map((app) => (
              <tr key={app.id}>
                <td>{app.job_title}</td>
                <td>{app.company}</td>
                <td>
                  <select
                    className="status-select"
                    value={app.status}
                    onChange={(e) => handleStatusChange(app.id, e.target.value)}
                  >
                    {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
                  </select>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
