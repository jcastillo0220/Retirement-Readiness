import { useState } from "react";
import { askAI } from "./api";

// npm run dev
// ^This will run the program in development mode. Open http://localhost:5173 to view it in the browser.

export default function AIChat() {
  const [answer, setAnswer] = useState("");

  async function handleAsk() {
    console.log("Button clicked");
    const res = await askAI("can you explain what Roth IRA as simple and formally as you can." 
      + "Do not include an example." 
      + "Make it as short as possible and use simple language.");
    console.log("Response from backend:", res);
    setAnswer(res.answer);
  }

  const bubbleStyle = {
  backgroundColor: "#e8f0fe",
  padding: "12px 16px",
  borderRadius: "12px",
  maxWidth: "300px",
  fontSize: "16px",
  lineHeight: "1.4",
  marginTop: "12px",
};

const buttonStyle = {
  padding: "10px 18px",
  backgroundColor: "#4a90e2",
  color: "white",
  border: "none",
  borderRadius: "8px",
  fontSize: "1rem",
  cursor: "pointer",
  marginBottom: "12px",
};


return (
  <div
    style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
    }}
  >
    <button onClick={handleAsk} style={buttonStyle}>
      What is Roth IRA?</button>
    <p style={bubbleStyle}>{answer}</p>
  </div>
);
}
