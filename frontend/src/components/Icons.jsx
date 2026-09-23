/* Small inline icon set — kept dependency-free (no icon library needed). */
const base = {
  width: 20,
  height: 20,
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.8,
  strokeLinecap: "round",
  strokeLinejoin: "round",
};

export const UploadIcon = () => (
  <svg {...base}><path d="M12 16V4M12 4l-4 4M12 4l4 4" /><path d="M4 16v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3" /></svg>
);

export const GaugeIcon = () => (
  <svg {...base}><path d="M4 15a8 8 0 1 1 16 0" /><path d="M12 15l3-4" /><circle cx="12" cy="15" r="1" fill="currentColor" stroke="none" /></svg>
);

export const TargetIcon = () => (
  <svg {...base}><circle cx="12" cy="12" r="8" /><circle cx="12" cy="12" r="4" /><circle cx="12" cy="12" r="0.5" fill="currentColor" /></svg>
);

export const BriefcaseIcon = () => (
  <svg {...base}><rect x="3" y="7" width="18" height="13" rx="2" /><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" /></svg>
);

export const ListChecksIcon = () => (
  <svg {...base}><path d="M9 6h11M9 12h11M9 18h11" /><path d="M4 6l1 1 2-2M4 12l1 1 2-2M4 18l1 1 2-2" /></svg>
);

export const FileIcon = () => (
  <svg {...base}><path d="M14 3v5a1 1 0 0 0 1 1h5" /><path d="M6 21h12a1 1 0 0 0 1-1V7l-5-5H6a1 1 0 0 0-1 1v17a1 1 0 0 0 1 1Z" /></svg>
);
