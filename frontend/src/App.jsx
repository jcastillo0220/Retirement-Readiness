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
    activeTopicKey,
    handleAsk,
    handleScenario,
  } = useAIChat();

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

  const latestItem = history.length ? history[history.length - 1] : null;
  const olderHistory = history.length > 1 ? history.slice(0, -1) : [];

  return (
    <div style={containerStyle}>
      <div style={shellStyle}>
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

        <TopicButtons
          buttons={topic_buttons}
          loading={loading}
          selectedQuestion={selectedQuestion}
          onAsk={handleAsk}
          buttonStyle={buttonStyle}
          buttonRowStyle={buttonRowStyle}
        />

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

        <ScenarioForm onSubmit={handleScenario} loading={loading} />

        {selectedQuestion && <div style={selectedQuestionStyle}>{selectedQuestion}</div>}
        {error && <div style={errorStyle}>{error}</div>}

        {loading && (
          <div style={{ ...bubbleStyle, opacity: 0.6 }}>
            <span>Thinking…</span>
          </div>
        )}

        {!loading && answer && latestItem && (
          <AnswerBubble
            answer={answer}
            projection={latestItem.projection} 
            citation={latestItem.citation || ""}
            answer_body={latestItem.answer_body || ""}
            sources={latestItem.sources || ""}
            grounding_report={latestItem.grounding_report || []}
            validated={validated}
            originalAnswer={originalAnswer}
            bubbleStyle={bubbleStyle}
            validatedPill={validatedPill}
            correctedPill={correctedPill}
          />
        )}

        <HistoryList
          history={olderHistory}
          bubbleStyle={bubbleStyle}
          validatedPill={validatedPill}
          correctedPill={correctedPill}
          selectedQuestionStyle={selectedQuestionStyle}
        />
      </div>
    </div>
  );
}