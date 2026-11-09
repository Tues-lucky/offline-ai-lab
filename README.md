# offline-ai-lab

Daily experiments in running a useful AI assistant **fully offline**, on a single laptop, over private documents.

The test case is document Q&A on contracts: can a small local model find the right clause, quote it exactly, and admit when it cannot read something? Everything runs on a MacBook Air (M4, 32 GB) with no data leaving the machine.

See **[LOG.md](LOG.md)** for the daily notes.

## Stack

| Part | What it does |
| --- | --- |
| [Ollama](https://ollama.com) | Runs the models locally |
| Qwen 3.5 9B / Qwen 3.8 27B | Chat models (thinking on or off) |
| qwen3-embedding 0.6B | Embeddings for retrieval |
| [Open WebUI](https://github.com/open-webui/open-webui) (Docker) | Chat UI, knowledge base, retrieval, tool calling |
| [Docling Serve](https://github.com/docling-project/docling-serve) (Docker) | PDF/scan to Markdown, OCR, table recovery |

## Results so far

Contract Q&A test set (fictitious documents in [`test-docs/`](test-docs)):

| Set | What it tests | Score |
| --- | --- | --- |
| A (no documents) | General skill: email, translation, summary, date maths, made-up law, JSON | 9B: 10.5 / 14 |
| B (documents) | Extraction, comparison, risk spotting, conflicts inside one contract, drafting | 16.5 / 18 (92%) |

Main findings:

- Retrieval settings matter more than model size at first (Top K 3 → 8 fixed wrong answers).
- A fast model (thinking off) is fine for single-lookup questions; checking several places at once needs thinking on.
- **Document processing decides quality.** Flattening tables to one line per row let the fast model catch a date conflict in 7 s instead of 35 s.
- **Garbled OCR is dangerous.** Given half-readable text, the model invented a plausible clause and quoted it as if it were real. Garbled spans must be detected and marked before the model sees them ([`scripts/ocr_check.py`](scripts/ocr_check.py)).

## Repo layout

```
LOG.md          daily notes, newest first
scripts/        make_contracts.py (test documents), make_scan.py (fake scans), ocr_check.py (OCR quality check)
test-docs/      fictitious contracts (+ FLAT and SCAN variants), answer key
experiments/    inputs and outputs of individual experiments
```

## Notes

- All documents here are **fictitious** and generated for testing. They are not legal advice and do not describe real parties.
- The answer key is in `test-docs/answer-key/`. Do not put it in the knowledge base you are testing.
- Personal learning project.
