import ReactMarkdown from "react-markdown";

export default function HistoryList({
  history,
  bubbleStyle,
  validatedPill,
  correctedPill,
  selectedQuestionStyle
}) {
  return (
    <div style={{ marginTop: 6, width: "100%" }}>
      {history.map((item) => (
        <div key={item.id} style={{ marginBottom: 14 }}>
          <div style={{ ...selectedQuestionStyle, marginTop: 6 }}>{item.label}</div>

          <div style={{ ...bubbleStyle, marginTop: 10 }}>
            {item.projection && (
              <pre style={{ background: "#f7f7f7", padding: 10 }}>
                {JSON.stringify(item.projection, null, 2)}
              </pre>
            )}

            <ReactMarkdown>{item.answer}</ReactMarkdown>

            <div style={{ marginTop: 10, display: "flex", gap: 10, alignItems: "center" }}>
              {item.validated ? (
                <span style={validatedPill}>Validated</span>
              ) : (
                <span style={correctedPill}>Corrected</span>
              )}

              {!item.validated && item.originalAnswer && (
                <details style={{ marginLeft: 4 }}>
                  <summary style={{ cursor: "pointer", opacity: 0.85 }}>
                    View original answer
                  </summary>
                  <div style={{ marginTop: 8 }}>
                    <ReactMarkdown>{item.originalAnswer}</ReactMarkdown>
                  </div>
                </details>
              )}

              {item.cached && (
                <span style={{ marginLeft: "auto", opacity: 0.65, fontSize: 12 }}>
                  cached
                </span>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}