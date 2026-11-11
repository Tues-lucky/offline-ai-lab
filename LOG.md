# Lab log

Newest first. A few lines a day: what I tried, what happened, what I learned, what's next.

---

## 2026-11-11
- **Tried:** Changed `ocr_check.py` to mark the **whole sentence** as unreadable, not just the garbled words (`--span` keeps the old behaviour). Clause numbers and table cell names are kept. Re-ran the clause 7.2 and management fee questions, first with knowledge-base search, then with the whole contract in context.
- **Result (search):** No invented text in any run (yesterday: one invented clause and quote). But the 7.2 line is now almost empty, so vector search no longer finds it: the model said "Clause 7.2 does not exist". It grepped for `Clause 7\.2`, while the document only says `- 7.2`. After a prompt tip to grep the number alone, it found "7.2" in three contracts and answered from the consultancy agreement, ignoring "Landlord" in the question. The quoted text was real, which makes this error more convincing than an invented one.
- **Result (full context):** Clause 7.2, two runs: both said the clause is marked unreadable and cannot be answered, and kept clause 4.3 separate. No invented text, no wrong document. Management fee: right conclusion ("yes, pays") but wrong reason: it cited clause 2.2, which covers the fit-out period before the term, not the rent-free period in Schedule 2 and the unreadable clause 3.2.
- **Result (control):** Same full-context test with the old word-only marking (`--span`), so fragments like "rTue" and "compensationfor" stay. Two runs, two different guesses: "re-let" and "redevelop". Both borrowed "without prejudice to the Landlord's accrued rights" from clause 7.3, and the second cited "standard legal drafting", breaking the no-outside-knowledge rule. Whole-sentence marking and full context are both needed; neither works alone.
- **Result (thinking on):** Management fee question with the full contract and thinking on, two runs. Both again cited clause 2.2 as the rule for the rent-free period, and neither mentioned that clause 3.2 is unreadable. In run 1 the model's reasoning noticed the dates did not line up, then dismissed it. The model builds an answer from the text it has rather than asking what is missing.
- **Learned:** Full context removed every search problem for single-document questions. `prompt_eval_count` shows whether the document was actually included (~2,700 tokens with the contract vs ~330 without); two runs were invalid because the file was not attached, so the product should make "read the whole document" the default.
- **Learned:** Clause numbers repeat across documents. For single-document questions, picking the document first avoids the problem. Cross-document search will need every chunk to carry the document's name and an explicit "Clause 7.2" label; not needed yet.
- **Learned:** The OCR script's rules fit this one document: "7.2"-style numbering, Docling Markdown, English sentences, an English-only junk test. Chinese text would be flagged almost everywhere. Better OCR will also produce fewer garbled words but more *plausible* errors (15 → 16, a dropped "not"), which pattern checks cannot catch.
- **Next:** Warning banner listing unreadable clauses on every answer about that document. Measure how much a realistic scan (300 dpi, light blur) actually breaks. Then move to the next feature: an offline email assistant, followed by a contract summary table.

## 2026-11-10
- **Tried:** Uploaded the marked scan (`_checked.md`) and added a prompt rule: "If text is marked [UNREADABLE], do not guess; say which clause could not be read." Asked about clause 7.2 (twice), the rent-free management fee, and the handover date.
- **Result:** 7.2 run 1: the model received the [UNREADABLE] marker but still invented "re-let the property" and a quote that is not in the source, then said the key point was "clearly stated". 7.2 run 2: retrieval returned a heading-only chunk instead of section 7, so the model said 7.2 did not exist. Management fee: correct, quoted surviving text from 3.2. Handover date: both dates found and the conflict flagged (the new rule did not break normal answers).
- **Learned:** A prompt rule is a request, not a guarantee. Leftover fragments next to the marker ("...compensationfor such termination") gave the model enough to fill the gap. Docling Markdown also creates tiny heading-only chunks that can outrank the real clause.
- **Next:** (1) Mark the whole sentence as unreadable, not just the garbled span. (2) Add a filter that appends a warning whenever a retrieved chunk contains [UNREADABLE], whatever the model says. (3) Keep headings attached to their body text when chunking.

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
