import { useState } from "react";
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import { citationBlock, citationLink } from "../styles";

export default function AnswerBubble({
  citation,
  answer,
  sources,
  validated,
  isRefusal = false,
  originalAnswer,
  supported_phrases = [],
  bubbleStyle,
  validatedPill,
  correctedPill,
}) {
  const [phrasesOpen, setPhrasesOpen] = useState(false);
  const supported = supported_phrases || [];

  // Extract ALL source badges from the citation line
  // e.g. "According to [Fidelity](url), [IRS](url), and [Northwestern Mutual](url),"
  const badgeMatches = [...(citation || "").matchAll(/\[([^\]]+)\]\(([^)]+)\)/g)];
  const badges = badgeMatches.map(([, name, url]) => ({
    name,
    url,
    isPdf: url.includes("/pdf/") || url.toLowerCase().endsWith(".pdf"),
  }));

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

  // ── Refusal state — render a clean message with no citations,
  // no badges, no "Corrected" pill, no "View original answer".
  if (isRefusal) {
    return (
      <div style={{ ...bubbleStyle, ...refusalBubbleStyle }}>
        <div style={refusalIconRow}>
          <span style={refusalIcon}>⚠</span>
          <span style={refusalLabel}>Outside verified sources</span>
        </div>
        <p style={refusalText}>{answer}</p>
      </div>
    );
  }

  return (
    <div style={bubbleStyle}>

      {/* ── Source badge chips — one per contributing source ── */}
      {badges.length > 0 && (
        <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: 10 }}>
          {badges.map((badge, i) => (
            <a
              key={i}
              href={badge.url}
              target="_blank"
              rel="noopener noreferrer"
              style={badgeChipStyle}
            >
              {badge.isPdf ? "📄" : "🔗"} {badge.name}
            </a>
          ))}
        </div>
      )}

      {/* ── Citation line ── */}
      {citation && (
        <div style={citationBlock}>
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
      {/* "Corrected" is reserved for refusals/out-of-scope only.
          Any answer that passed grounding shows "Verified" regardless
          of whether it went through the repair loop. */}
      <div style={{ marginTop: 12, display: "flex", gap: 10, alignItems: "center" }}>
        {validated ? (
          <span style={validatedPill}>✓ Validated</span>
        ) : (
          <span style={validatedPill}>✓ Verified</span>
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

const refusalBubbleStyle = {
  background: "rgba(246,196,69,0.07)",
  border: "1px solid rgba(246,196,69,0.22)",
};

const refusalIconRow = {
  display: "flex",
  alignItems: "center",
  gap: 8,
  marginBottom: 10,
};

const refusalIcon = {
  fontSize: 16,
  color: "#F6C445",
};

const refusalLabel = {
  fontSize: 12,
  fontWeight: 700,
  color: "#F6C445",
  letterSpacing: 0.4,
  textTransform: "uppercase",
};

const refusalText = {
  fontSize: 14,
  color: "rgba(234,240,255,0.85)",
  lineHeight: 1.65,
  margin: 0,
};