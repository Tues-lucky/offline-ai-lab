# Lab log

Newest first. A few lines a day: what I tried, what happened, what I learned, what's next.

---

## 2026-11-09
- **Tried:** Script to detect garbled OCR spans in Docling output and replace them with `[UNREADABLE: clause, check original page]`.
- **Result:** Found all 10 garbled spans in the scanned lease, with the right clause numbers (inferred from the previous clause when OCR lost the number).
- **Learned:** OCR failures are silent. Docling reports "success" even when key clauses are unreadable.
- **Next:** Re-test the clause 7.2 question with the marked file and a new rule: "If text is marked [UNREADABLE], say so and ask the user to check the original."

## 2026-11-06
- **Tried:** Image-only scan of the lease (slight skew, blur, specks). Default extraction, then Docling Serve (CPU, OCR auto, TableFormer accurate).
- **Result:** Default extraction: no text, model answered "Not found". Docling: tables recovered perfectly (`| Handover Date | 1 December 2026 |`), all amounts correct, but about 10 lines garbled, including the key risk clauses.
- **Learned:** The model **made up** clause 7.2 from garbled text ("re-let or put the Premises to better use") and presented it in quotation marks with a source chip. Half-readable text is worse than no text.
- **Next:** Mark unreadable spans before indexing; check that every quote in an answer exists in the source.

## 2026-11-05
- **Tried:** Last B-set question (draft an HR email from the non-compete clause). Then the date-conflict question with `grep` instructions and a table-flattened PDF.
- **Result:** Email 1.75/2 (missed non-solicitation and notice period). With the original PDF the fast model missed the conflict even when told to grep: the table row split into two lines, so the date never reached the model. With one line per table row it caught 15 Dec vs 1 Dec in **7 s** (thinking model: 35 s).
- **Learned:** Read `prompt_token/s` to see caching: tens of thousands = fully cached, thousands = partly cached, hundreds = read from scratch.
- **Next:** OCR for scanned documents.

## 2026-11-01 to 11-04 (setup week)
- **Set up:** Ollama on MacBook Air M4 32 GB; Qwen 3.5 9B and 3.8 27B; Open WebUI in Docker with Ollama embeddings and offline mode (a first attempt hung downloading an embedding model from the internet).
- **A-set (no documents):** 9B scored 10.5/14. Thinking off was better at language tasks; thinking on was better at reasoning. 27B was better on law but still invented ordinance numbers.
- **Made test documents:** five fictitious Hong Kong-style contracts with traps (conflicting dates, ambiguous break clause, rent-free terms only in a schedule, governing law vs arbitration seat).
- **Retrieval fixes:** Top K 3 → 8 and hybrid search fixed answers pulled from the wrong contract. Turning off background title/tag generation cut answers from 1 min 57 s to 4 s.
- **Routing:** Two model presets: fast (thinking off) for lookups, deep (thinking on) for classification, comparison and conflicts. Thinking fixed a question where the model quoted "English law" and then classified it as Hong Kong law.
