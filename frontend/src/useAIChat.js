import { useState, useRef } from "react";
import { askAI, runScenario } from "./api";

export function useAIChat() {
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
    const id = ++requestIdRef.current;

    const questionLabel = label || "What is a Roth IRA?";
    const finalPrompt = typeof prompt === "string" ? prompt : questionLabel;

    setSelectedQuestion(questionLabel);
    setValidated(true);
    setOriginalAnswer(null);
    setError(null);
    setLoading(true);

    try {
      const res = await askAI({ question: finalPrompt, topicKey, label });
      if (id !== requestIdRef.current) return;

      const finalAnswer = res?.answer ?? "";
      const suggestions = res?.suggestions ?? [];
      const isValid = res?.validated ?? true;
      const orig = res?.original_answer ?? null;

      setAnswer(finalAnswer);
      setSuggestedButtons(suggestions);
      setValidated(isValid);
      setOriginalAnswer(orig);
      setLabelPrompt(res?.label_prompt || null);

      setHistory((prev) => [
        ...prev,
        {
          id,
          label: questionLabel,
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
      if (id === requestIdRef.current) setError("Something went wrong.");
    } finally {
      if (id === requestIdRef.current) setLoading(false);
    }
  }

  async function handleScenario(inputs) {
    const id = ++requestIdRef.current;

    setSelectedQuestion("Personalized Scenario");
    setLoading(true);
    setError(null);

    try {
      const res = await runScenario({
        age: Number(inputs.age),
        retirement_age: Number(inputs.retirement_age),
        annual_income: Number(inputs.annual_income),
        current_savings: Number(inputs.current_savings),
        monthly_contribution: Number(inputs.monthly_contribution),
      });
      
      if (id !== requestIdRef.current) return;

      const { projection, explanation } = res;

      setAnswer(explanation);
      setSuggestedButtons([]);
      setValidated(true);
      setOriginalAnswer(null);

      setHistory((prev) => [
        ...prev,
        {
          id,
          label: "Personalized Scenario",
          prompt: JSON.stringify(inputs),
          topicKey: "scenario",
          answer: explanation,
          validated: true,
          originalAnswer: null,
          timestamp: Date.now(),
          cached: false,
          projection,
        },
      ]);
    } catch (err) {
      if (id === requestIdRef.current) setError("Scenario failed.");
    } finally {
      if (id === requestIdRef.current) setLoading(false);
    }
  }

  return {
    answer,
    suggestedButtons,
    loading,
    selectedQuestion,
    validated,
    originalAnswer,
    error,
    labelPrompt,
    history,
    handleAsk,
    handleScenario,
  };
}