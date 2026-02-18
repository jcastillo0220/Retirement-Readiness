import { useState } from "react";
import { askAI } from "./api";
import { bubbleStyle, buttonStyle } from "./styles";

import ReactMarkdown from "react-markdown";

export default function AIChat() {
  const [answer, setAnswer] = useState("");
  const [suggestedButtons, setSuggestedButtons] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedQuestion, setSelectedQuestion] = useState("");

 async function handleAsk(question) {
  setLoading(true);

  const prompt =
    typeof question === "string"
      ? question
      : "can you explain what is Roth IRA." +
        "Do not include an example. Make it as short as possible and use simple language. Base your definition off from this website: https://www.fidelity.com/learning-center/smart-money/what-is-a-roth-ira";

  // Save the question the user clicked
  setSelectedQuestion(prompt);

  const res = await askAI(prompt);

  setAnswer(res.answer);
  setSuggestedButtons(res.suggestions || []);
  setLoading(false);
  }

  {selectedQuestion && !loading && (
  <div
    style={{
      maxWidth: "70%",
      alignSelf: "flex-end",
      backgroundColor: "#d1e7ff",
      padding: "10px 16px",
      borderRadius: "16px",
      marginTop: "16px",
      marginBottom: "8px",
      color: "#003366",
      fontWeight: "500",
      boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
    }}
  >
    {selectedQuestion}
  </div>
  )}

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
      <button
        onClick={() => handleAsk()}
        style={{
          ...buttonStyle,
          opacity: loading ? 0.6 : 1,
          cursor: loading ? "not-allowed" : "pointer",
        }}
        disabled={loading}
      >
        {loading ? "Thinking..." : "What is Roth IRA?"}
      </button>

      {loading && (
        <div
          style={{
            backgroundColor: "#e8f0fe",
            padding: "10px 16px",
            borderRadius: "12px",
            marginTop: "12px",
            fontStyle: "italic",
            opacity: 0.7,
          }}
        >
          AI is thinking…
        </div>
      )}

      {!loading && (
        <div style={bubbleStyle}>
          <ReactMarkdown>{answer}</ReactMarkdown>
        </div>
      )}

      {!loading &&
        suggestedButtons.map((item, index) => (
          <button
            key={index}
            onClick={() => handleAsk(item.prompt)}
            style={{
              padding: "8px 14px",
              backgroundColor: "#4a90e2",
              color: "white",
              border: "none",
              borderRadius: "8px",
              fontSize: "0.9rem",
              cursor: "pointer",
              marginTop: "8px",
            }}
          >
            {item.label}
          </button>
        ))}
    </div>
  );
}