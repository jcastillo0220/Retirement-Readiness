import { useState } from "react";
import { askAI } from "./api";

// npm run dev
// ^This will run the program in development mode. Open http://localhost:5173 to view it in the browser.

export default function AIChat() {
  const [answer, setAnswer] = useState("");

  async function handleAsk() {
    console.log("Button clicked");
    const res = await askAI("can you explain what Roth IRA as simple and formally as you can. Do not include an example.");
    console.log("Response from backend:", res);
    setAnswer(res.answer);
  }

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
      <button onClick={handleAsk}>What is Roth IRA?</button>
      <p>{answer}</p>
    </div>
  );
}
