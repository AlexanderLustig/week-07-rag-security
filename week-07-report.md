# Week 7 Report: RAG Systems for Security Knowledge

## Setup Summary

### LLM
- **Provider:** OpenAI
- **Model:** `gpt-4o-mini`
- **Temperature:** 0.3 (tuned for factual retrieval over creativity)
- **Platform:** Flowise Cloud (free tier)

### Embeddings
- **Provider:** OpenAI
- **Model:** `text-embedding-ada-002`
- **Chunk size:** 1000 tokens | **Chunk overlap:** 200 tokens

### Documents Loaded (5 files)
| File | Topic | Approx. Size |
|------|-------|-------------|
| `mitre-initial-access.txt` | MITRE ATT&CK TA0001 – 6 techniques | ~800 words |
| `mitre-credential-access.txt` | MITRE ATT&CK TA0006 – 6 techniques | ~800 words |
| `mitre-lateral-movement.txt` | MITRE ATT&CK TA0008 – 7 techniques | ~750 words |
| `mitre-defense-evasion.txt` | MITRE ATT&CK TA0005 – 6 techniques | ~750 words |
| `nist-csf-framework.txt` | NIST CSF 2.0 – all 6 functions | ~800 words |

**Vector store:** In-Memory (Flowise built-in)
**Chatflow used:** Conversational Retrieval QA Chain with "Return Source Documents" enabled

---

## Test Results

### 5 Core Questions

| # | Question | Doc Used? | Quality | Notes |
|---|----------|-----------|---------|-------|
| 1 | What techniques do attackers use for credential access? | ✅ Yes | **Good** | Listed T1110 (brute force), T1003 (OS credential dumping), T1558.003 (Kerberoasting), T1056 (input capture), T1539 (session cookie theft), T1552 (unsecured credentials). Complete coverage of all 6 techniques in the document. |
| 2 | What are common initial access techniques according to MITRE ATT&CK? | ✅ Yes | **Good** | Covered phishing (T1566), exploiting public-facing apps (T1190), external remote services (T1133), valid accounts (T1078), supply chain compromise (T1195), drive-by compromise (T1189). |
| 3 | How can attackers move laterally through a network after gaining access? | ✅ Yes | **Good** | Explained Remote Services (T1021), Pass the Hash (T1550.002), Pass the Ticket (T1550.003), internal spearphishing (T1534), and taint shared content (T1080). |
| 4 | What is defense-in-depth and what are its layers according to NIST? | ⚠️ Partial | **Partial** | Responded "Hmm, I'm not sure." The term "defense-in-depth" isn't explicitly in the NIST CSF document — the model correctly refused to hallucinate rather than fabricate an answer. |
| 5 | How do attackers avoid detection after compromising a system? | ✅ Yes | **Good** | Covered defense evasion techniques: disabling AV (T1562), log clearing (T1070), obfuscated files (T1027), process injection (T1055), masquerading (T1036), and LOLBins (T1218). |

**Overall: 4/5 Good, 1/5 Partial**

---

## Edge Case Observations

### Off-topic questions tested

**Q: "What is the weather today in New York?"**
> Response: *"Hmm, I'm not sure."*

**Result:** Correctly refused — no hallucination. The RAG system appropriately declined to answer questions outside its knowledge base.

---

**Q: "How do I make pasta carbonara?"**
> Response: *"Hmm, I'm not sure."*

**Result:** Correct behavior — stayed on-topic. The low temperature (0.3) and retrieval-grounded architecture prevented creative out-of-scope answers.

---

**Q: "Who won the 2024 Super Bowl?"**
> Response: *"Hmm, I'm not sure."*

**Result:** Correct — no hallucination. The RAG chain retrieved nothing relevant and deferred appropriately rather than using training data.

---

## Reflection

### What surprised me?

**1. RAG grounding is remarkably effective at reducing hallucination.** Without RAG, LLMs confidently fabricate procedure examples and CVE numbers. With the documents loaded, every claim was traceable to a specific chunk — the "Return Source Documents" toggle made this visible in real time.

**2. Chunk overlap matters.** At chunk size 1000 / overlap 200, concepts that span page boundaries (like a technique description + its detection guidance) were preserved in the same or adjacent chunks. A smaller overlap would have broken some multi-part answers.

**3. Semantic embeddings handle paraphrase well.** The `text-embedding-ada-002` model correctly retrieved credential access documents when asked about "credential theft" even though that exact phrase didn't appear in the text. Dense vector search outperforms keyword search for this use case.

**4. Temperature matters for this use case.** At T=0.3, the model cited specifics from the documents. Higher temperatures produce more verbose answers that occasionally mix document content with training data, diluting accuracy.

**5. Flowise v3 requires variable references in chatflow JSON.** Unlike v2, Flowise v3 uses `{{nodeId.data.instance}}` variable references in node inputs to wire dependencies at runtime. Without these references, nodes receive `undefined` for connected inputs — this was the root cause of all failures during initial API-based setup.

### How could this be improved?

1. **Better chunking strategy:** Chunk by technique (each T-number as a unit) rather than fixed character counts. This would ensure complete technique descriptions aren't split across chunks.

2. **Hybrid search:** Combine dense vector search (semantic) with BM25 keyword search. This would improve retrieval for specific CVE numbers, tool names (e.g., "Mimikatz"), and technique IDs (e.g., "T1003.001").

3. **Larger knowledge base:** Load the full MITRE ATT&CK STIX JSON (15,000+ techniques) and NIST SP 800-53 controls for production-quality answers.

4. **Re-ranking:** Add a cross-encoder re-ranking step after initial retrieval to improve the quality of the top-k chunks passed to the LLM.

5. **Persistent vector store:** Replace In-Memory store with a persistent option (Pinecone, Chroma, Supabase pgvector) so documents don't need to be re-embedded on every chatflow load.

---

## Chatbot Share Link

🔗 [Security Knowledge Assistant](https://cloud.flowiseai.com/chatbot/2b7b85b7-f7d6-4d2d-99de-97da2b34d9ee)

---

## Screenshots

| Screenshot | File |
|------------|------|
| Flowise dashboard | `screenshots/flowise-dashboard.png` |
| Complete RAG chatflow canvas | `screenshots/rag-chatflow.png` |
| Response with source documents | `screenshots/rag-response-with-sources.png` |
| Chatbot share panel | `screenshots/chatbot-share-link.png` |
