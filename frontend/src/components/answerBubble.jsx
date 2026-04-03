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
  correctedPill,
}) {
  const [phrasesOpen, setPhrasesOpen] = useState(false);
  const supported = supported_phrases || [];

  // Extract source name + url from the citation markdown for the badge chip
  // e.g. "According to [Northwestern Mutual](http://...),"
  const badgeMatch = (citation || "").match(/\[([^\]]+)\]\(([^)]+)\)/);
  const badge = badgeMatch
    ? { name: badgeMatch[1], url: badgeMatch[2] }
    : null;
  const badgeIsPdf = badge && (badge.url.includes("/pdf/") || badge.url.endsWith(".pdf"));

  // Shared link renderer — always opens in new tab
  const linkRenderer = ({ href, children }) => (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      style={linkStyle}
    >
      {children}
    </a>
  );

  return (
    <div style={bubbleStyle}>

      {/* ── Source badge chip ── */}
      {badge && (
        <a
          href={badge.url}
          target="_blank"
          rel="noopener noreferrer"
          style={badgeChipStyle}
        >
          {badgeIsPdf ? "📄" : "🔗"} {badge.name}
        </a>
      )}

      {/* ── Citation line ── */}
      {citation && (
        <div style={{ ...citationBlock, marginTop: badge ? 10 : 0 }}>
          <ReactMarkdown
            rehypePlugins={[rehypeRaw]}
            components={{ a: linkRenderer }}
          >
            {citation}
          </ReactMarkdown>
        </div>
      )}

      {/* ── Answer body ── */}
      <div style={{ marginTop: 10 }}>
        <ReactMarkdown
          rehypePlugins={[rehypeRaw]}
          components={{ a: linkRenderer }}
        >
          {answer}
        </ReactMarkdown>
      </div>

      {/* ── Sources block ── */}
      {sources && (
        <div style={{ marginTop: 14 }}>
          <ReactMarkdown
            rehypePlugins={[rehypeRaw]}
            components={{ a: linkRenderer }}
          >
            {sources}
          </ReactMarkdown>
        </div>
      )}

      {/* ── Supported phrases toggle ── */}
      {supported.length > 0 && (
        <div style={{ marginTop: 12 }}>
          <button
            onClick={() => setPhrasesOpen((p) => !p)}
            style={toggleBtnStyle}
          >
            {phrasesOpen ? "▼" : "▶"} Supported phrases ({supported.length})
          </button>
          {phrasesOpen && (
            <ul style={{ marginTop: 6, paddingLeft: 18 }}>
              {supported.map((phrase, i) => (
                <li key={i} style={phraseItemStyle}>
                  {typeof phrase === "string" ? phrase : phrase.phrase}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      {/* ── Validation pill ── */}
      <div style={{ marginTop: 12, display: "flex", gap: 10, alignItems: "center" }}>
        {validated ? (
          <span style={validatedPill}>✓ Validated</span>
        ) : (
          <span style={correctedPill}>⚠ Corrected</span>
        )}

        {!validated && originalAnswer && (
          <details style={{ marginLeft: 4 }}>
            <summary style={{ cursor: "pointer", opacity: 0.85, fontSize: 13 }}>
              View original answer
            </summary>
            <div style={{ marginTop: 8 }}>
              <ReactMarkdown rehypePlugins={[rehypeRaw]} components={{ a: linkRenderer }}>
                {originalAnswer}
              </ReactMarkdown>
            </div>
          </details>
        )}
      </div>

    </div>
  );
}

// ── Styles ──────────────────────────────────────────────────────────────────

const linkStyle = {
  color: "#5B8CFF",
  textDecoration: "underline",
  fontWeight: 600,
};

const badgeChipStyle = {
  display: "inline-flex",
  alignItems: "center",
  gap: 5,
  fontSize: 12,
  fontWeight: 600,
  padding: "4px 10px",
  borderRadius: 999,
  background: "rgba(91,140,255,0.14)",
  border: "1px solid rgba(91,140,255,0.30)",
  color: "#8fb3ff",
  textDecoration: "none",
  cursor: "pointer",
};

const toggleBtnStyle = {
  background: "none",
  border: "none",
  color: "rgba(234,240,255,0.6)",
  fontSize: 13,
  cursor: "pointer",
  padding: 0,
};

const phraseItemStyle = {
  fontSize: 12,
  color: "rgba(234,240,255,0.6)",
  marginBottom: 3,
  lineHeight: 1.5,
};