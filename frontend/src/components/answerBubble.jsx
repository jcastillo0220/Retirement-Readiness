import { useState } from "react";
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import { citationBlock, citationLink } from "../styles";

export default function AnswerBubble({
  citation,
  answer,
  sources,
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

      {/* Citation Block */}
      {citation && (
        <div style={citationBlock}>
          <ReactMarkdown
            rehypePlugins={[rehypeRaw]}
            components={{
              a: ({ node, ...props }) => (
                <a {...props} style={citationLink} />
              )
            }}
          >
            {citation}
          </ReactMarkdown>
        </div>
      )}


      {/* Render Answer */}
      <ReactMarkdown rehypePlugins={[rehypeRaw]}>
        {answer}
      </ReactMarkdown>

      {/* Source Block */}
      <div style={{ marginTop: 16 }}>
        <ReactMarkdown rehypePlugins={[rehypeRaw]}>
          {sources}
        </ReactMarkdown>
      </div>

      {/* Supported Phrases Dropdown */}
      <details style={{ marginTop: 12 }}>
        <summary style={{ cursor: "pointer", opacity: 0.85 }}>
          Supported phrases ({supported.length})
        </summary>

        <ul style={{ marginTop: 8, paddingLeft: 20 }}>
          {supported.map((item, i) => (
            <li key={i} style={{ marginBottom: 8 }}>
              <strong>{item.phrase}</strong>
              <div style={{ fontSize: "0.85em", color: "#666", marginTop: 4 }}>
                <div>Chunk ID: {item.chunk_id}</div>
                <div>{item.chunk_text}</div>
              </div>
            </li>
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
              <ReactMarkdown rehypePlugins={[rehypeRaw]}>
                {originalAnswer}
              </ReactMarkdown>
            </div>
          </details>
        )}
      </div>
    </div>
  );
}