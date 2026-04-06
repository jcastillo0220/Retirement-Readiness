import ReactMarkdown from "react-markdown";

function MarkdownBlock({ children }) {
  return (
    <ReactMarkdown
      components={{
        a: ({ href, children }) => (
          <a
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              color: "#5B8CFF",
              textDecoration: "underline",
              fontWeight: 500,
            }}
          >
            {children}
          </a>
        ),
      }}
    >
      {children}
    </ReactMarkdown>
  );
}

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

            {item.citation && (
              <div
                style={{
                  marginBottom: 12,
                  padding: "10px 12px",
                  border: "1px solid rgba(91,140,255,0.25)",
                  borderRadius: 10,
                  background: "rgba(91,140,255,0.06)",
                }}
              >
                <MarkdownBlock>{item.citation}</MarkdownBlock>
              </div>
            )}

            <MarkdownBlock>{item.answer_body || item.answer}</MarkdownBlock>

            {item.sources && (
              <div style={{ marginTop: 12 }}>
                <MarkdownBlock>{item.sources}</MarkdownBlock>
              </div>
            )}

            {item.grounding_report && item.grounding_report.length > 0 && (
              <details style={{ marginTop: 12 }}>
                <summary style={{ cursor: "pointer", opacity: 0.85 }}>
                  Grounding Report ({item.grounding_report.length})
                </summary>

                <ul style={{ marginTop: 8, paddingLeft: 20 }}>
                  {item.grounding_report.map((g, i) => (
                    <li key={i} style={{ marginBottom: 10 }}>
                      <strong>{g.phrase}</strong>:{" "}
                      <span style={{ color: g.supported ? "lightgreen" : "salmon" }}>
                        {g.supported ? "Supported" : "Not supported"}
                      </span>

                      {g.chunks && g.chunks.length > 0 && (
                        <ul style={{ marginTop: 6, paddingLeft: 20 }}>
                          {g.chunks.map((c, j) => (
                            <li key={j}>
                              <details>
                                <summary style={{ cursor: "pointer" }}>
                                  <em>Chunk {c.id}</em> — {c.source} ({c.section})
                                </summary>

                                <div
                                  style={{
                                    marginTop: 6,
                                    padding: "10px 12px",
                                    background: "rgba(255,255,255,0.05)",
                                    borderRadius: 8,
                                    border: "1px solid rgba(255,255,255,0.12)",
                                    whiteSpace: "pre-wrap",
                                    lineHeight: 1.45,
                                  }}
                                >
                                  {c.text}
                                </div>
                              </details>
                            </li>
                          ))}
                        </ul>
                      )}
                    </li>
                  ))}
                </ul>
              </details>
            )}

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
                    <MarkdownBlock>{item.originalAnswer}</MarkdownBlock>
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