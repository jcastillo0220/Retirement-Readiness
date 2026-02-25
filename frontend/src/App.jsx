import { useState, useRef } from "react";
import { askAI } from "./api";
import { bubbleStyle, buttonStyle, suggestionStyle, selectedQuestionStyle, errorStyle } from "./styles";
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

  // chat history: newest last (optional)
  const [history, setHistory] = useState([]);
  // request id guard to avoid out-of-order updates
  const requestIdRef = useRef(0);

  // handleAsk expects a short prompt, a human label, and a topic key
  async function handleAsk(prompt, label, topicKey) {
    const myRequestId = ++requestIdRef.current;

    // Immediately show which question is active
    setSelectedQuestion(label || "What is a Roth IRA?");
    setValidated(true);
    setOriginalAnswer(null);
    setError(null);
    setLoading(true);

    const finalPrompt = typeof prompt === "string" ? prompt : "What is a Roth IRA?";

    try {
      // askAI should call your backend /api/ai/generate and return JSON:
      // { answer: string, suggestions: [], validated: boolean, original_answer?: string, cached?: bool }
      const res = await askAI({ question: finalPrompt, topicKey });

      // If a newer request started after this one, ignore this response
      if (myRequestId !== requestIdRef.current) return;

      const finalAnswer = res?.answer ?? "";
      const suggestions = res?.suggestions ?? [];
      const isValid = res?.validated !== undefined ? res.validated : true;
      const orig = res?.original_answer ?? null;

      // update UI
      setAnswer(finalAnswer);
      setSuggestedButtons(suggestions);
      setValidated(isValid);
      setOriginalAnswer(orig);

      // append to history
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
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        width: "100%",
        padding: 20,
        boxSizing: "border-box",
      }}
    >
      <div style={{ width: "100%", maxWidth: 900, display: "flex", flexDirection: "column", gap: 12 }}>
        {/* Top row of topic buttons */}
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
          {TOPIC_BUTTONS.map((btn) => {
            const isActive = loading && selectedQuestion === btn.label;
            return (
              <button
                key={btn.key}
                onClick={() => handleAsk(btn.prompt, btn.label, btn.key)}
                style={{
                  ...buttonStyle,
                  padding: "8px 14px",
                  opacity: loading && !isActive ? 0.6 : 1,
                  cursor: loading ? "not-allowed" : "pointer",
                }}
                disabled={loading}
                aria-pressed={selectedQuestion === btn.label}
                aria-label={btn.label}
              >
                {isActive ? "Thinking..." : btn.label}
              </button>
            );
          })}
        </div>

        {/* Suggested follow-up buttons (topic-scoped) */}
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginTop: 4 }}>
          {!loading &&
            suggestedButtons.map((item, index) => (
              <button
                key={index}
                onClick={() => handleAsk(item.prompt, item.label, null)}
                style={{
                  ...suggestionStyle,
                }}
              >
                {item.label}
              </button>
            ))}
        </div>

        {/* Selected question bubble (shows the label the user asked) */}
        {selectedQuestion && (
          <div
            style={{
              ...selectedQuestionStyle,
            }}
          >
            {selectedQuestion}
          </div>
        )}

        {/* Error */}
        {error && (
          <div
            style={{
              ...errorStyle,
            }}
          >
            {error}
          </div>
        )}

        {/* Loading indicator */}
        {loading && (
          <div
            style={{
              backgroundColor: "#e8f0fe",
              padding: "10px 16px",
              borderRadius: 12,
              marginTop: 6,
              fontStyle: "italic",
              opacity: 0.95,
            }}
          >
            AI is thinking…
          </div>
        )}

        {/* Current AI answer bubble */}
        {!loading && answer && (
          <div style={{ ...bubbleStyle, marginTop: 8 }}>
            <ReactMarkdown>{answer}</ReactMarkdown>

            <div style={{ marginTop: 8, display: "flex", gap: 8, alignItems: "center" }}>
              {validated ? (
                <span style={{ color: "#0b6623", fontWeight: 600 }}>Validated</span>
              ) : (
                <span style={{ color: "#a63a3a", fontWeight: 600 }}>Corrected by AI</span>
              )}

              {!validated && originalAnswer && (
                <details style={{ marginLeft: 8 }}>
                  <summary style={{ cursor: "pointer", color: "#555" }}>View original answer</summary>
                  <div style={{ marginTop: 6 }}>
                    <ReactMarkdown>{originalAnswer}</ReactMarkdown>
                  </div>
                </details>
              )}
            </div>
          </div>
        )}

        {/* Chat history (previous Q&A) */}
        {history.length > 0 && (
          <div style={{ marginTop: 12, width: "100%" }}>
            {history.map((item) => (
              <div key={item.id} style={{ marginBottom: 12 }}>
                <div
                  style={{
                    alignSelf: "flex-end",
                    backgroundColor: "#d1e7ff",
                    padding: "6px 12px",
                    borderRadius: 14,
                    maxWidth: "70%",
                    marginLeft: "auto",
                    color: "#003366",
                    fontWeight: 500,
                    boxShadow: "0 1px 4px rgba(0,0,0,0.06)",
                  }}
                >
                  {item.label}
                </div>

                <div style={{ ...bubbleStyle, marginTop: 8 }}>
                  <ReactMarkdown>{item.answer}</ReactMarkdown>

                  <div style={{ marginTop: 8, display: "flex", gap: 8, alignItems: "center" }}>
                    {item.validated ? (
                      <span style={{ color: "#0b6623", fontWeight: 600 }}>Validated</span>
                    ) : (
                      <span style={{ color: "#a63a3a", fontWeight: 600 }}>Corrected by AI</span>
                    )}

                    {!item.validated && item.originalAnswer && (
                      <details style={{ marginLeft: 8 }}>
                        <summary style={{ cursor: "pointer", color: "#555" }}>View original answer</summary>
                        <div style={{ marginTop: 6 }}>
                          <ReactMarkdown>{item.originalAnswer}</ReactMarkdown>
                        </div>
                      </details>
                    )}

                    {item.cached && (
                      <span style={{ marginLeft: "auto", color: "#666", fontSize: 12 }}>cached</span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}