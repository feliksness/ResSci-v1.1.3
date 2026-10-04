#!/usr/bin/env python3
"""
verify_citations.py - check that cited works exist, match their citations, and
have not been retracted, corrected, or flagged.

Standard library only (Python 3.8+). Needs internet access to public APIs:
  - Crossref REST API   (DOIs; retraction/correction notices incl. Retraction Watch data)
  - NCBI E-utilities    (PubMed records; "Retracted Publication", "Retraction in", "Erratum in")
  - OpenAlex            (is_retracted flag; optional second opinion)
  - arXiv export API    (arXiv identifiers; journal reference if published)

What it checks
  * existence of each DOI / PMID / arXiv ID (and, for reference strings without an
    identifier, a bibliographic search for the closest match);
  * whether the retrieved title, first author and year agree with the reference text;
  * retraction, withdrawal, expression of concern, correction, and preprint status.

What it cannot check
  * whether the source supports the sentence it is cited for - that requires reading it.
  * a network failure is reported as UNCHECKED, which means "not verified", never
    "does not exist".

Usage examples
  python3 verify_citations.py --doi 10.1016/S0140-6736(97)11096-0 --pmid 9500320
  python3 verify_citations.py --file references.txt --email you@example.org
  python3 verify_citations.py --file dois.txt --json > report.json

Input file: one reference per line, or references separated by blank lines.
DOIs, PMIDs ("PMID: 123"), and arXiv IDs ("arXiv:2101.00001") are extracted
automatically. Lines without identifiers are matched by bibliographic search.

Optional politeness/identification (never hard-code secrets):
  --email or env CROSSREF_MAILTO / NCBI_EMAIL   contact email for API etiquette
  env NCBI_API_KEY                               raises NCBI rate limits
  env OPENALEX_API_KEY                           used if OpenAlex requires/accepts a key

Statuses (most severe first): RETRACTED, PARTIALLY_RETRACTED, EXPRESSION_OF_CONCERN,
MISMATCH (identifier resolves to a different title/author/year), NOT_FOUND (the DOI
registration agency or PubMed/arXiv says it does not exist), NO_CONFIDENT_MATCH,
PROBABLE_MATCH (search match needing manual confirmation), UNCHECKED (service
unreachable: NOT verified, NOT evidence of non-existence), REGISTERED_ELSEWHERE (DOI
exists with a non-Crossref agency; metadata not compared), CORRECTED, PREPRINT, OK.

Exit status: 0 all OK/CORRECTED/PREPRINT; 1 at least one problem; 2 no problems but at
least one item needs a manual check.
"""

import argparse
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

VERSION = "1.0"
CROSSREF = "https://api.crossref.org/works"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
OPENALEX = "https://api.openalex.org/works"
ARXIV = "https://export.arxiv.org/api/query"
DOI_RA = "https://doi.org/ra"
DATACITE = "https://api.datacite.org/dois"

SEVERITY = [
    "RETRACTED", "PARTIALLY_RETRACTED", "EXPRESSION_OF_CONCERN", "MISMATCH", "NOT_FOUND",
    "NO_CONFIDENT_MATCH", "PROBABLE_MATCH", "UNCHECKED", "REGISTERED_ELSEWHERE",
    "CORRECTED", "PREPRINT", "OK",
]
# Problems: the reference must be fixed, replaced, or removed (or the status disclosed).
PROBLEM = {"RETRACTED", "PARTIALLY_RETRACTED", "EXPRESSION_OF_CONCERN", "MISMATCH", "NOT_FOUND",
           "NO_CONFIDENT_MATCH"}
# Needs a manual check before it can be treated as verified.
MANUAL = {"PROBABLE_MATCH", "UNCHECKED", "REGISTERED_ELSEWHERE"}

STOPWORDS = set("""a an and are as at be by for from in into is it its of on or that the
their this to was were with without via vs versus using use study analysis effect effects""".split())


class NotFound(Exception):
    pass


class Unreachable(Exception):
    pass


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

class Http:
    def __init__(self, email=None, timeout=20, sleep=0.34):
        self.email = email
        self.timeout = timeout
        self.sleep = sleep
        self._last = 0.0

    def user_agent(self):
        ua = f"scientific-researcher-skill/{VERSION} (citation verification)"
        if self.email:
            ua += f" mailto:{self.email}"
        return ua

    def get(self, url, params=None, accept="application/json"):
        """Return response body (str). Raises NotFound on 404, Unreachable otherwise."""
        if params:
            url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
        wait = self.sleep - (time.time() - self._last)
        if wait > 0:
            time.sleep(wait)
        req = urllib.request.Request(url, headers={"User-Agent": self.user_agent(), "Accept": accept})
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    self._last = time.time()
                    return resp.read().decode("utf-8", errors="replace")
            except urllib.error.HTTPError as e:
                self._last = time.time()
                if e.code == 404:
                    raise NotFound(url)
                if e.code in (429, 500, 502, 503, 504) and attempt < 2:
                    time.sleep(2 * (attempt + 1))
                    continue
                raise Unreachable(f"HTTP {e.code} for {url}")
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                self._last = time.time()
                if attempt < 1:
                    time.sleep(1.5)
                    continue
                raise Unreachable(f"{type(e).__name__}: {e}")
        raise Unreachable(url)

    def get_json(self, url, params=None):
        body = self.get(url, params)
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            raise Unreachable(f"non-JSON response from {url}")


# ---------------------------------------------------------------------------
# Text utilities
# ---------------------------------------------------------------------------

DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"{}|\\^`\[\]]+", re.I)
PMID_RE = re.compile(r"\bPMID:?\s*(\d{1,9})\b", re.I)
_ARXIV_ID = r"(\d{4}\.\d{4,5}|[a-z][a-z\-]+(?:\.[A-Z]{2})?/\d{7})"
ARXIV_RE = re.compile(r"\barXiv:\s*" + _ARXIV_ID + r"(v\d+)?", re.I)
ARXIV_URL_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/" + _ARXIV_ID + r"(v\d+)?", re.I)
YEAR_RE = re.compile(r"\b(1[6-9]\d{2}|20\d{2})\b")


def clean_doi(doi):
    doi = doi.strip()
    doi = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", doi, flags=re.I)
    doi = doi.rstrip(".,;:'\"")
    # strip unbalanced closing parentheses/brackets picked up from surrounding text
    while doi.endswith(")") and doi.count("(") < doi.count(")"):
        doi = doi[:-1]
    while doi.endswith("]") and doi.count("[") < doi.count("]"):
        doi = doi[:-1]
    while doi.endswith(">") and doi.count("<") < doi.count(">"):
        doi = doi[:-1]
    return doi.rstrip(".,;:").lower()


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def tokens(s):
    s = strip_accents(s or "").lower()
    s = re.sub(r"<[^>]+>", " ", s)  # JATS/HTML tags in titles
    return [t for t in re.findall(r"[a-z0-9]+", s) if t not in STOPWORDS and len(t) > 1]


def title_coverage(title, text):
    """Share of the title's content words that appear in the reference text."""
    tt = tokens(title)
    if not tt:
        return None
    tx = set(tokens(text))
    return sum(1 for t in tt if t in tx) / len(tt)


def similarity(a, b):
    """Symmetric token-overlap (Dice) similarity."""
    ta, tb = set(tokens(a)), set(tokens(b))
    if not ta or not tb:
        return 0.0
    return 2 * len(ta & tb) / (len(ta) + len(tb))


def residual_text(entry):
    """Reference text with identifiers and URLs removed (to see if there is anything to compare)."""
    t = DOI_RE.sub(" ", entry)
    t = re.sub(r"https?://\S+", " ", t)
    t = PMID_RE.sub(" ", t)
    t = ARXIV_RE.sub(" ", t)
    t = re.sub(r"\bdoi:?", " ", t, flags=re.I)
    return t


LIST_MARKER_RE = re.compile(r"^\s*(\[\d{1,3}\]|\d{1,3}[.)]|[-*\u2022])\s+")
HEADING_LINE_RE = re.compile(
    r"^\s*(#{1,6}\s+.*|(\d+\.?\s*)?(\*\*)?(references|reference list|bibliography|works cited|"
    r"literature cited|sources|unverified leads?)(\*\*)?\s*:?)\s*$", re.I)


def _looks_like_reference_line(line):
    return bool(DOI_RE.search(line) or PMID_RE.search(line) or ARXIV_RE.search(line)
                or ARXIV_URL_RE.search(line) or YEAR_RE.search(line))


def split_entries(text):
    """Split a reference list into entries.

    Handles: numbered or bulleted lists (continuation lines are joined), one reference
    per line, references separated by blank lines (wrapped lines are joined), and
    files of bare identifiers. Heading lines ("References", "## 6. References") are skipped.
    """
    lines = [ln.rstrip() for ln in text.splitlines()]
    lines = [ln for ln in lines if not HEADING_LINE_RE.match(ln)]
    has_markers = any(LIST_MARKER_RE.match(ln) for ln in lines if ln.strip())
    entries = []
    if has_markers:
        current = None
        for ln in lines:
            if not ln.strip():
                if current:
                    entries.append(current)
                current = None
            elif LIST_MARKER_RE.match(ln):
                if current:
                    entries.append(current)
                current = LIST_MARKER_RE.sub("", ln, count=1)
            elif current is not None:
                current += " " + ln.strip()
            else:
                current = ln.strip()
        if current:
            entries.append(current)
    else:
        blocks, block = [], []
        for ln in lines:
            if ln.strip():
                block.append(ln.strip())
            elif block:
                blocks.append(block)
                block = []
        if block:
            blocks.append(block)
        for b in blocks:
            # A block whose lines each look like a complete reference (identifier or year on
            # every line, or more than one identifier in the block) is one-reference-per-line.
            n_ids = sum(len(DOI_RE.findall(ln)) + len(PMID_RE.findall(ln)) for ln in b)
            if len(b) > 1 and (n_ids > 1 or all(_looks_like_reference_line(ln) for ln in b)):
                entries.extend(b)
            else:
                entries.append(" ".join(b))
    return [re.sub(r"\s+", " ", e).strip() for e in entries if e.strip()]


# ---------------------------------------------------------------------------
# Lookups
# ---------------------------------------------------------------------------

def classify_update(kind):
    k = (kind or "").lower().replace("-", "_").replace(" ", "_")
    if "partial" in k and "retract" in k:
        return "PARTIALLY_RETRACTED"
    if "retract" in k or "withdraw" in k or k == "removal":
        return "RETRACTED"
    if "concern" in k:
        return "EXPRESSION_OF_CONCERN"
    if k in ("correction", "corrigendum", "erratum", "addendum", "clarification"):
        return "CORRECTED"
    return None


def crossref_record(http, doi):
    data = http.get_json(f"{CROSSREF}/{urllib.parse.quote(doi, safe='/()')}")
    m = data.get("message", {})
    issued = (m.get("issued") or m.get("published-print") or m.get("published-online") or {}).get("date-parts", [[None]])
    year = issued[0][0] if issued and issued[0] else None
    authors = [a.get("family") or a.get("name") or "" for a in m.get("author", [])]
    rec = {
        "source": "crossref",
        "doi": (m.get("DOI") or doi).lower(),
        "title": " ".join(m.get("title") or []).strip(),
        "authors": authors,
        "year": year,
        "venue": " ".join(m.get("container-title") or []).strip(),
        "volume": m.get("volume"),
        "issue": m.get("issue"),
        "page": m.get("page") or m.get("article-number"),
        "type": m.get("type"),
        "subtype": m.get("subtype"),
        "flags": [],
        "notes": [],
    }
    for u in m.get("updated-by", []) or []:
        cls = classify_update(u.get("type"))
        if cls:
            date = (u.get("updated") or {}).get("date-parts", [[None]])[0][0]
            rec["flags"].append(cls)
            rec["notes"].append(f"{u.get('label') or u.get('type')} notice {u.get('DOI', '')} "
                                f"({date or 'date n/a'}, via {u.get('source', 'crossref')})")
    for u in m.get("update-to", []) or []:
        rec["notes"].append(f"this DOI is itself a {u.get('label') or u.get('type')} notice for {u.get('DOI')}")
    rel = m.get("relation") or {}
    if m.get("type") == "posted-content" or m.get("subtype") == "preprint":
        rec["flags"].append("PREPRINT")
        for r in rel.get("is-preprint-of", []) or []:
            rec["notes"].append(f"preprint later published as {r.get('id')}")
    for r in rel.get("has-preprint", []) or []:
        rec["notes"].append(f"has preprint {r.get('id')}")
    if rec["title"].lower().startswith(("retracted", "withdrawn")):
        rec["flags"].append("RETRACTED")
        rec["notes"].append("title carries a RETRACTED/WITHDRAWN prefix")
    return rec


def doi_registration_agency(http, doi):
    """Return the DOI's registration agency name, or None if the DOI does not exist."""
    data = http.get_json(f"{DOI_RA}/{urllib.parse.quote(doi, safe='/()')}")
    entry = data[0] if isinstance(data, list) and data else {}
    if entry.get("RA"):
        return entry["RA"]
    if "not exist" in (entry.get("status") or "").lower() or "invalid" in (entry.get("status") or "").lower():
        return None
    raise Unreachable(f"unexpected doi.org/ra response: {str(data)[:120]}")


def datacite_record(http, doi):
    data = http.get_json(f"{DATACITE}/{urllib.parse.quote(doi, safe='/()')}")
    a = (data.get("data") or {}).get("attributes") or {}
    titles = a.get("titles") or [{}]
    authors = [c.get("familyName") or c.get("name") or "" for c in a.get("creators") or []]
    rtype = ((a.get("types") or {}).get("resourceTypeGeneral") or "").lower()
    rec = {
        "source": "datacite",
        "doi": (a.get("doi") or doi).lower(),
        "title": (titles[0].get("title") or "").strip(),
        "authors": authors,
        "year": a.get("publicationYear"),
        "venue": a.get("publisher") if isinstance(a.get("publisher"), str) else (a.get("publisher") or {}).get("name"),
        "type": rtype or None,
        "flags": [],
        "notes": ["DataCite record (dataset, software, repository item, or preprint); "
                  "retraction status is not available from DataCite"],
    }
    if rtype == "preprint":
        rec["flags"].append("PREPRINT")
    return rec


def crossref_search(http, text, rows=3):
    params = {"query.bibliographic": text[:300], "rows": rows,
              "select": "DOI,title,author,issued,container-title,type"}
    if http.email:
        params["mailto"] = http.email
    data = http.get_json(CROSSREF, params)
    items = data.get("message", {}).get("items", [])
    out = []
    for it in items:
        issued = (it.get("issued") or {}).get("date-parts", [[None]])
        out.append({
            "doi": (it.get("DOI") or "").lower(),
            "title": " ".join(it.get("title") or []),
            "authors": [a.get("family") or a.get("name") or "" for a in it.get("author", [])],
            "year": issued[0][0] if issued and issued[0] else None,
            "venue": " ".join(it.get("container-title") or []),
        })
    return out


def _ncbi_params(extra):
    p = {"tool": "scientific-researcher-skill"}
    email = os.environ.get("NCBI_EMAIL") or os.environ.get("CROSSREF_MAILTO")
    if email:
        p["email"] = email
    key = os.environ.get("NCBI_API_KEY")
    if key:
        p["api_key"] = key
    p.update(extra)
    return p


def pubmed_record(http, pmid):
    data = http.get_json(f"{EUTILS}/esummary.fcgi", _ncbi_params({"db": "pubmed", "id": pmid, "retmode": "json"}))
    res = data.get("result", {})
    r = res.get(str(pmid))
    if not r or "error" in r:
        raise NotFound(f"PMID {pmid}")
    year_m = YEAR_RE.search(r.get("pubdate", "") or r.get("epubdate", ""))
    doi = next((a.get("value") for a in r.get("articleids", []) if a.get("idtype") == "doi"), None)
    rec = {
        "source": "pubmed",
        "pmid": str(pmid),
        "doi": doi.lower() if doi else None,
        "title": (r.get("title") or "").strip(),
        "authors": [a.get("name", "").split(" ")[0] for a in r.get("authors", []) if a.get("authtype", "Author") == "Author"],
        "year": int(year_m.group(1)) if year_m else None,
        "venue": r.get("fulljournalname") or r.get("source"),
        "volume": r.get("volume"),
        "issue": r.get("issue"),
        "page": r.get("pages"),
        "flags": [],
        "notes": [],
    }
    pubtypes = [p.lower() for p in r.get("pubtype", [])]
    if "retracted publication" in pubtypes:
        rec["flags"].append("RETRACTED")
        rec["notes"].append("PubMed publication type: Retracted Publication")
    if "retraction of publication" in pubtypes:
        rec["notes"].append("this PMID is itself a retraction notice")
    if "preprint" in pubtypes:
        rec["flags"].append("PREPRINT")
    for ref in r.get("references", []) or []:
        rt = (ref.get("reftype") or "").lower()
        label = f"PubMed: {ref.get('reftype')} PMID {ref.get('pmid')}"
        if rt.startswith("retraction in") or rt.startswith("retracted and republished in"):
            rec["flags"].append("RETRACTED")
            rec["notes"].append(label)
        elif rt.startswith("expression of concern in"):
            rec["flags"].append("EXPRESSION_OF_CONCERN")
            rec["notes"].append(label)
        elif rt.startswith(("erratum in", "corrected and republished in", "update in")):
            rec["flags"].append("CORRECTED")
            rec["notes"].append(label)
    return rec


def pubmed_pmid_for_doi(http, doi):
    data = http.get_json(f"{EUTILS}/esearch.fcgi",
                         _ncbi_params({"db": "pubmed", "term": f"\"{doi}\"[doi]", "retmode": "json"}))
    ids = data.get("esearchresult", {}).get("idlist", [])
    return ids[0] if len(ids) == 1 else None


def openalex_flags(http, doi):
    params = {}
    if http.email:
        params["mailto"] = http.email
    key = os.environ.get("OPENALEX_API_KEY")
    if key:
        params["api_key"] = key
    data = http.get_json(f"{OPENALEX}/doi:{urllib.parse.quote(doi, safe='/()')}", params or None)
    return bool(data.get("is_retracted"))


def arxiv_record(http, arxiv_id):
    body = http.get(ARXIV, {"id_list": arxiv_id}, accept="application/atom+xml")
    ns = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        raise Unreachable("unparseable arXiv response")
    entry = root.find("a:entry", ns)
    if entry is None or entry.find("a:title", ns) is None:
        raise NotFound(arxiv_id)
    eid = (entry.findtext("a:id", default="", namespaces=ns) or "")
    if "api/errors" in eid:
        raise NotFound(arxiv_id)
    published = entry.findtext("a:published", default="", namespaces=ns)
    year_m = YEAR_RE.search(published)
    rec = {
        "source": "arxiv",
        "arxiv": arxiv_id,
        "doi": (entry.findtext("arxiv:doi", default="", namespaces=ns) or "").lower() or None,
        "title": re.sub(r"\s+", " ", entry.findtext("a:title", default="", namespaces=ns)).strip(),
        "authors": [(a.findtext("a:name", default="", namespaces=ns) or "").split(" ")[-1]
                    for a in entry.findall("a:author", ns)],
        "year": int(year_m.group(1)) if year_m else None,
        "venue": "arXiv",
        "flags": ["PREPRINT"],
        "notes": [],
    }
    jref = entry.findtext("arxiv:journal_ref", default="", namespaces=ns)
    if jref:
        rec["notes"].append(f"journal reference: {jref.strip()}")
    if rec["doi"]:
        rec["notes"].append(f"published version DOI: {rec['doi']}")
    comment = entry.findtext("arxiv:comment", default="", namespaces=ns) or ""
    if re.search(r"withdrawn|retracted", comment, re.I):
        rec["flags"].append("RETRACTED")
        rec["notes"].append(f"arXiv comment: {comment.strip()[:120]}")
    return rec


# ---------------------------------------------------------------------------
# Verification of one item
# ---------------------------------------------------------------------------

def compare_to_text(rec, text, result):
    """Compare retrieved metadata with the reference text; add MISMATCH flags."""
    if len(tokens(residual_text(text))) < 4:
        result["notes"].append("no reference text to compare (identifier only); confirm title/authors manually")
        return
    cov = title_coverage(rec.get("title", ""), text)
    if cov is not None:
        result["title_match"] = round(cov, 2)
        if cov < 0.6:
            result["flags"].append("MISMATCH")
            result["notes"].append(f"retrieved title shares only {cov:.0%} of its words with the reference text")
    years_in_text = {int(y) for y in YEAR_RE.findall(residual_text(text))}
    if rec.get("year") and years_in_text and not any(abs(rec["year"] - y) <= 1 for y in years_in_text):
        result["flags"].append("MISMATCH")
        result["notes"].append(f"year in reference {sorted(years_in_text)} vs record {rec['year']}")
    elif rec.get("year") and years_in_text and rec["year"] not in years_in_text:
        result["notes"].append(f"year differs by one ({sorted(years_in_text)} vs {rec['year']}); "
                               "often online-first vs print year")
    if rec.get("authors"):
        first = strip_accents(rec["authors"][0]).lower().strip()
        if first and first not in strip_accents(text).lower():
            result["flags"].append("MISMATCH")
            result["notes"].append(f"first author '{rec['authors'][0]}' of the record does not appear in the "
                                   "reference text (check for transliteration or name-particle differences)")


def verify_item(http, item, use_pubmed=True, use_openalex=True):
    """item: dict with keys kind ('doi'|'pmid'|'arxiv'|'text'), value, text."""
    result = {"input": item["text"], "kind": item["kind"], "id": item["value"],
              "flags": [], "notes": [], "record": None}
    rec = None
    try:
        if item["kind"] == "doi":
            try:
                rec = crossref_record(http, item["value"])
            except NotFound:
                ra = doi_registration_agency(http, item["value"])  # may raise Unreachable
                if ra is None:
                    raise
                if ra.lower() == "datacite":
                    rec = datacite_record(http, item["value"])
                else:
                    result["flags"].append("REGISTERED_ELSEWHERE")
                    result["notes"].append(f"DOI exists (registration agency: {ra}) but is not in Crossref; "
                                           "compare title/authors/year manually on the landing page")
                    return finalize(result)
        elif item["kind"] == "pmid":
            rec = pubmed_record(http, item["value"])
        elif item["kind"] == "arxiv":
            rec = arxiv_record(http, item["value"])
        else:
            cands = crossref_search(http, item["text"])
            scored = sorted(((similarity(item["text"], " ".join([c["title"], " ".join(c["authors"][:3]),
                                                                    c["venue"], str(c["year"] or "")])), c)
                             for c in cands), key=lambda x: -x[0])
            best = scored[0][1] if scored else None
            cov = title_coverage(best["title"], item["text"]) if best else None
            if best is None or cov is None or cov < 0.75:
                result["flags"].append("NO_CONFIDENT_MATCH")
                if best:
                    result["notes"].append(f"closest Crossref match (not confirmed): '{best['title'][:90]}' "
                                           f"{best['year']} doi:{best['doi']}")
                result["notes"].append("search other indexes (PubMed, Google Scholar, publisher, library catalog) "
                                       "before concluding it does not exist; books and reports are often absent from Crossref")
                return finalize(result)
            # A search hit is only a candidate: require a substantive title, matching year and author.
            text_norm = strip_accents(item["text"]).lower()
            years_in_text = {int(y) for y in YEAR_RE.findall(item["text"])}
            year_ok = (not years_in_text) or (best["year"] is not None and any(abs(best["year"] - y) <= 1 for y in years_in_text))
            author_ok = bool(best["authors"]) and strip_accents(best["authors"][0]).lower() in text_norm
            long_title = len(tokens(best["title"])) >= 3
            rec = crossref_record(http, best["doi"])
            if not (cov >= 0.85 and year_ok and author_ok and long_title):
                result["flags"].append("PROBABLE_MATCH")
                why = []
                if cov < 0.85:
                    why.append(f"title overlap {cov:.0%}")
                if not year_ok:
                    why.append("year differs")
                if not author_ok:
                    why.append("first author not found in reference")
                if not long_title:
                    why.append("very short title")
                result["notes"].append(f"candidate doi:{best['doi']} needs manual confirmation ({'; '.join(why)})")
            else:
                result["notes"].append(f"matched by bibliographic search to doi:{best['doi']}")
    except NotFound:
        result["flags"].append("NOT_FOUND")
        where = {"doi": "DOI registration agencies (doi.org)", "pmid": "PubMed", "arxiv": "arXiv"}.get(item["kind"], "registry")
        result["notes"].append(f"{item['kind'].upper()} does not exist according to {where}")
        return finalize(result)
    except Unreachable as e:
        result["flags"].append("UNCHECKED")
        result["notes"].append(f"service unreachable ({e}); not verified")
        return finalize(result)

    result["record"] = {k: rec.get(k) for k in ("title", "authors", "year", "venue", "volume", "issue",
                                                  "page", "doi", "pmid", "arxiv", "type") if rec.get(k)}
    if result["record"].get("authors"):
        result["record"]["authors"] = result["record"]["authors"][:6]
    result["flags"].extend(rec["flags"])
    result["notes"].extend(rec["notes"])
    compare_to_text(rec, item["text"], result)

    doi = rec.get("doi")
    # Cross-check DOI-bearing records with PubMed and OpenAlex for retraction status
    if doi and use_pubmed and rec.get("source") != "pubmed":
        try:
            pmid = pubmed_pmid_for_doi(http, doi)
            if pmid:
                prec = pubmed_record(http, pmid)
                result["record"]["pmid"] = pmid
                result["flags"].extend(prec["flags"])
                result["notes"].extend(prec["notes"])
        except (NotFound, Unreachable) as e:
            result["notes"].append(f"PubMed cross-check not completed ({type(e).__name__})")
    elif rec.get("source") == "pubmed" and doi:
        try:
            crec = crossref_record(http, doi)
            result["flags"].extend(crec["flags"])
            result["notes"].extend(crec["notes"])
        except (NotFound, Unreachable) as e:
            result["notes"].append(f"Crossref cross-check not completed ({type(e).__name__})")
    if doi and use_openalex:
        try:
            if openalex_flags(http, doi):
                result["flags"].append("RETRACTED")
                result["notes"].append("OpenAlex: is_retracted = true")
        except (NotFound, Unreachable) as e:
            result["notes"].append(f"OpenAlex cross-check not completed ({type(e).__name__})")
    return finalize(result)


def finalize(result):
    flags = list(dict.fromkeys(result["flags"]))  # dedupe, keep order
    result["flags"] = flags
    result["notes"] = list(dict.fromkeys(n for n in result["notes"] if n))
    result["status"] = next((s for s in SEVERITY if s in flags), "OK")
    return result


# ---------------------------------------------------------------------------
# Input assembly and output
# ---------------------------------------------------------------------------

def items_from_entry(entry):
    found = []
    for m in DOI_RE.finditer(entry):
        found.append({"kind": "doi", "value": clean_doi(m.group(0)), "text": entry})
    for m in PMID_RE.finditer(entry):
        found.append({"kind": "pmid", "value": m.group(1), "text": entry})
    for rx in (ARXIV_RE, ARXIV_URL_RE):
        for m in rx.finditer(entry):
            found.append({"kind": "arxiv", "value": m.group(1), "text": entry})
    if not found:
        return [{"kind": "text", "value": None, "text": entry}]
    # Prefer one identifier per entry: DOI > PMID > arXiv (others are cross-checked)
    for kind in ("doi", "pmid", "arxiv"):
        sel = [f for f in found if f["kind"] == kind]
        if sel:
            return [sel[0]]
    return found[:1]


def render_markdown(results):
    lines = ["| # | Status | Input (truncated) | Retrieved title | Year | Venue | Notes |",
             "|---|---|---|---|---|---|---|"]
    for i, r in enumerate(results, 1):
        rec = r.get("record") or {}
        cell = lambda s: (s or "").replace("|", "/").replace("\n", " ")
        lines.append("| {} | **{}** | {} | {} | {} | {} | {} |".format(
            i, r["status"], cell(r["input"][:70]), cell((rec.get("title") or "")[:80]),
            rec.get("year") or "", cell((rec.get("venue") or "")[:40]), cell("; ".join(r["notes"]))))
    counts = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    lines.append("")
    lines.append("Summary: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items(), key=lambda kv: SEVERITY.index(kv[0]))))
    lines.append("")
    lines.append("Reminder: metadata checks confirm existence and identity only. Whether each source supports the "
                 "claim it is cited for must be checked by reading it. UNCHECKED means not verified.")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--doi", action="append", default=[], help="DOI to check (repeatable)")
    ap.add_argument("--pmid", action="append", default=[], help="PubMed ID to check (repeatable)")
    ap.add_argument("--arxiv", action="append", default=[], help="arXiv ID to check (repeatable)")
    ap.add_argument("--ref", action="append", default=[], help="a full reference string (repeatable)")
    ap.add_argument("--file", help="file with references (one per line or blank-line separated)")
    ap.add_argument("--email", default=os.environ.get("CROSSREF_MAILTO") or os.environ.get("NCBI_EMAIL"),
                    help="contact email sent to APIs for polite access")
    ap.add_argument("--no-pubmed", action="store_true", help="skip PubMed cross-checks")
    ap.add_argument("--no-openalex", action="store_true", help="skip OpenAlex cross-checks")
    ap.add_argument("--timeout", type=float, default=20)
    ap.add_argument("--sleep", type=float, default=0.34, help="minimum seconds between requests")
    ap.add_argument("--json", action="store_true", help="print JSON instead of a Markdown table")
    args = ap.parse_args(argv)

    items = []
    items += [{"kind": "doi", "value": clean_doi(d), "text": d} for d in args.doi]
    items += [{"kind": "pmid", "value": p.strip(), "text": f"PMID {p.strip()}"} for p in args.pmid]
    items += [{"kind": "arxiv", "value": a.strip().replace("arXiv:", ""), "text": f"arXiv:{a.strip()}"} for a in args.arxiv]
    for r in args.ref:
        items += items_from_entry(r)
    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            entries = split_entries(fh.read())
        print(f"{len(entries)} reference entries parsed from {args.file}", file=sys.stderr)
        for entry in entries:
            items += items_from_entry(entry)
    if not items:
        ap.print_help()
        return 2

    http = Http(email=args.email, timeout=args.timeout, sleep=args.sleep)
    results = []
    for it in items:
        results.append(verify_item(http, it, use_pubmed=not args.no_pubmed, use_openalex=not args.no_openalex))
        if not args.json:
            print(f"checked {len(results)}/{len(items)}: {results[-1]['status']}", file=sys.stderr)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(results))
    statuses = {r["status"] for r in results}
    if statuses & PROBLEM:
        return 1
    if statuses & MANUAL:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
