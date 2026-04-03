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
    suggestedButtons,
    loading,
    selectedQuestion,
    validated,
    originalAnswer,
    error,
    history,
    supported_phrases,
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

  function handleSendCustomQuestion() {
    const trimmed = userQ.trim();
    if (!trimmed) return;
    handleAsk(trimmed, "definitions", trimmed);
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
            answer={answer}
            validated={validated}
            originalAnswer={originalAnswer}
            supported_phrases={supported_phrases}
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