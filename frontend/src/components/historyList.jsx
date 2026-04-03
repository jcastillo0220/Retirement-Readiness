import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";

const linkRenderer = ({ href, children }) => (
  <a
    href={href}
    target="_blank"
    rel="noopener noreferrer"
    style={{ color: "#5B8CFF", textDecoration: "underline", fontWeight: 600 }}
  >
    {children}
  </a>
);

export default function HistoryList({
  history,
  bubbleStyle,
  validatedPill,
  correctedPill,
  selectedQuestionStyle,
}) {
  return (
    <div style={{ marginTop: 6, width: "100%" }}>
      {history.map((item) => (
        <div key={item.id} style={{ marginBottom: 14 }}>
          <div style={{ ...selectedQuestionStyle, marginTop: 6 }}>
            {item.label}
          </div>

          <div style={{ ...bubbleStyle, marginTop: 10 }}>
            {item.projection && (
              <div
                style={{
                  background: "rgba(255,255,255,0.06)",
                  borderRadius: 10,
                  padding: "10px 14px",
                  marginBottom: 10,
                  border: "1px solid rgba(255,255,255,0.10)",
                }}
              >
                {Object.entries(item.projection).map(([k, v]) => (
                  <div
                    key={k}
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      gap: 12,
                      marginBottom: 6,
                    }}
                  >
                    <span style={{ opacity: 0.7, textTransform: "capitalize" }}>
                      {k.replace(/_/g, " ")}
                    </span>
                    <span>{String(v)}</span>
                  </div>
                ))}
              </div>
            )}

            <ReactMarkdown rehypePlugins={[rehypeRaw]} components={{ a: linkRenderer }}>
              {item.answer}
            </ReactMarkdown>

            <div
              style={{
                marginTop: 10,
                display: "flex",
                gap: 10,
                alignItems: "center",
                flexWrap: "wrap",
              }}
            >
              {item.validated ? (
                <span style={validatedPill}>✓ Validated</span>
              ) : (
                <span style={correctedPill}>⚠ Corrected</span>
              )}

              {!item.validated && item.originalAnswer && (
                <details style={{ marginLeft: 4 }}>
                  <summary style={{ cursor: "pointer", opacity: 0.85 }}>
                    View original answer
                  </summary>
                  <div style={{ marginTop: 8 }}>
                    <ReactMarkdown rehypePlugins={[rehypeRaw]} components={{ a: linkRenderer }}>
                      {item.originalAnswer}
                    </ReactMarkdown>
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