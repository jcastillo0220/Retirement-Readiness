import { useState, useRef } from "react";
import { askAI, runScenario } from "./api";

export function useAIChat() {
  const [citation, setCitation] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState("");
  const [suggestedButtons, setSuggestedButtons] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedQuestion, setSelectedQuestion] = useState("");
  const [validated, setValidated] = useState(true);
  const [originalAnswer, setOriginalAnswer] = useState(null);
  const [error, setError] = useState(null);
  const [labelPrompt, setLabelPrompt] = useState(null);
  const [history, setHistory] = useState([]);
  const [supported_phrases, setSupportedPhrases] = useState([]);

  const requestIdRef = useRef(0);

  // UPDATED SIGNATURE: (prompt, topicKey, label)
  async function handleAsk(prompt, topicKey, label) {
    const id = ++requestIdRef.current;

    const finalPrompt = prompt;               // AI receives full prompt
    const finalTopicKey = topicKey || "definitions";
    const questionLabel = label;              // UI shows short label ONLY

    setSelectedQuestion(questionLabel || "");       
    setValidated(true);
    setOriginalAnswer(null);
    setError(null);
    setLoading(true);

    try {
      const res = await askAI({
        question: finalPrompt,
        topicKey: finalTopicKey,
        label: questionLabel
      });

      if (id !== requestIdRef.current) return;

      const finalAnswer = res?.answer ?? "";
      const suggestions = res?.suggestions ?? [];
      const isValid = res?.validated ?? true;
      const orig = res?.original_answer ?? null;

      setCitation(res?.citation || "");
      setAnswer(finalAnswer);
      setSources(res?.sources || "");
      setSuggestedButtons(suggestions);
      setValidated(isValid);
      setOriginalAnswer(orig);
      setLabelPrompt(res?.label_prompt || null);
      setSupportedPhrases(res?.supported_phrases || []);

      setHistory((prev) => [
        ...prev,
        {
          id,
          label: questionLabel,
          prompt: finalPrompt,
          topicKey: finalTopicKey,
          answer: finalAnswer,
          citation: res?.citation || "",
          sources: res?.sources || "",
          validated: isValid,
          originalAnswer: orig,
          timestamp: Date.now(),
          cached: !!res?.cached,
          supported_phrases: res?.supported_phrases || [],
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
    citation,
    sources,
    suggestedButtons,
    loading,
    selectedQuestion,
    validated,
    originalAnswer,
    error,
    labelPrompt,
    history,
    supported_phrases,
    handleAsk,
    handleScenario,
  };
}