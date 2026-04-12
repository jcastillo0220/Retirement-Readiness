import { useState, useRef } from "react";
import { askAI, runScenario } from "./api";
 
export function useAIChat() {
  const [answer, setAnswer] = useState("");
  const [citation, setCitation] = useState("");
  const [answerBody, setAnswerBody] = useState("");
  const [sources, setSources] = useState("");
  const [isRefusal, setIsRefusal] = useState(false);
  const [suggestedButtons, setSuggestedButtons] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedQuestion, setSelectedQuestion] = useState("");
  const [validated, setValidated] = useState(true);
  const [originalAnswer, setOriginalAnswer] = useState(null);
  const [error, setError] = useState(null);
  const [labelPrompt, setLabelPrompt] = useState(null);
  const [history, setHistory] = useState([]);
  const [supported_phrases, setSupportedPhrases] = useState([]);
  const [activeTopicKey, setActiveTopicKey] = useState("definitions");
 
  const requestIdRef = useRef(0);
 
  async function handleAsk(prompt, topicKey, label) {
    const id = ++requestIdRef.current;
 
    const finalPrompt = prompt;
    const finalTopicKey = topicKey || "definitions";
    const questionLabel = label || prompt;
 
    setSelectedQuestion(questionLabel);
    setActiveTopicKey(finalTopicKey);
    setValidated(true);
    setOriginalAnswer(null);
    setError(null);
    setLoading(true);
 
    try {
      const res = await askAI({
        question: finalPrompt,
        topicKey: finalTopicKey,
        label: questionLabel,
      });
 
      if (id !== requestIdRef.current) return;
 
      const finalAnswer = res?.answer ?? "";
      const suggestions = res?.suggestions ?? [];
      const isValid = res?.validated ?? true;
      const orig = res?.original_answer ?? null;
 
      setAnswer(finalAnswer);
      setCitation(res?.citation ?? "");
      setAnswerBody(res?.answer_body ?? finalAnswer);
      setSources(res?.sources ?? "");
      setIsRefusal(res?.is_refusal ?? false);
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
          validated: isValid,
          originalAnswer: orig,
          timestamp: Date.now(),
          cached: !!res?.cached,
          supported_phrases: res?.supported_phrases || [],
        },
      ]);
    } catch (err) {
      if (id === requestIdRef.current) {
        setError(err?.message || "Something went wrong.");
      }
    } finally {
      if (id === requestIdRef.current) setLoading(false);
    }
  }
 
  async function handleScenario(inputs) {
    const id = ++requestIdRef.current;
 
    setSelectedQuestion("Personalized Scenario");
    setActiveTopicKey("scenario");
    setLoading(true);
    setError(null);
    setSuggestedButtons([]);
    setOriginalAnswer(null);
    setValidated(true);
 
    try {
      const res = await runScenario({
        age: Number(inputs.age),
        retirement_age: Number(inputs.retirement_age),
        annual_income: Number(inputs.annual_income),
        current_savings: Number(inputs.current_savings),
        monthly_contribution: Number(inputs.monthly_contribution),
        return_rate:
          inputs.return_rate !== undefined
            ? Number(inputs.return_rate)
            : undefined,
      });
 
      if (id !== requestIdRef.current) return;
 
      const { projection, explanation } = res;
 
      setAnswer(explanation || "");
      setSupportedPhrases([]);
 
      setHistory((prev) => [
        ...prev,
        {
          id,
          label: "Personalized Scenario",
          prompt: JSON.stringify(inputs),
          topicKey: "scenario",
          answer: explanation || "",
          validated: true,
          originalAnswer: null,
          timestamp: Date.now(),
          cached: false,
          projection,
        },
      ]);
    } catch (err) {
      if (id === requestIdRef.current) {
        setError(err?.message || "Scenario failed.");
      }
    } finally {
      if (id === requestIdRef.current) setLoading(false);
    }
  }
 
  return {
    answer,
    citation,
    answerBody,
    sources,
    isRefusal,
    suggestedButtons,
    loading,
    selectedQuestion,
    validated,
    originalAnswer,
    error,
    labelPrompt,
    history,
    supported_phrases,
    activeTopicKey,
    handleAsk,
    handleScenario,
  };
}