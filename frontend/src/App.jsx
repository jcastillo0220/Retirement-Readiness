import { useEffect, useState } from "react";
import { useAIChat } from "./useAIChat";
import { API_BASE } from "./api";
import ScenarioForm from "./components/scenarioForm";
import TopicButtons from "./components/topicButtons";
import AnswerBubble from "./components/answerBubble";
import HistoryList from "./components/historyList";
import logo from "./assets/logo.png";
import {
  containerStyle,
  shellStyle,
  headerStyle,
  brandStyle,
  titleStyle,
  subtitleStyle,
  badgeStyle,
  buttonRowStyle,
  buttonStyle,
  suggestionStyle,
  selectedQuestionStyle,
  bubbleStyle,
  errorStyle,
  validatedPill,
  correctedPill,
} from "./styles";

export default function AIChat() {
  const {
    answer,
    citation,
    answer_body,
    sources,
    isRefusal,
    suggestedButtons,
    loading,
    selectedQuestion,
    validated,
    originalAnswer,
    error,
    history,
    grounding_report,
    activeTopicKey,
    handleAsk,
    handleScenario,
  } = useAIChat();

  const [userQ, setUserQ] = useState("");
  const [status, setStatus] = useState("checking");

  useEffect(() => {
    fetch(`${API_BASE}/health`)
      .then((r) => setStatus(r.ok ? "connected" : "error"))
      .catch(() => setStatus("error"));
  }, []);

  const topic_buttons = [
    { label: "What is a Roth IRA?", prompt: "What is a Roth IRA?", key: "roth_ira" },
    { label: "What is a 401(k)?", prompt: "What is a 401(k)?", key: "401k" },
    { label: "What is a Traditional IRA?", prompt: "What is a Traditional IRA?", key: "traditional_ira" },
    { label: "What is a Rollover IRA?", prompt: "What is a Rollover IRA?", key: "rollover_ira" },
    { label: "What is a Roth 401(k)?", prompt: "What is a Roth 401(k)?", key: "roth_401k" },
  ];

  // Detect topic key from free-text question so numeric questions
  // are routed to the correct retrieval pipeline instead of always
  // defaulting to "definitions" (which only searches the PDF).
  function detectTopicKey(q) {
    const lower = q.toLowerCase();
    if (lower.includes("roth 401") || lower.includes("roth401")) return "roth_401k";
    if (lower.includes("rollover")) return "rollover_ira";
    if (lower.includes("traditional ira") || lower.includes("traditional")) return "traditional_ira";
    if (lower.includes("roth ira") || lower.includes("roth")) return "roth_ira";
    if (lower.includes("401(k)") || lower.includes("401k")) return "401k";
    if (lower.includes("compound interest") || lower.includes("compound")) return "compound_interest";
    // Default to definitions for "what is" style questions, otherwise use roth_ira
    // as a broad fallback that has the most general retirement content
    if (lower.includes("what is") || lower.includes("define") || lower.includes("explain")) {
      return "definitions";
    }
    return "definitions";
  }

  function handleSendCustomQuestion() {
    const trimmed = userQ.trim();
    if (!trimmed) return;
    const topicKey = detectTopicKey(trimmed);
    handleAsk(trimmed, topicKey, trimmed);
    setUserQ("");
  }

  return (
    <div style={containerStyle}>
      <div style={shellStyle}>
        {/* Header */}
        <div style={headerStyle}>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <img
              src={logo}
              alt="Retirement Readiness Logo"
              style={{ width: 60, height: 60 }}
            />

            <div style={brandStyle}>
              <div style={titleStyle}>Retirement Readiness</div>
              <div style={subtitleStyle}>
                A grounded, citation-based retirement assistant with validation and scenario-based financial logic.
              </div>
            </div>
          </div>

          <div
            style={{
              ...badgeStyle,
              background:
                status === "connected"
                  ? "rgba(46,229,157,0.14)"
                  : status === "error"
                  ? "rgba(255,107,107,0.14)"
                  : "rgba(246,196,69,0.14)",
              color:
                status === "connected"
                  ? "#2EE59D"
                  : status === "error"
                  ? "#FF6B6B"
                  : "#F6C445",
            }}
          >
            {status === "connected"
              ? "Connected"
              : status === "error"
              ? "Offline"
              : "Checking..."}
          </div>
        </div>

        {/* Main Topic Buttons */}
        <TopicButtons
          buttons={topic_buttons}
          loading={loading}
          selectedQuestion={selectedQuestion}
          onAsk={handleAsk}
          buttonStyle={buttonStyle}
          buttonRowStyle={buttonRowStyle}
        />

                {/* Suggested follow-ups */}
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap", padding: "0 6px" }}>
          {!loading &&
            suggestedButtons.map((item, index) => (
              <button
                key={index}
                onClick={() => handleAsk(item.prompt, activeTopicKey, item.label)}
                style={suggestionStyle}
              >
                {item.label}
              </button>
            ))}
        </div>

        {/* Free-text input */}
        <div style={{ display: "flex", gap: 10, padding: "0 6px" }}>
          <input
            value={userQ}
            onChange={(e) => setUserQ(e.target.value)}
            placeholder="Ask anything..."
            disabled={loading}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleSendCustomQuestion();
            }}
            style={{
              flex: 1,
              padding: "12px 14px",
              borderRadius: 12,
              border: "1px solid rgba(255,255,255,0.12)",
              background: "rgba(255,255,255,0.06)",
              color: "#EAF0FF",
              outline: "none",
              fontSize: 14,
            }}
          />
          <button
            onClick={handleSendCustomQuestion}
            disabled={loading || !userQ.trim()}
            style={{
              padding: "12px 16px",
              borderRadius: 12,
              border: "none",
              background: "#5B8CFF",
              color: "#fff",
              fontWeight: 600,
              cursor: loading || !userQ.trim() ? "not-allowed" : "pointer",
              opacity: loading || !userQ.trim() ? 0.6 : 1,
            }}
          >
            Send
          </button>
        </div>

        {/* Scenario form */}
        <ScenarioForm onSubmit={handleScenario} loading={loading} />

        {selectedQuestion && <div style={selectedQuestionStyle}>{selectedQuestion}</div>}
        {error && <div style={errorStyle}>{error}</div>}

        {loading && (
          <div style={{ ...bubbleStyle, opacity: 0.6 }}>
            <span>Thinking…</span>
          </div>
        )}

        {!loading && answer && (
          <AnswerBubble
            citation={citation}
            answer={answer_body}
            sources={sources}
            validated={validated}
            isRefusal={isRefusal}
            originalAnswer={originalAnswer}
            grounding_report={grounding_report}
            bubbleStyle={bubbleStyle}
            validatedPill={validatedPill}
            correctedPill={correctedPill}
          />
        )}

        <HistoryList
          history={history}
          bubbleStyle={bubbleStyle}
          validatedPill={validatedPill}
          correctedPill={correctedPill}
          selectedQuestionStyle={selectedQuestionStyle}
        />
      </div>
    </div>
  );
}