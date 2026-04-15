import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import { citationBlock, citationLink } from "../styles";

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

export default function AnswerBubble({
  citation,
  answer,
  sources,
  validated,
  isRefusal = false,
  originalAnswer,
  grounding_report = [],
  bubbleStyle,
  validatedPill,
  correctedPill,
}) {
  const report = grounding_report.full_report || [];

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
        <p style={refusalText}>{answer_body}</p>
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
        <div style={citationLink}>
          <ReactMarkdown
            rehypePlugins={[rehypeRaw]}
            components={{ a: linkRenderer }}
          >
            {sources}
          </ReactMarkdown>
        </div>
      )}

      {report.length > 0 && (
        <details style={{ marginTop: 16 }}>
          <summary style={{ cursor: "pointer", opacity: 0.85 }}>
            Grounding Report ({report.length})
          </summary>

          <ul style={{ marginTop: 8, paddingLeft: 20 }}>
            {report.map((item, i) => (
              <li key={i} style={{ marginBottom: 12 }}>
                <strong>{item.phrase}</strong>:{" "}
                <span style={{ color: item.supported ? "lightgreen" : "salmon" }}>
                  {item.supported ? "Supported" : "Not supported"}
                </span>

                {item.chunks && item.chunks.length > 0 && (
                  <ul style={{ marginTop: 6, paddingLeft: 20 }}>
                    {item.chunks.map((chunk, j) => (
                      <li key={j} style={{ marginBottom: 8 }}>
                        <details>
                          <summary style={{ cursor: "pointer" }}>
                            <em>Chunk {chunk.id}</em> — {chunk.source} ({chunk.section})
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
                              {highlightPhrase(chunk.text, item.phrase)}
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
        </details>
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