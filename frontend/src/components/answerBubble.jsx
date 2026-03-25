import { useState } from "react";
import ReactMarkdown from "react-markdown";

export default function AnswerBubble({
  answer,
  validated,
  originalAnswer,
  supported_phrases = [],
  bubbleStyle,
  validatedPill,
  correctedPill
}) {
  const supported = supported_phrases || [];

  return (
    <div style={bubbleStyle}>
      {/* Render Answer */}
      <ReactMarkdown>{answer}</ReactMarkdown>

      {/* Supported Phrases Dropdown */}
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

      {/* Validation Pills */}
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