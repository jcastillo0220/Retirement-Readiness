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

export default function AnswerBubble({
  answer,
  projection,   // ⭐ this is now the correct prop
  citation,
  answer_body,
  sources,
  validated,
  originalAnswer,
  supported_phrases = [],
  grounding_report = [],
  bubbleStyle,
  validatedPill,
  correctedPill,
}) {
  const supported = supported_phrases || [];

  return (
    <div style={bubbleStyle}>

      {/* ⭐ FIXED: use projection, not answer.projection */}
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

      <MarkdownBlock>{answer_body || answer}</MarkdownBlock>

      {sources && (
        <div style={{ marginTop: 12 }}>
          <MarkdownBlock>{sources}</MarkdownBlock>
        </div>
      )}

      <details style={{ marginTop: 12 }}>
        <summary style={{ cursor: "pointer", opacity: 0.85 }}>
          Supported phrases ({supported.length})
        </summary>

        <ul style={{ marginTop: 8, paddingLeft: 20 }}>
          {supported.map((p, i) => (
            <li key={i}>{p}</li>
          ))}
        </ul>
      </details>

      {grounding_report.length > 0 && (
      <details style={{ marginTop: 12 }}>
        <summary style={{ cursor: "pointer", opacity: 0.85 }}>
          Grounding report ({grounding_report.length})
        </summary>

        <ul style={{ marginTop: 8, paddingLeft: 20 }}>
          {grounding_report.map((item, i) => (
            <li key={i} style={{ marginBottom: 6 }}>
              <strong>{item.phrase}</strong>:{" "}
              <span style={{ color: item.supported ? "green" : "red" }}>
                {item.supported ? "Supported" : "Not supported"}
              </span>
            </li>
          ))}
        </ul>
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