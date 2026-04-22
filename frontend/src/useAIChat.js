import { useState, useRef } from "react";
import { askAI, runScenario } from "./api";
 
export function useAIChat() {
  const [answer, setAnswer] = useState("");
  const [citation, setCitation] = useState("");
  const [answer_body, setAnswerBody] = useState("");
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
  const [grounding_report, setGroundingReport] = useState([]);
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
      setGroundingReport(res?.grounding_report || []);
 
      setHistory((prev) => [
        ...prev,
        {
          id,
          label: questionLabel,
          prompt: finalPrompt,
          topicKey: finalTopicKey,
          answer: finalAnswer,
          citation: res?.citation ?? "",
          answer_body: res?.answer_body ?? finalAnswer,
          sources: res?.sources ?? "",
          validated: isValid,
          originalAnswer: orig,
          timestamp: Date.now(),
          cached: !!res?.cached,
          grounding_report: res?.grounding_report || [],
        },
      ]);
    } catch (err) {
      if (id === requestIdRef.current) {
        // Detect network drop or backend offline
        if (err?.message?.includes("Failed to fetch")) {
          setError("The backend is not reachable. It may be offline or there is a network issue.");
        } 
        // Detect 500 or other server errors
        else if (err?.message?.includes("500")) {
          setError("The backend returned an error (500). Please try again.");
        } 
        // Fallback
        else {
          setError("The backend is not working properly. Please try again.");
        }
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

    // Extract all fields returned by backend
    const {
      projection,
      answer,
      citation,
      answer_body,
      sources,
      validated,
      original_answer,
      grounding_report,
    } = res;

    // Set all UI fields just like handleAsk()
    setAnswer(answer || "");
    setCitation(citation || "");
    setAnswerBody(answer_body || "");
    setSources(sources || "");
    setGroundingReport(grounding_report || []);
    setValidated(validated ?? true);
    setOriginalAnswer(original_answer || null);
    setIsRefusal(res?.is_refusal ?? false);

    // Save to history
    setHistory((prev) => [
      ...prev,
      {
        id,
        label: "Personalized Scenario",
        prompt: JSON.stringify(inputs),
        topicKey: "scenario",
        answer: answer_body || "",
        validated: validated ?? true,
        originalAnswer: original_answer || null,
        timestamp: Date.now(),
        cached: false,
        projection,
        grounding_report: grounding_report || [],
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
    answer_body,
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
    grounding_report,
    activeTopicKey,
    handleAsk,
    handleScenario,
  };
}