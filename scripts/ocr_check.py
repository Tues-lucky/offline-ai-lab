"""
OCR quality check for Docling Markdown output.

Finds garbled OCR spans, replaces them with an [UNREADABLE: ...] marker so the
model has nothing to "fill in", and writes a review list a person can complete.

Usage:
    python3 ocr_check.py input.md            # mark the whole sentence (default, safer)
    python3 ocr_check.py input.md --span     # mark only the garbled words

Outputs (next to the input):
    input_checked.md   garbled spans replaced with [UNREADABLE: ...]
    input_review.csv   one row per span, with an empty column for the correct text
"""
import csv
import re
import sys
from pathlib import Path

# Short English words that are common in contracts. Short words in this set are
# treated as normal text, not OCR noise.
COMMON_SHORT = {
    "a", "an", "the", "of", "to", "in", "on", "by", "or", "and", "any", "for",
    "is", "be", "at", "as", "it", "its", "if", "no", "not", "may", "per", "all",
    "are", "has", "had", "was", "who", "use", "out", "but", "set", "two", "one",
    "six", "ten", "day", "due", "pay", "act", "law", "hk", "ltd", "inc", "sum",
    "new", "own", "end", "off", "up", "so", "do", "we", "our", "you", "can",
}

CLAUSE_RE = re.compile(r"^\s*(?:[-*]|\d+\.)?\s*(\d{1,2})\.(\d{1,2})")  # "7.2" at line start
HEADING_RE = re.compile(r"^#+\s*(\d{1,2})\.")                         # "## 7. EARLY ..."
LIST_RE = re.compile(r"^\s*(?:[-*]|\d+\.)\s")                          # "- " or "2. "

MIN_JUNK = 4   # this many suspicious words close together = one garbled span
MAX_GAP = 2    # allow up to this many normal words between suspicious ones

PREFIX_RE = re.compile(r"^(?:[-*]|\d+\.|\d+\.\d+\.?)$")           # "-", "2.", "7.2" before the text
NUMBER_RE = re.compile(r"^\(?\d+(?:\.\d+)*\.?\)?$")                 # "7.2", "(6)", "10.1."
ABBREVIATIONS = {"cap.", "no.", "ltd.", "co.", "inc.", "e.g.", "i.e.", "hk$"}


def is_junk(word: str) -> bool:
    """Return True if a single word looks like OCR noise."""
    w = word.strip(".,;:()\"'").lower()
    if not w.isalpha():                 # digits or symbols: don't judge
        return False
    if w in COMMON_SHORT:
        return False
    if len(w) <= 3:                     # uncommon 1-3 letter word: suspicious
        return True
    if not re.search(r"[aeiouy]", w):   # no vowels: suspicious
        return True
    return False


def find_junk_groups(words):
    """Return (start, end) index ranges where suspicious words cluster."""
    junk_idx = [i for i, w in enumerate(words) if is_junk(w)]
    groups, current = [], []
    for i in junk_idx:
        if current and i - current[-1] - 1 > MAX_GAP:
            groups.append(current)
            current = []
        current.append(i)
    if current:
        groups.append(current)
    return [(g[0], g[-1] + 1) for g in groups if len(g) >= MIN_JUNK]


def ends_sentence(token: str) -> bool:
    """True if this word ends a sentence ("termination." but not "7.2" or "Cap.")."""
    if not token.rstrip('"\')').endswith("."):
        return False
    if NUMBER_RE.match(token) or token.lower() in ABBREVIATIONS:
        return False
    return True


def widen_to_sentence(words, start, end):
    """Grow a garbled span to cover its whole sentence, keeping any clause number prefix."""
    prefix = 0
    while prefix < len(words) and PREFIX_RE.match(words[prefix]):
        prefix += 1
    s = start
    while s > prefix and not ends_sentence(words[s - 1]) and words[s - 1] != "|":
        s -= 1
    e = end
    while e < len(words) and not ends_sentence(words[e - 1]) and words[e] != "|":
        e += 1   # "|" is a table cell border: stay inside the cell
    return s, min(e, len(words))


def merge(ranges):
    """Merge overlapping (start, end) ranges."""
    merged = []
    for s, e in sorted(ranges):
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    return merged


def main(path: str, sentence_mode: bool = True):
    src = Path(path)
    lines = src.read_text(encoding="utf-8").splitlines()

    section, major, last_minor = "", None, 0
    out_lines, review = [], []

    for line_no, line in enumerate(lines, start=1):
        # 1) Headings tell us which clause group we are in
        if line.startswith("#"):
            section = line.lstrip("# ").strip()
            h = HEADING_RE.match(line)
            major, last_minor = (h.group(1), 0) if h else (None, 0)
            out_lines.append(line)
            continue

        # 2) Clause number: use it if visible, otherwise guess previous + 1
        m = CLAUSE_RE.match(line)
        if m:
            major, last_minor = m.group(1), int(m.group(2))
            label = f"{major}.{last_minor}"
        elif LIST_RE.match(line) and major:
            last_minor += 1
            label = f"{major}.{last_minor} (inferred)"
        elif line.startswith("|"):
            row_name = line.strip("|").split("|")[0].strip()
            label = f"{section} / {row_name}"
        else:
            label = f"{major}.{last_minor} (continued)" if major else section

        # 3) Find and mark garbled spans
        words = line.split()
        groups = find_junk_groups(words)
        if sentence_mode:
            groups = merge(widen_to_sentence(words, s, e) for s, e in groups)
        for start, end in reversed(groups):   # replace from the end so indexes stay valid
            review.append({
                "line": line_no,
                "where": label,
                "ocr_text": " ".join(words[start:end]),
                "correct_text": "",            # filled in by a person
            })
            ending = "." if sentence_mode and words[end - 1].endswith(".") else ""
            words[start:end] = [f"[UNREADABLE: {label}, check original page]{ending}"]
        if groups:
            line = " ".join(words)

        out_lines.append(line)

    checked = src.with_name(src.stem + "_checked.md")
    checked.write_text("\n".join(out_lines) + "\n", encoding="utf-8")

    review.sort(key=lambda r: r["line"])
    review_csv = src.with_name(src.stem + "_review.csv")
    with review_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["line", "where", "ocr_text", "correct_text"])
        writer.writeheader()
        writer.writerows(review)

    print(f"Found {len(review)} garbled span(s).")
    for r in review:
        print(f"  line {r['line']:>3} | {r['where'][:34]:<34} | {r['ocr_text'][:45]}")
    print(f"\nSaved: {checked.name}, {review_csv.name}")


if __name__ == "__main__":
    main(sys.argv[1], sentence_mode="--span" not in sys.argv[2:])
