import { useState } from "react";
import { askAI } from "./api";

export default function AIChat() {
  const [answer, setAnswer] = useState("");

  async function handleAsk() {
    console.log("Button clicked");
    const res = await askAI("How should I start saving money?");
    console.log("Response from backend:", res);
    setAnswer(res.answer);
  }

  return (
    <div>
      <button onClick={handleAsk}>Ask AI</button>
      <p>{answer}</p>
    </div>
  );
}
