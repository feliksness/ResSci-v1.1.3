# Scientific Writing

How to structure, write, and reference the final article so that every claim stays traceable to evidence.

## Contents
1. Article types and honest labels
2. Structures by article type
3. Section guidance for a research synthesis
4. Synthesis, not summary
5. Research gaps
6. Limitations
7. Reproducibility statement
8. Definitions and terminology
9. Style
10. Citation placement
11. Citation styles
12. Figures and tables
13. Presenting uncertainty
14. Translation
15. Historical claims

---

## 1. Article types and honest labels

The article-type label is a claim about methodology. Use the label in SKILL.md §3 that matches what was actually done. If the user asked for a "systematic review" but only a narrative review was possible, write the narrative review and explain the change in the scope note and methods.

## 2. Structures by article type

Adapt to the user's target journal or format when specified.

| Type | Typical structure | Reporting guideline (if any) |
|---|---|---|
| Evidence synthesis / evaluation of a claim | Question or claim, Bottom line (with confidence), What the evidence shows (by line of evidence), Contradictory evidence, What remains uncertain, Sources | — |
| Research synthesis / narrative review | Title, Abstract, Keywords, Introduction, Approach (how literature was identified), Thematic sections, Discussion, Limitations, Conclusion, References | — (be transparent about search) |
| Systematic review / meta-analysis | Title, Structured abstract, Introduction, Methods (protocol, eligibility, sources, search, selection, extraction, RoB, synthesis, certainty), Results (flow, characteristics, RoB, syntheses, certainty), Discussion, Other information (registration, funding, conflicts), References | PRISMA 2020 |
| Scoping review | As above, with charting instead of appraisal-driven conclusions | PRISMA-ScR |
| Original research (empirical) | Title, Abstract, Introduction, Methods, Results, Discussion, Conclusion, Data/code availability, References (IMRaD) | CONSORT, STROBE, STARD, TRIPOD, ARRIVE, etc., by design |
| Case report | Title, Abstract, Introduction, Case presentation (timeline), Discussion, Patient perspective/consent statement, References | CARE |
| Theoretical / mathematical paper | Introduction, Preliminaries/definitions, Main results (theorems with proofs), Discussion, References | — |
| Methodological paper | Problem, Existing methods and limitations, Proposed method, Evaluation, Discussion | — |
| Technical report | Executive summary, Background, Methods, Findings, Recommendations (if evidence permits), Limitations, Appendices | — |
| Scientific essay | Thesis or question, Argument organized by evidence, Counterarguments and their evidence, Conclusion matched to evidence, References | — |
| Scientific explainer | Plain-language summary up front, What we know (with confidence), What is uncertain, Why it matters, Sources | — |
| Historical scientific analysis | Context, Primary sources, Analysis, Historiographical debates, Conclusion | — |

## 3. Section guidance for a research synthesis

- **Title:** precise, informative, non-sensational. State the question or scope; avoid claims the evidence cannot support ("X cures Y").
- **Abstract:** background, objective, methods (what was actually done), findings with strength of evidence, conclusion matched to evidence. No claims absent from the body.
- **Keywords:** standard terms in the field (use controlled vocabulary such as MeSH terms where relevant).
- **Introduction:** what is established (with citations), the specific problem, why it matters, the gap, the research question and objectives.
- **Methods / approach:** sources searched, dates, query strategy, inclusion logic, appraisal approach, synthesis approach, tools and software, and access limits. Describe only what was done.
- **Results / evidence synthesis:** findings organized by theme or question, with strength of evidence. Keep reporting separate from interpretation.
- **Discussion:** interpretation, mechanisms (labeled as established or hypothesized), competing explanations, agreements and disagreements with prior work, implications proportional to evidence, limitations.
- **Conclusion:** answer the research question directly with appropriate confidence. Introduce nothing new.
- **Limitations:** a dedicated section (see §6).
- **References:** complete and verified (`citation-verification.md`).

## 4. Synthesis, not summary

Avoid "Author A found X. Author B found Y. Author C found Z." Organize around:
- themes and sub-questions;
- mechanisms and competing hypotheses;
- methodological approaches and how they shape findings;
- strength and consistency of evidence;
- disagreements and their likely explanations;
- historical development where it explains the current state;
- unresolved questions.

A useful paragraph pattern: **claim (with strength) → supporting evidence (with design and size) → qualifications or contrary evidence → what this means.**

## 5. Research gaps

A gap is not "one paper didn't study this." Defensible gaps include: contradictory findings without explanation; lack of replication; under-studied populations or settings; methodological weaknesses common to the literature; lack of longitudinal or causal evidence; poor or inconsistent measurement; unresolved mechanisms; missing geographic or demographic coverage. For each gap, say why it matters and what kind of study would address it.

## 6. Limitations

Cover limitations of both the evidence and the research process:
- evidence: risk of bias, heterogeneity, imprecision, indirectness, publication bias, generalizability, measurement;
- process: databases not searched, paywalled texts not read, language restrictions, single-reviewer screening, date of search, reliance on abstracts, no independent verification of statistics.

Do not hide limitations because they weaken the article; they are part of the result.

## 7. Reproducibility statement

Where applicable, report: data sources and versions; search strategy and dates; inclusion and exclusion criteria; analysis methods and software with versions; parameters and assumptions; preprocessing; code and data availability. If code or data are unavailable, say so. Never claim reproducibility that does not exist.

## 8. Definitions and terminology

- Define technical terms at first use with the discipline's standard meaning.
- Do not mix colloquial and technical meanings ("theory," "significant," "risk," "natural," "toxic").
- Where definitions compete across sources or fields, say so and state which one you use.
- Do not silently redefine a term mid-article.
- Define abbreviations at first use.

## 9. Style

- Precise, analytical, readable, formal, appropriately cautious.
- Use technical terms when they add precision; explain them for broader audiences.
- Avoid fake academic padding, rhetorical exaggeration, sensational framing, repetition, and verbosity.
- Prefer concrete numbers to vague quantifiers ("in 3 of 5 trials" rather than "in several trials").
- Keep tense consistent: past tense for what studies did and found; present tense for established knowledge and for what the evidence currently indicates.
- Calibrate every claim (SKILL.md §6, `evidence-evaluation.md` §13).

## 10. Citation placement

- Place each citation directly after the claim it supports, within the sentence if needed.
- Do not put one citation at the end of a paragraph when it supports only one sentence.
- Avoid citation dumping (long strings of references for a simple claim); cite the strongest and most direct sources.
- Every source should have a reason for being cited.
- When citing a secondary source for a primary finding, say so ("as reported in...").

## 11. Citation styles

Use the user's requested style; otherwise choose an appropriate one for the field and state it. Never mix styles.

| Style | In-text | Typical fields |
|---|---|---|
| APA (7th) | (Author, Year) | Psychology, social sciences, education |
| Harvard | (Author Year) or (Author, Year) | Many disciplines; varies by institution |
| Chicago (author-date or notes-bibliography) | (Author Year) or footnotes | History, humanities, some sciences |
| Vancouver / ICMJE | Numbered in order of first citation [1] | Medicine, biomedicine |
| AMA | Superscript numbers in order of citation | Medicine |
| IEEE | Numbered [1] in order of citation | Engineering, computer science |
| Nature | Superscript numbers in order of citation | Multidisciplinary science |

Formatting must not add information: if the issue number or page range is unknown, omit it rather than guess. Include DOIs where available and verified.

## 12. Figures and tables

- Every value must come from a source or an in-session computation; cite the source in the caption or a note.
- Include units, define abbreviations, and state sample sizes.
- Show uncertainty (CIs, error bars with stated meaning) where appropriate.
- Distinguish observed data from model estimates (e.g., different line styles, labeled).
- Avoid misleading axes (truncated without indication, dual axes implying correlation), inappropriate chart types, and false precision.
- Never draw a chart from nonexistent or guessed data. Never present an illustrative schematic as data.

## 13. Presenting uncertainty

- Quantify where possible: CIs, credible intervals, SDs, measurement uncertainties, ranges, sensitivity analyses, scenario ranges.
- State qualitative uncertainty explicitly when quantification is impossible.
- Do not smooth uncertainty away for cleaner prose.
- Use field-specific calibrated language faithfully (e.g., IPCC likelihood terms, GRADE certainty levels).

## 14. Translation

- Preserve technical meaning, units, symbols, and the strength of claims; do not upgrade "may" into "does."
- Use established terminology in the target language; when no standard term exists, give the original term in parentheses.
- Mark translated quotations as translations; do not present them as original wording.

## 15. Historical claims

- Verify dates and original publications.
- Distinguish direct quotation, paraphrase, and translation.
- Distinguish historically held theories from current evidence.
- Do not attribute modern concepts to historical figures without textual evidence.
