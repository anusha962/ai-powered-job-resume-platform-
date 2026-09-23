import { useEffect, useState } from "react";
import { api } from "../api";
import { TargetIcon } from "./Icons";

export default function JobMatches({ resume }) {
  const [recommendations, setRecommendations] = useState([]);
  const [activeMatch, setActiveMatch] = useState(null);
  const [loadingJobId, setLoadingJobId] = useState(null);

  useEffect(() => {
    if (!resume) return;
    api.getRecommendations(resume.id).then(setRecommendations).catch(console.error);
  }, [resume]);

  const handleGenerateMatch = async (jobId) => {
    setLoadingJobId(jobId);
    try {
      const match = await api.matchResumeToJob(resume.id, jobId);
      setActiveMatch(match);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingJobId(null);
    }
  };

  const handleSaveApplication = async (jobId) => {
    await api.createApplication({ resume: resume.id, job: jobId, status: "saved" });
    alert("Added to your application tracker.");
  };

  if (!resume) return null;

  return (
    <div className="card">
      <div className="section-title"><TargetIcon /><h2>Recommended jobs</h2></div>

      {recommendations.length === 0 && (
        <p className="empty-state">No job postings yet — add one in the Job Postings tab to see matches here.</p>
      )}

      <ul className="job-list">
        {recommendations.map(({ job, similarity_pct }) => (
          <li key={job.id} className="job-item">
            <div>
              <strong>{job.title}</strong> {job.company && <span className="muted"> @ {job.company}</span>}
              <div className="similarity-badge">
                <span className="similarity-track">
                  <span className="similarity-fill" style={{ width: `${similarity_pct}%` }} />
                </span>
                {similarity_pct}% similarity
              </div>
            </div>
            <div className="job-actions">
              <button onClick={() => handleGenerateMatch(job.id)} disabled={loadingJobId === job.id}>
                {loadingJobId === job.id ? "Generating..." : "Full match + interview Qs"}
              </button>
              <button className="secondary" onClick={() => handleSaveApplication(job.id)}>
                Save to tracker
              </button>
            </div>
          </li>
        ))}
      </ul>

      {activeMatch && (
        <div className="match-detail">
          <h3 style={{ marginTop: 0 }}>
            {activeMatch.job.title}
            <span className="match-score-pill">{activeMatch.match_score}% skill match</span>
          </h3>
          <p><strong>Missing skills:</strong> {activeMatch.missing_skills.join(", ") || "None — great fit!"}</p>
          <p><strong>Tailored interview questions</strong></p>
          <ol>
            {activeMatch.interview_questions.map((q, i) => <li key={i} style={{ marginBottom: 6 }}>{q}</li>)}
          </ol>
        </div>
      )}
    </div>
  );
}
