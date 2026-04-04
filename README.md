# Week 7 – RAG Security Knowledge Assistant

## Deliverables

| Item | Status |
|------|--------|
| Flowise chatflow built | ✅ |
| OpenAI LLM connected | ✅ |
| 5 knowledge base documents | ✅ |
| RAG chatbot tested (5 questions) | ✅ |
| Edge case testing | ✅ |
| Chatbot shared | ✅ |
| Report written | ✅ |
| Screenshots captured | ✅ |

## Chat Link

🔗 [Security Knowledge Assistant](https://cloud.flowiseai.com/chatbot/2b7b85b7-f7d6-4d2d-99de-97da2b34d9ee)

## Knowledge Base Documents

- `rag-documents/mitre-initial-access.txt` – MITRE ATT&CK Initial Access (TA0001)
- `rag-documents/mitre-credential-access.txt` – MITRE ATT&CK Credential Access (TA0006)
- `rag-documents/mitre-lateral-movement.txt` – MITRE ATT&CK Lateral Movement (TA0008)
- `rag-documents/mitre-defense-evasion.txt` – MITRE ATT&CK Defense Evasion (TA0005)
- `rag-documents/nist-csf-framework.txt` – NIST Cybersecurity Framework 2.0

## Stack

- **LLM:** OpenAI → gpt-4o-mini (temp 0.3)
- **Embeddings:** OpenAI text-embedding-ada-002
- **Vector Store:** Flowise In-Memory
- **Chain:** Conversational Retrieval QA Chain
- **Platform:** Flowise Cloud

## Report

See [`week-07-report.md`](./week-07-report.md) for full test results, edge case analysis, and reflection.
