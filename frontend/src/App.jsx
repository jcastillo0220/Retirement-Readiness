import { useAIChat } from "./useAIChat";
import ScenarioForm from "./components/scenarioForm";
import TopicButtons from "./components/topicButtons";
import AnswerBubble from "./components/answerBubble";
import HistoryList from "./components/historyList";
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
    handleAsk,
    handleScenario,
  } = useAIChat();

const topic_buttons = [
  { label: "What is a Roth IRA?", prompt: "What is a Roth IRA?", key: "roth_ira" },
  { label: "What is a 401(k)?", prompt: "What is a 401(k)?", key: "401k" },
  { label: "What is a Traditional IRA?", prompt: "What is a Traditional IRA?", key: "traditional_ira" },
  { label: "What is a Rollover IRA?", prompt: "What is a Rollover IRA?", key: "rollover_ira" },
  { label: "What is a Roth 401(k)?", prompt: "What is a Roth 401(k)?", key: "roth_401k" },
];

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
                onClick={() => handleAsk(item.prompt, item.label, null)}
                style={suggestionStyle}
              >
                {item.label}
              </button>
            ))}
        </div>

        {/* User Input Scenario Form */}
        <ScenarioForm onSubmit={handleScenario} />

        {selectedQuestion && <div style={selectedQuestionStyle}>{selectedQuestion}</div>}
        {error && <div style={errorStyle}>{error}</div>}

        {!loading && answer && (
          <AnswerBubble
            answer={answer}
            validated={validated}
            originalAnswer={originalAnswer}
            projection={history[history.length - 1]?.projection}
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