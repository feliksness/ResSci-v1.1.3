# Systematic, Scoping, and Rapid Review Methods

Use this file when the task genuinely calls for a structured review. Do not force this workflow onto a simple explainer or a narrative overview.

## Contents
1. Choosing the review type
2. Question frameworks
3. Protocol
4. Search strategy
5. Search documentation
6. Deduplication, screening, and eligibility
7. Data extraction
8. Risk of bias and certainty
9. Synthesis
10. Reporting (PRISMA and related)
11. What an AI-assisted review can and cannot claim
12. Quick decision table

---

## 1. Choosing the review type

| Type | Purpose | Minimum to earn the label |
|---|---|---|
| Systematic review | Answer a focused question using all available evidence | Pre-specified question and eligibility criteria; reproducible search of multiple sources; documented screening; risk-of-bias assessment; transparent synthesis |
| Meta-analysis | Quantitatively pool effects | A systematic review (normally) plus actual statistical pooling of extracted data |
| Scoping review | Map the extent, range, and nature of evidence; identify concepts and gaps | Systematic search and charting; appraisal optional; does not make effectiveness conclusions |
| Rapid review | Timely evidence for decisions | Systematic methods with declared shortcuts (e.g., one database, single screener, date limits) |
| Umbrella review | Synthesize systematic reviews | Systematic search for reviews; review-level appraisal (AMSTAR 2/ROBIS); overlap handling |
| Narrative review | Expert synthesis and interpretation | Honest description of how sources were found; no claim of systematic methodology |

If shortcuts are needed, call it a rapid review or a narrative review with a structured search, and state the shortcuts.

## 2. Question frameworks

Use a framework when it sharpens the question; skip it when it does not fit.

| Framework | Elements | Best for |
|---|---|---|
| PICO | Population, Intervention, Comparator, Outcome (+ Time, Setting) | Intervention effectiveness |
| PECO | Population, Exposure, Comparator, Outcome | Exposures and environmental or occupational risks |
| PIRD | Population, Index test, Reference standard, Diagnosis of interest | Diagnostic accuracy |
| PFO | Population, prognostic Factor, Outcome | Prognosis |
| PICOTS | PICO plus Timing and Setting | Interventions where timing and setting matter; prognostic and prediction questions |
| SPIDER | Sample, Phenomenon of Interest, Design, Evaluation, Research type | Qualitative and mixed-methods |
| PCC | Population, Concept, Context | Scoping reviews |
| CoCoPop | Condition, Context, Population | Prevalence and incidence |

For non-health fields, define the equivalent explicitly: system/material/sample, manipulation or condition, comparison, measured property, and context (e.g., "In perovskite solar cells (system), does additive X (intervention) compared with no additive (comparator) improve operational stability under standardized aging protocols (outcome, context)?").

## 3. Protocol

Write it before searching:
- question and framework elements;
- eligibility criteria (designs, populations, interventions/exposures, comparators, outcomes, languages, dates, publication types) with rationale;
- information sources and draft search strategy;
- screening process;
- data items to extract;
- risk-of-bias tool;
- synthesis plan (including when pooling will and will not be done);
- certainty assessment method.

Do not claim registration (e.g., PROSPERO, OSF) unless the user has actually registered and supplies the identifier.

## 4. Search strategy

- Build one block per concept with free-text terms and controlled vocabulary (e.g., MeSH in PubMed/MEDLINE, Emtree in Embase), combine synonyms with OR and concepts with AND.
- Use truncation, phrase searching, and proximity operators where the interface supports them; adapt syntax per database.
- Test the strategy against a set of known relevant studies; if it misses them, revise.
- Search multiple sources appropriate to the field (see `field-specific-methods.md` § Where to search), plus trial registries and grey literature where relevant.
- Supplement with citation chasing: backward (reference lists) and forward (citing articles).
- Search explicitly for counter-evidence and null results.
- Record any limits and why (date, language, publication type). Language restrictions are a limitation to declare.

## 5. Search documentation

Keep a research log (`templates/research-log.md`) with, for each search:
- date searched;
- database or source and interface/platform;
- exact query string as run;
- filters and limits;
- number of records returned (as displayed, never estimated);
- notes.

Also log screening decisions with reasons for exclusion at full-text stage. Every number in a PRISMA-style flow must come from this log.

## 6. Deduplication, screening, and eligibility

1. **Deduplicate** by DOI/PMID, then by normalized title + year + first author. Record the count removed.
2. **Title/abstract screening** against eligibility criteria; be inclusive when unsure.
3. **Full-text eligibility**: obtain full texts; record a reason for every exclusion (wrong population, wrong design, wrong outcome, duplicate report, etc.).
4. **Linked reports**: group multiple publications from the same study; the unit of synthesis is the study, not the paper.

Gold standard is two independent reviewers with conflict resolution. An AI acting alone does not meet that standard; say so in the methods and limitations, and suggest human verification of a sample.

## 7. Data extraction

Pre-define fields: study identifiers; design; setting; dates; population characteristics; sample size (randomized/analyzed); intervention/exposure details; comparator; outcomes with definitions and time points; effect estimates with uncertainty; funding and conflicts; risk-of-bias inputs; notes.

- Extract numbers exactly as reported, with location (table/figure/page).
- Record when values are derived (e.g., SE computed from CI) and how.
- Never impute missing data silently; if imputation is used, document the method and run sensitivity analyses.
- Do not extract numbers by reading values off figures without saying so (and naming the method/tool).

## 8. Risk of bias and certainty

- Apply the tool matching each design (`study-designs.md` §4), domain by domain, with supporting quotes or reasons.
- Summarize risk of bias per outcome, not just per study.
- Rate certainty of the body of evidence per outcome with GRADE (or an equivalent framework in non-health fields); present a summary-of-findings table for key outcomes.

## 9. Synthesis

- **Meta-analysis** only when conditions in `statistics.md` §12 are met. Report model, effect measure, heterogeneity, sensitivity analyses, and small-study assessment.
- **Structured narrative synthesis** otherwise: group studies by meaningful features, use consistent metrics (e.g., vote counting based on direction of effect, not on p-values), tabulate, and explain heterogeneity. Follow the SWiM (Synthesis Without Meta-analysis) reporting guideline.
- **Qualitative evidence synthesis**: thematic synthesis or meta-ethnography; assess confidence with GRADE-CERQual.

## 10. Reporting (PRISMA and related)

- **PRISMA 2020** for systematic reviews (27-item checklist plus abstract checklist and flow diagram). PRISMA-S for reporting searches, PRISMA-P for protocols, PRISMA-ScR for scoping reviews, and other extensions as applicable (e.g., network meta-analysis, diagnostic test accuracy).
- Use the current version from the EQUATOR Network.
- A flow diagram is only valid if every number in it comes from the log. A PRISMA diagram does not make a review PRISMA-compliant; the checklist items must be reported.
- Report deviations from the protocol.

## 11. What an AI-assisted review can and cannot claim

Can claim (when true): the exact sources searched, queries run, dates, counts displayed, screening decisions made, and analyses computed.

Cannot claim without evidence: comprehensive coverage of databases not actually searched (Embase, Web of Science, Scopus, CINAHL, and PsycINFO typically require subscriptions); dual independent screening; protocol registration; contact with study authors; translation of non-English full texts not actually read.

State access limitations plainly: paywalled full texts not read, databases unavailable, single-reviewer screening.

## 12. Quick decision table

| User asks for... | Do |
|---|---|
| "A systematic review on X" | Full workflow; if tools or access limit it, deliver a rapid review or structured narrative review and explain why the label changed |
| "A meta-analysis" | Systematic workflow + pooling only if data permit; otherwise structured narrative synthesis with explanation |
| "A literature review" | Narrative review with a transparent, documented search; no systematic claims |
| "What does the evidence say about X" | Standard-depth evidence synthesis; start from high-quality systematic reviews and guidelines, then check for newer primary studies |
| "Map the research on X" | Scoping review approach |
