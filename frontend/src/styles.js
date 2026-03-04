// Fintech-grade UI tokens (dark, clean, high-contrast)

const colors = {
  bg: "#070A12",
  card: "rgba(255,255,255,0.06)",
  card2: "rgba(255,255,255,0.08)",
  border: "rgba(255,255,255,0.12)",
  border2: "rgba(255,255,255,0.18)",
  text: "#EAF0FF",
  subtext: "rgba(234,240,255,0.72)",
  muted: "rgba(234,240,255,0.55)",
  accent: "#5B8CFF",
  accent2: "#7C5CFF",
  green: "#2EE59D",
  red: "#FF6B6B",
  amber: "#F6C445",
  chip: "rgba(91,140,255,0.12)",
  shadow: "0 18px 60px rgba(0,0,0,0.55)",
};

export const containerStyle = {
  minHeight: "100vh",
  width: "100%",
  background:
    "radial-gradient(1200px 600px at 10% 0%, rgba(91,140,255,0.22), transparent 60%)," +
    "radial-gradient(900px 500px at 90% 10%, rgba(124,92,255,0.20), transparent 55%)," +
    "linear-gradient(180deg, #050710 0%, #070A12 40%, #070A12 100%)",
  color: colors.text,
  fontFamily:
    'ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial',
  display: "flex",
  justifyContent: "center",
  padding: "28px 16px",
  boxSizing: "border-box",
};

export const shellStyle = {
  width: "100%",
  maxWidth: 980,
  display: "flex",
  flexDirection: "column",
  gap: 14,
};

export const headerStyle = {
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
  padding: "18px 18px",
  borderRadius: 18,
  background: colors.card,
  border: `2px solid ${colors.border}`,
  boxShadow: colors.shadow,
  backdropFilter: "blur(10px)",
};

export const brandStyle = {
  display: "flex",
  flexDirection: "column",
  gap: 4,
};

export const titleStyle = {
  fontSize: 20,
  fontWeight: 700,
  letterSpacing: 0.3,
};

export const subtitleStyle = {
  fontSize: 13,
  color: colors.subtext,
};

export const badgeStyle = {
  fontSize: 12,
  padding: "6px 10px",
  borderRadius: 999,
  border: `1px solid ${colors.border2}`,
  background: "rgba(255,255,255,0.04)",
  color: colors.subtext,
};

export const buttonRowStyle = {
  display: "flex",
  gap: 10,
  flexWrap: "wrap",
  padding: "12px 6px 2px",
};

export const buttonStyle = {
  border: `1px solid ${colors.border}`,
  background: "rgba(255,255,255,0.04)",
  color: colors.text,
  borderRadius: 999,
  padding: "10px 14px",
  fontSize: 13,
  fontWeight: 650,
  transition: "transform 120ms ease, background 120ms ease, border 120ms ease",
  boxShadow: "0 8px 20px rgba(0,0,0,0.25)",
};

export const suggestionStyle = {
  ...buttonStyle,
  background: colors.chip,
  border: `1px solid rgba(91,140,255,0.22)`,
  color: colors.text,
};

export const selectedQuestionStyle = {
  alignSelf: "flex-end",
  maxWidth: "76%",
  borderRadius: 16,
  padding: "10px 14px",
  background: "rgba(91,140,255,0.16)",
  border: "1px solid rgba(91,140,255,0.30)",
  color: colors.text,
  fontWeight: 650,
  boxShadow: "0 10px 30px rgba(0,0,0,0.30)",
};

export const bubbleStyle = {
  width: "100%",
  borderRadius: 18,
  padding: "14px 16px",
  background: colors.card2,
  border: `1px solid ${colors.border}`,
  boxShadow: "0 16px 50px rgba(0,0,0,0.35)",
  lineHeight: 1.5,
};

export const errorStyle = {
  width: "100%",
  borderRadius: 14,
  padding: "10px 12px",
  background: "rgba(255,107,107,0.12)",
  border: "1px solid rgba(255,107,107,0.26)",
  color: "#FFD6D6",
  fontWeight: 650,
};

export const statusPillBase = {
  fontSize: 12,
  fontWeight: 750,
  padding: "6px 10px",
  borderRadius: 999,
  border: `1px solid ${colors.border}`,
  background: "rgba(255,255,255,0.04)",
};

export const validatedPill = {
  ...statusPillBase,
  color: colors.green,
  border: "1px solid rgba(46,229,157,0.30)",
  background: "rgba(46,229,157,0.08)",
};

export const correctedPill = {
  ...statusPillBase,
  color: colors.amber,
  border: "1px solid rgba(246,196,69,0.30)",
  background: "rgba(246,196,69,0.10)",
};

export const footerNoteStyle = {
  fontSize: 12,
  color: colors.muted,
  padding: "0 6px",
};

export const scenarioCardStyle = {
  background: "#240a41",
  borderRadius: 12,
  padding: "14px 20px",
  marginBottom: 20,
  border: `2px solid ${colors.border}`,
  boxShadow: colors.shadow,
  backdropFilter: "blur(10px)",
};

export const scenarioLabelStyle = {
  fontSize: 14,
  fontWeight: 600,
  marginBottom: 4,
  color: "#b4bdee",
};

export const scenarioInputStyle = {
  width: "100%",
  padding: "10px 12px",
  borderRadius: 8,
  background: "#331257",
  border: `1px solid ${colors.border}`,
  marginBottom: 14,
  fontSize: 14,
};

export const scenarioButtonStyle = {
  background: "#231138",
  color: "white",
  padding: "10px 16px",
  borderRadius: 999,
  border: `1px solid ${colors.border}`,
  cursor: "pointer",
  fontWeight: 600,
  marginTop: 6,
};