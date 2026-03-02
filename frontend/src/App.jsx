import { useState, useRef } from "react";
import { askAI } from "./api";
import {
  containerStyle,
  shellStyle,
  headerStyle,
  brandStyle,
  titleStyle,
  subtitleStyle,
  badgeStyle,
  buttonRowStyle,
  footerNoteStyle,
  buttonStyle,
  suggestionStyle,
  selectedQuestionStyle,
  bubbleStyle,
  errorStyle,
  validatedPill,
  correctedPill,
} from "./styles";
import ReactMarkdown from "react-markdown";

const TOPIC_BUTTONS = [
  { label: "What is a Roth IRA?", prompt: "What is a Roth IRA?", key: "roth_ira" },
  { label: "What is a 401(k)?", prompt: "What is a 401(k)?", key: "401k" },
  { label: "What is a Traditional IRA?", prompt: "What is a Traditional IRA?", key: "traditional_ira" },
  { label: "What is a Rollover IRA?", prompt: "What is a Rollover IRA?", key: "rollover_ira" },
  { label: "What is a Roth 401(k)?", prompt: "What is a Roth 401(k)?", key: "roth_401k" },
];

export default function AIChat() {
  const [answer, setAnswer] = useState("");
  const [suggestedButtons, setSuggestedButtons] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedQuestion, setSelectedQuestion] = useState("");
  const [validated, setValidated] = useState(true);
  const [originalAnswer, setOriginalAnswer] = useState(null);
  const [error, setError] = useState(null);
  const [labelPrompt, setLabelPrompt] = useState(null);

  const [history, setHistory] = useState([]);
  const requestIdRef = useRef(0);

  async function handleAsk(prompt, label, topicKey) {
    const myRequestId = ++requestIdRef.current;

    setSelectedQuestion(label || "What is a Roth IRA?");
    setValidated(true);
    setOriginalAnswer(null);
    setError(null);
    setLoading(true);

    const finalPrompt = typeof prompt === "string" ? prompt : "What is a Roth IRA?";

    try {
      const res = await askAI({ question: finalPrompt, topicKey, label: label || null });

      if (myRequestId !== requestIdRef.current) return;

      const finalAnswer = res?.answer ?? "";
      const suggestions = res?.suggestions ?? [];
      const isValid = res?.validated !== undefined ? res.validated : true;
      const orig = res?.original_answer ?? null;
      const labelPromptFromBackend = res?.label_prompt || null;

      setAnswer(finalAnswer);
      setSuggestedButtons(suggestions);
      setValidated(isValid);
      setOriginalAnswer(orig);
      setLabelPrompt(labelPromptFromBackend);

      setHistory((h) => [
        ...h,
        {
          id: myRequestId,
          label: label || "What is a Roth IRA?",
          prompt: finalPrompt,
          topicKey,
          answer: finalAnswer,
          validated: isValid,
          originalAnswer: orig,
          timestamp: Date.now(),
          cached: !!res?.cached,
        },
      ]);
    } catch (err) {
      console.error(err);
      if (myRequestId !== requestIdRef.current) return;
      setError("Something went wrong. Try again.");
    } finally {
      if (myRequestId === requestIdRef.current) setLoading(false);
    }
  }

  return (
    <div style={containerStyle}>
      <div style={shellStyle}>
        {/* Header */}
        <div style={headerStyle}>
          <div style={brandStyle}>
            <div style={titleStyle}>Retirement Readiness</div>
            <div style={subtitleStyle}>
              Fintech-style AI assistant for retirement basics (educational only)
            </div>
          </div>
          <div style={badgeStyle}>{loading ? "Working…" : "Demo • Connected"}</div>
        </div>

        {/* Topic Buttons */}
        <div style={buttonRowStyle}>
          {TOPIC_BUTTONS.map((btn) => {
            const isActive = loading && selectedQuestion === btn.label;
            return (
              <button
                key={btn.key}
                onClick={() => handleAsk(btn.prompt, btn.label, btn.key)}
                style={{
                  ...buttonStyle,
                  opacity: loading && !isActive ? 0.65 : 1,
                  cursor: loading ? "not-allowed" : "pointer",
                }}
                disabled={loading}
                aria-pressed={selectedQuestion === btn.label}
                aria-label={btn.label}
                onMouseDown={(e) => (e.currentTarget.style.transform = "scale(0.98)")}
                onMouseUp={(e) => (e.currentTarget.style.transform = "scale(1)")}
                onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1)")}
              >
                {isActive ? "Thinking…" : btn.label}
              </button>
            );
          })}
        </div>

        {/* Suggested Follow-ups */}
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap", padding: "0 6px" }}>
          {!loading &&
            suggestedButtons.map((item, index) => (
              <button
                key={index}
                onClick={() => handleAsk(item.prompt, item.label, null)}
                style={suggestionStyle}
              >
                {item.label}
              </button>
            ))}
        </div>

        {/* Selected Question */}
        {selectedQuestion && <div style={selectedQuestionStyle}>{selectedQuestion}</div>}

        {/* Error */}
        {error && <div style={errorStyle}>{error}</div>}

        {/* Loading */}
        {loading && (
          <div style={{ ...bubbleStyle, opacity: 0.95, fontStyle: "italic" }}>
            AI is thinking…
          </div>
        )}

        {/* Current Answer */}
        {!loading && answer && (
          <div style={bubbleStyle}>
            <ReactMarkdown>{answer}</ReactMarkdown>

            <div style={{ marginTop: 10, display: "flex", gap: 10, alignItems: "center" }}>
              {validated ? (
                <span style={validatedPill}>Validated</span>
              ) : (
                <span style={correctedPill}>Corrected</span>
              )}

              {!validated && originalAnswer && (
                <details style={{ marginLeft: 4 }}>
                  <summary style={{ cursor: "pointer", opacity: 0.85 }}>View original answer</summary>
                  <div style={{ marginTop: 8 }}>
                    <ReactMarkdown>{originalAnswer}</ReactMarkdown>
                  </div>
                </details>
              )}
            </div>
          </div>
        )}

        {/* History */}
        {history.length > 0 && (
          <div style={{ marginTop: 6, width: "100%" }}>
            {history.map((item) => (
              <div key={item.id} style={{ marginBottom: 14 }}>
                <div style={{ ...selectedQuestionStyle, marginTop: 6 }}>{item.label}</div>

                <div style={{ ...bubbleStyle, marginTop: 10 }}>
                  <ReactMarkdown>{item.answer}</ReactMarkdown>

                  <div style={{ marginTop: 10, display: "flex", gap: 10, alignItems: "center" }}>
                    {item.validated ? (
                      <span style={validatedPill}>Validated</span>
                    ) : (
                      <span style={correctedPill}>Corrected</span>
                    )}

                    {!item.validated && item.originalAnswer && (
                      <details style={{ marginLeft: 4 }}>
                        <summary style={{ cursor: "pointer", opacity: 0.85 }}>View original answer</summary>
                        <div style={{ marginTop: 8 }}>
                          <ReactMarkdown>{item.originalAnswer}</ReactMarkdown>
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
        )}

        <div style={footerNoteStyle}>
          Tip: Use the top buttons for a clean 2–3 minute demo. Add “Sources” under answers for extra credibility.
        </div>
      </div>
    </div>
  );
}