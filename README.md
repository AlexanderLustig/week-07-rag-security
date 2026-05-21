# RAG Security Knowledge Assistant

**Problem:** Security analysts need fast, reliable access to threat intelligence without context-switching to external tools. When responding to an incident, seconds matter.

**Solution:** A retrieval-augmented generation (RAG) chatbot that grounds an LLM in curated security knowledge (MITRE ATT&CK, NIST frameworks) and returns relevant tactics, techniques, and mitigations in real time.

**Why this matters:** RAG demonstrates how to make LLMs useful for domain-specific tasks by combining vector search + LLM reasoning. This pattern applies across security, compliance, legal, and financial workflows.

## Live Demo

🔗 [Try the chatbot](https://cloud.flowiseai.com/chatbot/2b7b85b7-f7d6-4d2d-99de-97da2b34d9ee)

**Example queries:**
- "What MITRE techniques are used in credential theft attacks?"
- "How does NIST CSF address data protection?"
- "What's the difference between Initial Access and Persistence?"

## What I Built

| Component | Details |
|-----------|---------|
| **Knowledge Base** | 5 markdown documents covering MITRE ATT&CK (Initial Access, Credential Access, Lateral Movement, Defense Evasion) + NIST Cybersecurity Framework |
| **LLM Chain** | Conversational Retrieval QA in Flowise, using OpenAI `gpt-4o-mini` at low temperature (0.3) for consistency |
| **Vector Store** | Flowise in-memory embeddings with OpenAI `text-embedding-ada-002` |
| **Testing** | 5 questions + edge case analysis (out-of-scope queries, multi-turn conversation) |

## Stack

- **Platform:** Flowise Cloud
- **LLM:** OpenAI gpt-4o-mini
- **Embeddings:** OpenAI text-embedding-ada-002
- **Vector Search:** Flowise in-memory

## What I Learned

1. **RAG is a framework, not magic** — quality depends entirely on knowledge base curation. Garbage in = garbage out.
2. **Temperature tuning matters for consistency** — Setting temp=0.3 gave reliable, factual responses; higher temps hallucinated.
3. **Context window limitations** — Flowise truncated long NIST documents; had to split into sections.
4. **Testing RAG is different from testing LLMs** — Need to test both relevance (are right docs retrieved?) and generation quality (is the answer correct given the docs?).

## Full Report

See [`week-07-report.md`](./week-07-report.md) for detailed test results, edge cases, and design reflection.

## Files

- `rag-documents/` — Knowledge base source files (Markdown)
- `week-07-report.md` — Full test report with test cases + evaluation
- `screenshots/` — Chatbot interface screenshots

---

**Portfolio Signal:** This project shows I can architect a domain-specific AI system, not just prompt an LLM. It demonstrates understanding of retrieval (vector search), grounding (RAG patterns), and evaluation (testing LLM outputs against expected behavior).
