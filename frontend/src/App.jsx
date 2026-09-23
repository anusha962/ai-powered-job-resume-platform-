import { useState } from "react";
import ResumeUpload from "./components/ResumeUpload";
import ScoreCard from "./components/ScoreCard";
import JobMatches from "./components/JobMatches";
import JobBoard from "./components/JobBoard";
import ApplicationTracker from "./components/ApplicationTracker";
import {
  UploadIcon, GaugeIcon, TargetIcon, BriefcaseIcon, ListChecksIcon,
} from "./components/Icons";

const TABS = [
  { key: "score", label: "Score & Skills", icon: <GaugeIcon /> },
  { key: "matches", label: "Job Matches", icon: <TargetIcon /> },
  { key: "postings", label: "Job Postings", icon: <BriefcaseIcon /> },
  { key: "applications", label: "Applications", icon: <ListChecksIcon /> },
];

export default function App() {
  const [resume, setResume] = useState(null);
  const [tab, setTab] = useState("score");

  return (
    <div className="app">
      <section className="hero">
        <span className="hero-eyebrow">AI-powered · resume to interview</span>
        <h1>Turn your resume into interviews, faster.</h1>
        <p>
          Upload once — get an ATS score, a ranked list of matching jobs, missing
          skills to close, and interview questions tailored to each role.
        </p>
        <div className="hero-steps">
          <div className="hero-step">
            <div className="hero-step-icon"><UploadIcon /></div>
            <span>Upload your resume</span>
          </div>
          <div className="hero-step">
            <div className="hero-step-icon"><GaugeIcon /></div>
            <span>Get scored &amp; parsed</span>
          </div>
          <div className="hero-step">
            <div className="hero-step-icon"><TargetIcon /></div>
            <span>Match to real roles</span>
          </div>
        </div>
      </section>

      <ResumeUpload onUploaded={(r) => { setResume(r); setTab("score"); }} />

      {resume && (
        <>
          <nav className="tabs">
            {TABS.map((t) => (
              <button
                key={t.key}
                className={t.key === tab ? "tab active" : "tab"}
                onClick={() => setTab(t.key)}
              >
                {t.label}
              </button>
            ))}
          </nav>

          <main>
            {tab === "score" && <ScoreCard resume={resume} />}
            {tab === "matches" && <JobMatches resume={resume} />}
            {tab === "postings" && <JobBoard />}
            {tab === "applications" && <ApplicationTracker resume={resume} />}
          </main>
        </>
      )}
    </div>
  );
}
