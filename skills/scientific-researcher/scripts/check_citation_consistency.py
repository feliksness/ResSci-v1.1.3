#!/usr/bin/env python3
"""
check_citation_consistency.py - audit a manuscript's in-text citations against
its reference list, offline.

Standard library only (Python 3.8+). Works on Markdown or plain text.

Checks
  * numeric styles ([1], [2-4], [1,3], <sup>1</sup>, ^1^): cited numbers missing
    from the reference list, references never cited, duplicate numbers,
    references not numbered in order of first citation (Vancouver/IEEE/AMA/Nature)
  * author-year styles ((Smith, 2020), (Smith & Lee, 2019; Wu et al., 2021a),
    Smith et al. (2020)): citations with no matching reference, references never cited
  * duplicate reference entries
  * leftover placeholders and unverified tags: [citation needed], (Author, Year),
    TODO, TBD, XXXX, [?], ??, [UNV], [UNVERIFIED ...] outside an "Unverified leads" section
  * references without a year; references without a DOI (informational)

It cannot judge whether a source supports a claim; that requires reading the source.

Resolving errors: find a supporting source, move the item to an "Unverified leads"
section, or disclose the gap. Never delete a marker such as [citation needed] or [UNV]
while keeping the unsupported claim, and never delete a valid reference just because the
script could not parse its in-text citation (check the format first).

Usage
  python3 check_citation_consistency.py draft.md
  python3 check_citation_consistency.py draft.md --style numeric
  python3 check_citation_consistency.py draft.md --export-refs refs.txt   # then: verify_citations.py --file refs.txt
  python3 check_citation_consistency.py draft.md --export-dois dois.txt

Exit status: 0 no errors; 1 errors found; 2 could not locate a reference section.
"""

import argparse
import re
import sys
import unicodedata

REF_HEADING_RE = re.compile(
    r"^\s*(#{1,6}\s*)?(\*\*)?\s*(\d{1,2}\.?\s+)?(references|reference list|bibliography|works cited|literature cited|sources)\s*(\*\*)?\s*:?\s*$",
    re.I)
UNVERIFIED_HEADING_RE = re.compile(r"^\s*(#{1,6}\s*)?(\*\*)?\s*(\d{1,2}\.?\s+)?unverified leads?\b.*$", re.I)
HEADING_RE = re.compile(r"^\s*#{1,6}\s+\S")
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"<>{}|\\^`\[\]]+", re.I)
YEAR_RE = re.compile(r"\b(1[6-9]\d{2}|20\d{2})([a-z])?\b")

NUMERIC_BRACKET_RE = re.compile(r"\[(\d{1,3}(?:\s*[-–—,]\s*\d{1,3})*)\]")  # also matches linked [1](#r1)
SUPERSCRIPT_DIGITS = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")
UNICODE_SUP_RE = re.compile(r"(?<=[A-Za-z\.,;:)\]’'\"])([⁰¹²³⁴⁵⁶⁷⁸⁹]+(?:[,⁻–-][⁰¹²³⁴⁵⁶⁷⁸⁹]+)*)")
NUMERIC_SUP_RE = re.compile(r"<sup>\s*(\d{1,3}(?:\s*[-–—,]\s*\d{1,3})*)\s*</sup>|\^(\d{1,3}(?:\s*[-–—,]\s*\d{1,3})*)\^")
PAREN_RE = re.compile(r"\(([^()]*?\b(?:1[6-9]\d{2}|20\d{2})[a-z]?[^()]*?)\)")
NARRATIVE_RE = re.compile(
    r"\b([A-Z][A-Za-z'’\-]+(?:\s+(?:van|von|de|der|den|da|di|le|la)\s+[A-Z][A-Za-z'’\-]+)?)"
    r"(?:\s+(?:et al\.?|and colleagues|(?:and|&)\s+[A-Z][A-Za-z'’\-]+))?\s*\((\d{4}[a-z]?)(?:[,;][^()]*)?\)")

NON_NAMES = set("""table tables figure figures fig appendix supplementary supplement section eq equation in the
since from between during until before after year years spring summer autumn fall winter version phase wave
cohort data accessed retrieved updated published january february march april may june july august september
october november december jan feb mar apr jun jul aug sep sept oct nov dec circa ca about approximately
see also e.g i.e cf and or of on at by for to n vol volume issue chapter part page pages""".split())

PLACEHOLDER_RES = [
    (re.compile(r"\[citation needed[^\]]*\]", re.I), "citation-needed marker"),
    (re.compile(r"\[(?:ref|refs|cite|citation|source)\??\]", re.I), "empty citation marker"),
    (re.compile(r"\(\s*Author\s*,?\s*(?:Year|\d{4})\s*\)", re.I), "template citation (Author, Year)"),
    (re.compile(r"\bXXXX?\b"), "XXX placeholder"),
    (re.compile(r"\bTODO\b"), "TODO"),
    (re.compile(r"\bTBD\b"), "TBD"),
    (re.compile(r"\[\?\]"), "[?] marker"),
    (re.compile(r"\?\?"), "?? marker"),
    (re.compile(r"\[UNV\]"), "[UNV] tag (unverified)"),
    (re.compile(r"\[UNVERIFIED[^\]]*\]", re.I), "[UNVERIFIED] tag"),
]


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", strip_accents(s).lower()).strip()


def expand_numbers(spec):
    out = []
    for part in re.split(r"\s*,\s*", spec):
        m = re.match(r"^(\d+)\s*[-–—]\s*(\d+)$", part.strip())
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            if a <= b and b - a < 200:
                out.extend(range(a, b + 1))
        elif part.strip().isdigit():
            out.append(int(part.strip()))
    return out


def split_sections(text):
    """Return (body, references, unverified_section, ref_heading_line)."""
    lines = text.splitlines()
    ref_idx = None
    for i, ln in enumerate(lines):
        if REF_HEADING_RE.match(ln):
            ref_idx = i  # last match wins
    if ref_idx is None:
        return text, None, "", None
    end = len(lines)
    for j in range(ref_idx + 1, len(lines)):
        if HEADING_RE.match(lines[j]) or UNVERIFIED_HEADING_RE.match(lines[j]):
            end = j
            break
    body = "\n".join(lines[:ref_idx])
    refs = "\n".join(lines[ref_idx + 1:end])
    tail = "\n".join(lines[end:])
    unverified = ""
    tail_lines = tail.splitlines()
    for k, ln in enumerate(tail_lines):
        if UNVERIFIED_HEADING_RE.match(ln):
            stop = len(tail_lines)
            for m in range(k + 1, len(tail_lines)):
                if HEADING_RE.match(tail_lines[m]):
                    stop = m
                    break
            unverified = "\n".join(tail_lines[k:stop])
            tail = "\n".join(tail_lines[:k] + tail_lines[stop:])
            break
    # Text after the references (appendices) is checked as body text too
    return body + "\n" + tail, refs, unverified, ref_idx + 1


def parse_references(refs):
    """Return list of dicts: {num, text}."""
    entries = []
    current = None
    for ln in refs.splitlines():
        if not ln.strip():
            if current:
                entries.append(current)
                current = None
            continue
        m = re.match(r"^\s*(?:\[(\d{1,3})\]|(\d{1,3})[.)])\s+(.*)$", ln)
        b = re.match(r"^\s*[-*•]\s+(.*)$", ln)
        if m:
            if current:
                entries.append(current)
            current = {"num": int(m.group(1) or m.group(2)), "text": m.group(3).strip()}
        elif b:
            if current:
                entries.append(current)
            current = {"num": None, "text": b.group(1).strip()}
        elif current and (ln.startswith((" ", "\t"))):
            current["text"] += " " + ln.strip()
        else:
            if current:
                entries.append(current)
            current = {"num": None, "text": ln.strip()}
    if current:
        entries.append(current)
    return [e for e in entries if e["text"]]


def detect_style(body):
    n_num = (len(NUMERIC_BRACKET_RE.findall(body)) + len(NUMERIC_SUP_RE.findall(body))
             + len(UNICODE_SUP_RE.findall(body)))
    n_ay = len(PAREN_RE.findall(body)) + len(NARRATIVE_RE.findall(body))
    return "numeric" if n_num >= n_ay and n_num > 0 else "author-year"


def numeric_citations(body, notes=None):
    order = []
    for m in re.finditer(NUMERIC_BRACKET_RE.pattern + "|" + NUMERIC_SUP_RE.pattern, body):
        spec = next(g for g in m.groups() if g)
        order.extend(expand_numbers(spec))
    if not order:
        # Fall back to Unicode superscripts (AMA/Nature style pasted from word processors)
        for m in UNICODE_SUP_RE.finditer(body):
            order.extend(expand_numbers(m.group(1).translate(SUPERSCRIPT_DIGITS)))
        if order and notes is not None:
            notes.append("citations read from Unicode superscripts; check that units or exponents "
                         "(e.g. m², 10⁶) were not counted as citations")
    return order


def author_year_citations(body):
    cites = []
    for m in PAREN_RE.finditer(body):
        inner = m.group(1)
        for part in re.split(r";", inner):
            part = re.sub(r"^\s*(?:e\.g\.,?|see(?: also)?|cf\.|i\.e\.,?)\s+", "", part.strip(), flags=re.I)
            ym = YEAR_RE.search(part)
            if not ym:
                continue
            name_part = part[:ym.start()]
            nm = re.match(r"\s*([A-Z][a-z][A-Za-z'’\-]*(?:\s+(?:van|von|de|der|den|da|di|le|la)\s+[A-Z][A-Za-z'’\-]+)?)", name_part)
            if not nm:
                # organisational authors / acronyms need a comma before the year, e.g. "(WHO, 2021)"
                nm = re.match(r"\s*([A-Z][A-Z0-9&\-]{1,})\s*,\s*$", name_part)
            if nm and nm.group(1).lower() not in NON_NAMES:
                cites.append((nm.group(1), ym.group(1) + (ym.group(2) or "")))
    for m in NARRATIVE_RE.finditer(body):
        name = m.group(1)
        if name.lower() in NON_NAMES:
            continue
        cites.append((name, m.group(2)))
    return cites


def ref_key(entry_text):
    t = entry_text.strip()
    first = re.match(r"^\s*([^,.(]+)", t)
    surname = first.group(1).strip() if first else ""
    ym = re.search(r"\((1[6-9]\d{2}|20\d{2})([a-z])?\)", t) or YEAR_RE.search(t)
    year = (ym.group(1) + (ym.group(2) or "")) if ym else None
    return surname, year


def matches(cite, entry_text):
    name, year = cite
    surname, ryear = ref_key(entry_text)
    head = norm(entry_text[:80])
    name_ok = bool(norm(name)) and (norm(name).split()[-1] in head.split()[:6] or head.startswith(norm(name)))
    if not name_ok and name.isupper() and len(name) >= 2:
        # organisational acronym, e.g. WHO -> "World Health Organization"
        words = [w for w in re.split(r"[\s\-]+", re.sub(r"[^A-Za-z\s\-]", " ", entry_text[:120]))
                 if w and w.lower() not in {"of", "and", "for", "the", "on", "in", "de", "du"}]
        initials = "".join(w[0].upper() for w in words[:len(name) + 2])
        name_ok = initials.startswith(name) or ("[" + name + "]") in entry_text[:120]
    if not name_ok:
        return False
    if ryear is None:
        return False
    if year == ryear:
        return True
    # tolerate missing suffix on one side (2020 vs 2020a)
    return year[:4] == ryear[:4] and (len(year) == 4 or len(ryear) == 4)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--style", choices=["auto", "numeric", "author-year"], default="auto")
    ap.add_argument("--export-dois", metavar="PATH", help="write DOIs found in the reference list to this file")
    ap.add_argument("--export-refs", metavar="PATH",
                    help="write the full reference entries, one per line, for verify_citations.py --file "
                         "(preferred: lets the verifier compare titles, authors and years)")
    args = ap.parse_args(argv)

    text = open(args.file, encoding="utf-8").read()
    body, refs, unverified, ref_line = split_sections(text)
    errors, warnings, info = [], [], []

    # Placeholders and unverified tags (anywhere except the Unverified leads section)
    checked_text = body + "\n" + (refs or "")
    for rx, label in PLACEHOLDER_RES:
        for m in rx.finditer(checked_text):
            line_no = checked_text[:m.start()].count("\n") + 1
            snippet = checked_text[max(0, m.start() - 30):m.end() + 30].replace("\n", " ")
            errors.append(f"placeholder/unverified marker ({label}) near: ...{snippet}...")
            if len(errors) > 200:
                break

    if refs is None:
        print("# Citation consistency report\n")
        print("Could not find a reference section (heading such as 'References' or 'Bibliography').")
        for e in errors:
            print(f"- ERROR: {e}")
        return 2

    entries = parse_references(refs)
    style = args.style if args.style != "auto" else detect_style(body)
    info.append(f"style: {style}; references parsed: {len(entries)} (section starts at line {ref_line})")

    # Duplicates in reference list
    seen = {}
    for i, e in enumerate(entries):
        k = norm(re.sub(DOI_RE, "", e["text"]))[:120]
        if k in seen:
            warnings.append(f"possible duplicate references: #{seen[k] + 1} and #{i + 1}: {e['text'][:80]}")
        else:
            seen[k] = i
    dois = {}
    for i, e in enumerate(entries):
        for d in DOI_RE.findall(e["text"]):
            d = d.rstrip(".,;)").lower()
            if d in dois:
                warnings.append(f"same DOI in two references (#{dois[d] + 1} and #{i + 1}): {d}")
            dois.setdefault(d, i)

    for i, e in enumerate(entries):
        label = f"#{e['num']}" if e["num"] is not None else f"entry {i + 1}"
        if not YEAR_RE.search(e["text"]) and not re.search(r"\bn\.d\.", e["text"]):
            warnings.append(f"reference {label} has no year: {e['text'][:80]}")
        if not DOI_RE.search(e["text"]) and not re.search(r"https?://|ISBN|arXiv", e["text"], re.I):
            info.append(f"reference {label} has no DOI/URL/ISBN (fine for some sources): {e['text'][:70]}")

    if style == "numeric":
        cited = numeric_citations(body, warnings)
        nums = [e["num"] for e in entries if e["num"] is not None]
        if not nums:
            errors.append("numeric citations used but the reference list is not numbered")
        numset = set(nums)
        for n in sorted(set(cited)):
            if n not in numset:
                errors.append(f"in-text citation [{n}] has no matching reference")
        for n in nums:
            if n not in set(cited):
                errors.append(f"reference [{n}] is never cited in the text")
        dup = sorted({n for n in nums if nums.count(n) > 1})
        for n in dup:
            errors.append(f"reference number {n} appears more than once in the list")
        if nums and nums != list(range(1, len(nums) + 1)):
            warnings.append("reference numbers are not consecutive starting at 1")
        first_seen = []
        for n in cited:
            if n not in first_seen:
                first_seen.append(n)
        if first_seen and first_seen != sorted(first_seen):
            warnings.append("references are not numbered in order of first citation "
                            "(required by Vancouver, IEEE, AMA, Nature styles): first-citation order "
                            + ", ".join(map(str, first_seen[:20])) + ("..." if len(first_seen) > 20 else ""))
    else:
        cites = author_year_citations(body)
        if not cites:
            warnings.append("no author-year citations detected in the text")
        cited_entries = set()
        for c in sorted(set(cites)):
            hits = [i for i, e in enumerate(entries) if matches(c, e["text"])]
            if not hits:
                errors.append(f"in-text citation ({c[0]}, {c[1]}) has no matching reference")
            elif len(hits) > 1:
                warnings.append(f"citation ({c[0]}, {c[1]}) matches several references "
                                f"({', '.join('#' + str(h + 1) for h in hits)}); add a/b suffixes")
            cited_entries.update(hits)
        for i, e in enumerate(entries):
            if i not in cited_entries:
                errors.append(f"reference entry {i + 1} appears never cited: {e['text'][:80]}")

    if args.export_refs:
        with open(args.export_refs, "w", encoding="utf-8") as fh:
            for e in entries:
                fh.write(re.sub(r"\s+", " ", e["text"]).strip() + "\n")
        info.append(f"wrote {len(entries)} reference entries to {args.export_refs}")

    if args.export_dois:
        with open(args.export_dois, "w", encoding="utf-8") as fh:
            for d in dois:
                fh.write(d + "\n")
        info.append(f"wrote {len(dois)} DOIs to {args.export_dois}")

    print("# Citation consistency report\n")
    for i in info[:1]:
        print(i + "\n")
    print(f"Errors: {len(errors)}   Warnings: {len(warnings)}\n")
    for e in errors:
        print(f"- ERROR: {e}")
    for w in warnings:
        print(f"- WARNING: {w}")
    extra = info[1:]
    if extra:
        print("\nInformation:")
        for i in extra[:50]:
            print(f"- {i}")
        if len(extra) > 50:
            print(f"- ... {len(extra) - 50} more")
    if unverified:
        n_unv = len([ln for ln in unverified.splitlines()[1:] if ln.strip()])
        print(f"\nUnverified leads section present ({n_unv} non-empty lines); tags there are expected.")
    print("\nNote: this checks form only. Whether each source supports its sentence must be checked by reading it.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
