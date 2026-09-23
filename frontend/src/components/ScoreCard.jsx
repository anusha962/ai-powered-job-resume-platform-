import { GaugeIcon } from "./Icons";

function ScoreRing({ score }) {
  const size = 88;
  const stroke = 8;
  const r = (size - stroke) / 2;
  const circumference = 2 * Math.PI * r;
  const offset = circumference * (1 - score / 100);
  const color = score >= 75 ? "#1f7a5c" : score >= 50 ? "#d97706" : "#b3432b";

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#dcece4" strokeWidth={stroke} />
      <circle
        cx={size / 2} cy={size / 2} r={r} fill="none"
        stroke={color} strokeWidth={stroke} strokeLinecap="round"
        strokeDasharray={circumference} strokeDashoffset={offset}
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
      />
      <text x="50%" y="52%" textAnchor="middle" dominantBaseline="middle" fontFamily="Space Grotesk, sans-serif" fontWeight="700" fontSize="22" fill="#17231e">
        {Math.round(score)}
      </text>
    </svg>
  );
}

export default function ScoreCard({ resume }) {
  if (!resume) return null;
  const { ats_score, ats_breakdown, skills } = resume;
  const label = ats_score >= 75 ? "Strong resume" : ats_score >= 50 ? "Room to improve" : "Needs work";

  return (
    <div className="card">
      <div className="section-title"><GaugeIcon /><h2>ATS Score</h2></div>

      <div className="score-ring-wrap">
        <ScoreRing score={ats_score} />
        <div>
          <div className="score-ring-value">{label}</div>
          <div className="score-ring-label">out of 100, based on 4 signals below</div>
        </div>
      </div>

      {ats_breakdown && (
        <ul className="breakdown-list">
          {Object.entries(ats_breakdown).map(([key, val]) => (
            <li key={key}>
              <div className="breakdown-row">
                <span>{key.replace(/_/g, " ")}</span>
                <span>{val.points}/{val.max}</span>
              </div>
              <div className="bar-track">
                <div className="bar-fill" style={{ width: `${(val.points / val.max) * 100}%` }} />
              </div>
            </li>
          ))}
        </ul>
      )}

      <h3>Detected skills ({skills?.length || 0})</h3>
      <div className="chip-row">
        {skills?.length ? skills.map((s) => <span className="chip" key={s}>{s}</span>) : (
          <p className="muted small">No recognized skills found — try adding a dedicated Skills section.</p>
        )}
      </div>
    </div>
  );
}
