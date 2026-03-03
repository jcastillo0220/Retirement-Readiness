import ReactMarkdown from "react-markdown";

export default function AnswerBubble({
  answer,
  validated,
  originalAnswer,
  projection,
  bubbleStyle,
  validatedPill,
  correctedPill
}) {
  return (
    <div style={bubbleStyle}>
      {projection && (
        <pre style={{ background: "#0f184d", padding: 10 }}>
          {JSON.stringify(projection, null, 2)}
        </pre>
      )}

      <ReactMarkdown>{answer}</ReactMarkdown>

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
              <ReactMarkdown>{originalAnswer}</ReactMarkdown>
            </div>
          </details>
        )}
      </div>
    </div>
  );
}