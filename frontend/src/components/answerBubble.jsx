import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";

function highlightPhrase(text, phrase) {
  if (!phrase) return text;

  const ngrams = generateNGrams(phrase, 2); // require 2+ words
  let highlighted = text;

  for (const ng of ngrams) {
    const escaped = ng.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const regex = new RegExp(escaped, "gi");

    highlighted = highlighted.replace(regex, match => `<mark>${match}</mark>`);
  }

  return highlighted;
}

function generateNGrams(phrase, minWords = 2) {
  const words = phrase.split(/\s+/).filter(w => w.length > 2);
  const ngrams = [];

  for (let size = minWords; size <= words.length; size++) {
    for (let i = 0; i <= words.length - size; i++) {
      ngrams.push(words.slice(i, i + size).join(" "));
    }
  }

  return ngrams;
}

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

export default function AnswerBubble({
  answer,
  projection, 
  citation,
  answer_body,
  sources,
  validated,
  originalAnswer,
  grounding_report = [],
  bubbleStyle,
  validatedPill,
  correctedPill,
}) {

  return (
    <div style={bubbleStyle}>

      {projection && (
        <div
          style={{
            background: "rgba(255,255,255,0.06)",
            borderRadius: 10,
            padding: "10px 14px",
            marginBottom: 10,
            border: "1px solid rgba(255,255,255,0.10)",
          }}
        >
          {Object.entries(projection).map(([k, v]) => (
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

      {citation && (
        <div
          style={{
            marginBottom: 12,
            padding: "10px 12px",
            border: "1px solid rgba(91,140,255,0.25)",
            borderRadius: 10,
            background: "rgba(91,140,255,0.06)",
          }}
        >
          <MarkdownBlock>{citation}</MarkdownBlock>
        </div>
      )}

      <MarkdownBlock>{answer_body}</MarkdownBlock>

      {sources && (
        <div style={{ marginTop: 12 }}>
          <MarkdownBlock>{sources}</MarkdownBlock>
        </div>
      )}

      {grounding_report.length > 0 && (
        <details style={{ marginTop: 12 }}>
          <summary style={{ cursor: "pointer", opacity: 0.85 }}>
            Grounding Report ({grounding_report.length})
          </summary>

          <ul style={{ marginTop: 8, paddingLeft: 20 }}>
            {grounding_report.map((item, i) => (
              <li key={i} style={{ marginBottom: 10 }}>
                <strong>{item.phrase}</strong>:{" "}
                <span style={{ color: item.supported ? "lightgreen" : "salmon" }}>
                  {item.supported ? "Supported" : "Not supported"}
                </span>

                {item.chunks && item.chunks.length > 0 && (
                  <ul style={{ marginTop: 6, paddingLeft: 20, opacity: 0.9 }}>
                    {item.chunks.map((c, j) => (
                      <li key={j} style={{ marginBottom: 8 }}>
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
                            <ReactMarkdown
                              rehypePlugins={[rehypeRaw]}
                              components={{
                                mark: ({ children }) => (
                                  <mark style={{ background: "#e1e509ce", padding: "0 2px" }}>
                                    {children}
                                  </mark>
                                ),
                              }}
                            >
                              {highlightPhrase(c.text, item.phrase)}
                            </ReactMarkdown>
                          </div>
                        </details>
                      </li>
                    ))}
                  </ul>
                )}
              </li>
            ))}
          </ul>
          {/* Unsupported Phrases Section */}
          {grounding_report.some(item => !item.supported) && (
            <details style={{ marginTop: 12 }}>
              <summary style={{ cursor: "pointer", opacity: 0.85 }}>
                Unsupported Phrases (
                  {grounding_report.filter(item => !item.supported).length}
                )
              </summary>

              <ul style={{ marginTop: 8, paddingLeft: 20 }}>
                {grounding_report
                  .filter(item => !item.supported)
                  .map((item, i) => (
                    <li key={i} style={{ marginBottom: 10 }}>
                      <strong>{item.phrase}</strong>
                      <span style={{ color: "salmon", marginLeft: 6 }}>
                        Not supported
                      </span>
                    </li>
                  ))}
              </ul>
            </details>
          )}
        </details>
      )}

      <div style={{ marginTop: 10, display: "flex", gap: 10, alignItems: "center" }}>
        {validated ? (
          <span style={validatedPill}>Validated</span>
        ) : (
          <span style={correctedPill}>Corrected</span>
        )}

        {!validated && originalAnswer && (
          <details style={{ marginLeft: 4 }}>
            <summary style={{ cursor: "pointer", opacity: 0.85 }}>
              View original answer
            </summary>
            <div style={{ marginTop: 8 }}>
              <MarkdownBlock>{originalAnswer}</MarkdownBlock>
            </div>
          </details>
        )}
      </div>
    </div>
  );
}