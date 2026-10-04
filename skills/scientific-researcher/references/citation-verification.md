# Citation Verification

Procedures for confirming that every cited source exists, is described correctly, supports the claim it is attached to, and is still valid.

## Contents
1. Why this matters
2. The three questions for every citation
3. Step-by-step verification procedure
4. Identifiers and where to check them
5. Retractions, corrections, and expressions of concern
6. Preprints and publication status
7. Quotations and attributions
8. Claim-support check
9. Using the bundled scripts
10. Handling failures
11. Citation audit (pre-delivery)

---

## 1. Why this matters

Two kinds of citation error dominate AI-assisted writing:
- **Fabricated or corrupted references:** a plausible author–year–journal combination that does not exist, or a real DOI attached to the wrong paper.
- **Citation–claim mismatch:** the source exists but does not say what the sentence claims (wrong number, wrong population, overstated conclusion, or a different topic).

The second is more common and harder to catch, so existence checks alone are not enough.

## 2. The three questions for every citation

1. **Existence and identity:** does this exact work exist with these authors, title, venue, year, and identifiers?
2. **Support:** does the work, in the part you read, support the exact statement it is attached to?
3. **Validity:** has it been retracted, corrected, flagged with an expression of concern, superseded, or (for preprints) changed on publication?

## 3. Step-by-step verification procedure

For each source you cite:

1. **Locate it in-session** via a database, publisher page, DOI resolver, or repository. Recalled-from-memory references are `[UNV]` until located.
2. **Confirm bibliographic details** against an authoritative record (publisher page, Crossref, PubMed, arXiv, the journal's table of contents):
   - all author names (spelling, order, initials) or "et al." per style;
   - exact title;
   - journal, book, or conference name;
   - year (note online-first versus issue year);
   - volume, issue, pages or article number;
   - DOI, PMID, PMCID, arXiv ID, ISBN as applicable.
3. **Record the access level** (`[FT]`, `[AB]`, `[MD]`, `[SEC]`, `[UNV]`).
4. **Check support** (§8).
5. **Check validity** (§5, §6).
6. **Format** in the chosen citation style; never fill a missing field by guessing. If a field cannot be confirmed, omit it or mark it (e.g., "pages not available").

## 4. Identifiers and where to check them

| Identifier | Check at | Notes |
|---|---|---|
| DOI | doi.org resolver; Crossref REST API (`api.crossref.org/works/{doi}`); DataCite for datasets and some preprints | Case-insensitive. A DOI that resolves to a different title than cited is a red flag for fabrication |
| PMID | PubMed; NCBI E-utilities (`esummary`) | PubMed publication types include "Retracted Publication" |
| PMCID | PubMed Central | Full text often available |
| arXiv ID | arxiv.org/abs/{id} | Check version history (v1, v2...) and whether a journal version exists |
| bioRxiv / medRxiv DOI | Server page | Shows "now published in" links when available |
| ISBN | Publisher, national library catalogs, WorldCat | Check edition and year |
| Dataset DOI / accession | DataCite, repository (Zenodo, Dryad, GenBank, PDB, etc.) | Record version and access date |
| Clinical trial | ClinicalTrials.gov, WHO ICTRP, EU CTR, ISRCTN | Compare registered vs reported outcomes |

## 5. Retractions, corrections, and expressions of concern

Check status for every source a key claim relies on, and for all references in Deep work. Sources:
- **Crossref metadata**: the work record may contain `updated-by` entries (type `retraction`, `correction`, `expression_of_concern`, etc.), including data from the Retraction Watch database.
- **Retraction Watch database** (now openly available via Crossref).
- **PubMed**: publication type "Retracted Publication"; linked notices ("Retraction in," "Erratum in," "Expression of concern in").
- **OpenAlex**: `is_retracted` flag.
- **Publisher page**: retraction or correction notices; watermarks on the PDF; title prefixed with "RETRACTED:".
- **PubPeer** comments: signals of concern, not findings of misconduct.

How to handle what you find:
- **Retracted:** do not use as ordinary supporting evidence. If historically relevant, cite it explicitly as retracted, cite the retraction notice, and explain why it was retracted (in the notice's own terms).
- **Expression of concern:** use with an explicit caveat or avoid for key claims.
- **Correction / erratum:** check whether the correction affects the claim you cite; cite the corrected version and, if relevant, the correction.
- **Superseded guidance or updated review:** cite the current version unless discussing history.

Absence of a retraction flag in one database is not proof of validity; databases lag. Check at least one additional source for key claims.

## 6. Preprints and publication status

Distinguish: peer-reviewed publication; accepted manuscript; preprint; conference abstract; unpublished manuscript; thesis.
- Label preprints explicitly in the text when they carry an important claim: "a preprint not yet peer reviewed reported...".
- Check whether the preprint was later published (Crossref `relation` field such as `is-preprint-of`, server "now published" links, or a title search). If published, cite the published version and check whether results changed.
- Withdrawn preprints are treated like retractions.

## 7. Quotations and attributions

- Use quotation marks only for wording you saw verbatim in-session (in the original source, or a faithful reproduction you can name), or that the user supplied.
- Record the exact location (page, section, timestamp) when possible.
- If only a paraphrase can be verified, paraphrase without quotation marks and cite.
- For famous quotations, find the earliest documented source. Many popular science quotations are misattributed or altered. If authenticity cannot be established, say "widely attributed to X; we could not locate it in X's published work."
- When translating a quotation, mark it as a translation and identify the original language; do not present a translation as the original wording.

## 8. Claim-support check

For each cited sentence, open the source passage and check:
- **Same claim:** does the source state this, or something weaker/different?
- **Same numbers:** effect size, CI, sample size, units, time frame match exactly?
- **Same population and setting:** species, age group, condition, country, period?
- **Same direction and strength:** no upgrade from association to causation, from "may" to "does," from subgroup to overall?
- **Source's own conclusion versus its data:** if the abstract overstates the results, cite the results.
- **Right source type:** is a primary source needed instead of a review?

A citation that discusses the same topic but not the specific claim does not count. Either find a source that supports the claim, weaken the claim to what the source supports, or remove it.

## 9. Using the bundled scripts

`scripts/verify_citations.py` (standard library only; needs network access to Crossref, doi.org, DataCite, PubMed, OpenAlex, and arXiv):

```bash
# Preferred: full reference text, so titles, first authors, and years are compared
python3 scripts/check_citation_consistency.py draft.md --export-refs refs.txt
python3 scripts/verify_citations.py --file refs.txt --email you@example.org

# Individual identifiers (existence and status only; nothing to compare against)
python3 scripts/verify_citations.py --doi 10.1000/xyz123 --pmid 12345678 --arxiv 2101.00001

# JSON output for further processing
python3 scripts/verify_citations.py --file refs.txt --json
```

The input file may hold one reference per line, numbered or bulleted lists (wrapped lines are joined), or references separated by blank lines; heading lines are skipped, and the number of entries parsed is printed so you can confirm nothing was merged or dropped. Lines without identifiers are matched by bibliographic search.

| Status | Meaning |
|---|---|
| `OK` | Exists; title, first author, and year agree with the reference text (or no text to compare) |
| `CORRECTED` | A correction, erratum, or similar notice exists: check whether it affects the cited claim |
| `PREPRINT` | Preprint record; check for a published version |
| `REGISTERED_ELSEWHERE` | DOI exists with a non-Crossref agency (e.g., mEDRA, JaLC); compare details manually |
| `UNCHECKED` | Service unreachable: **not verified, not evidence of non-existence** |
| `PROBABLE_MATCH` | Bibliographic search found a candidate that needs manual confirmation |
| `NO_CONFIDENT_MATCH` | Search found nothing close (books and reports are often absent from Crossref) |
| `NOT_FOUND` | The DOI registration agency, PubMed, or arXiv says the identifier does not exist |
| `MISMATCH` | Identifier resolves to a work whose title, first author, or year differs from the reference |
| `EXPRESSION_OF_CONCERN` | Journal has flagged the work |
| `PARTIALLY_RETRACTED` / `RETRACTED` | Retraction or withdrawal notice exists |

DataCite records (datasets, software, many repository preprints) are checked for existence and identity, but DataCite does not provide retraction status.

`scripts/check_citation_consistency.py` checks the draft itself:

```bash
python3 scripts/check_citation_consistency.py draft.md            # auto-detect numeric vs author-year
python3 scripts/check_citation_consistency.py draft.md --style numeric
```

It reports in-text citations without references, references never cited, duplicate references, out-of-order numbering (for Vancouver/IEEE/AMA/Nature), and leftover placeholders or `[UNV]`-style tags outside an "Unverified leads" section. It recognizes bracketed, linked (`[1](#r1)`), `<sup>`/`^n^`, and Unicode superscript citations, plus author-year forms with or without commas.

Both scripts check form and metadata only. Neither can judge whether a source supports a claim; §8 remains a manual reading task. Script findings can be wrong (unusual formats, transliterated names): confirm a flag before acting on it.

## 10. Handling failures

| Situation | Action |
|---|---|
| Cannot locate the source (`NOT_FOUND`, `NO_CONFIDENT_MATCH` after manual searching) | Do not cite it as verified. Remove it, or move it to **Unverified leads** with a note |
| `PROBABLE_MATCH` or `REGISTERED_ELSEWHERE` | Open the record or landing page and compare title, authors, year; then treat as `OK` or `MISMATCH` |
| Located, but details differ (`MISMATCH`) | Use the authoritative details; re-check that it is the same work and that it supports the claim |
| DOI resolves to a different paper | Treat the original reference as unreliable; find the intended work by title, or drop it |
| `RETRACTED`, `PARTIALLY_RETRACTED`, `EXPRESSION_OF_CONCERN` | Follow §5 |
| Source does not support the claim | Revise the claim, find a supporting source, or delete the claim |
| Only abstract accessible | Label `[AB]`; limit claims to what the abstract states |
| `UNCHECKED` / network checks unavailable | Say so; verify manually by web search where possible; label remaining items `[UNV]` |

Never "repair" a reference by filling in details you have not seen in an authoritative record.

## 11. Citation audit (pre-delivery)

Run on every Standard or Deep deliverable:

- [ ] **Existence:** every reference located in-session.
- [ ] **Identity:** authors, title, venue, year, volume/issue/pages, identifiers match the authoritative record.
- [ ] **Support:** each in-text citation supports the exact sentence or clause it is attached to.
- [ ] **Placement:** citations sit next to the claims they support, not dumped at paragraph ends.
- [ ] **Consistency:** every in-text citation appears in the references and vice versa (run the consistency script where possible).
- [ ] **Script flags resolved:** every non-`OK` status from the verifier has been investigated and acted on (§10).
- [ ] **Style:** a single style, applied consistently.
- [ ] **Integrity:** no guessed fields; no identifiers from memory.
- [ ] **Validity:** key sources checked for retraction, correction, expression of concern, and preprint status.
- [ ] **Access honesty:** text does not imply full-text reading where only abstracts or metadata were seen.
- [ ] **Unverified items:** listed separately, never mixed into the verified references.
