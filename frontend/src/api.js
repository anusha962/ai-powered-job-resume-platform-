const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

async function request(path, options = {}) {
  const res = await fetch(`${API_URL}${path}`, options);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }
  return res.status === 204 ? null : res.json();
}

export const api = {
  uploadResume: (file) => {
    const formData = new FormData();
    formData.append("file", file);
    return request("/resumes/", { method: "POST", body: formData });
  },
  listResumes: () => request("/resumes/"),
  getResume: (id) => request(`/resumes/${id}/`),
  getRecommendations: (resumeId) => request(`/resumes/${resumeId}/recommendations/`),
  matchResumeToJob: (resumeId, jobId) =>
    request(`/resumes/${resumeId}/match/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ job_id: jobId }),
    }),
  listJobs: () => request("/jobs/"),
  createJob: (job) =>
    request("/jobs/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(job),
    }),
  listMatches: (resumeId) => request(`/matches/?resume=${resumeId}`),
  listApplications: (resumeId) => request(`/applications/?resume=${resumeId}`),
  createApplication: (application) =>
    request("/applications/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(application),
    }),
  updateApplication: (id, patch) =>
    request(`/applications/${id}/`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(patch),
    }),
};
