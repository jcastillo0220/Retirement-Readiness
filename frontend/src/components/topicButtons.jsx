export default function TopicButtons({
  buttons,
  loading,
  selectedQuestion,
  onAsk,
  buttonStyle,
  buttonRowStyle
}) {
  return (
    <div style={buttonRowStyle}>
      {buttons.map((btn) => {
        const isActive = loading && selectedQuestion === btn.label;
        return (
          <button
            key={btn.key}
            onClick={() => onAsk(btn.prompt, btn.key, btn.label)}
            disabled={loading}
            style={{
              ...buttonStyle,
              opacity: loading && !isActive ? 0.65 : 1,
              cursor: loading ? "not-allowed" : "pointer",
            }}
            aria-pressed={selectedQuestion === btn.label}
            aria-label={btn.label}
            onMouseDown={(e) => (e.currentTarget.style.transform = "scale(0.98)")}
            onMouseUp={(e) => (e.currentTarget.style.transform = "scale(1)")}
            onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1)")}
          >
            {isActive ? "Thinking…" : btn.label}
          </button>
        );
      })}
    </div>
  );
}