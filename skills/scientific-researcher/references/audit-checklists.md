# Audit Checklists

Run these before delivering any Standard or Deep deliverable. For Quick answers, run the anti-hallucination audit mentally on the few claims made. Fix every failure before delivery; if something cannot be fixed, remove it or disclose it.

## Contents
1. Fact-check pass
2. Citation audit
3. Anti-hallucination audit
4. Article-type integrity check
5. Final quality gate
6. Publication-quality standard

---

## 1. Fact-check pass

For every major factual statement in the draft, ask:

1. Is this a factual claim (as opposed to interpretation or opinion clearly marked as such)?
2. Does it need a citation? (Anything not common knowledge in the field does.)
3. Is the cited source authoritative enough for this claim?
4. Does the source directly support this exact statement (numbers, population, direction, strength)?
5. Is the wording stronger than the evidence?
6. Is there contradictory evidence that should be mentioned?
7. Is the source current enough for this topic?
8. Has the source been corrected or retracted?
9. Am I relying on a secondary source where the primary is available and needed?
10. Did I infer something the evidence does not establish (causation, mechanism, generalization to another population)?

Revise or remove statements that fail. A practical method: extract every sentence containing a number, a causal verb, a superlative, or a consensus claim, and check each against the evidence table.

## 2. Citation audit

Use the checklist in `citation-verification.md` §11, plus the scripts where available:

```bash
python3 scripts/check_citation_consistency.py draft.md --export-refs refs.txt
python3 scripts/verify_citations.py --file refs.txt
```

Use the exported full reference text (not bare DOIs), so the verifier can detect a real DOI attached to the wrong title, author, or year.

Every reference must pass existence, identity, support, consistency, integrity, validity, and access-honesty checks. Resolve failures as described in `citation-verification.md` §10: correct, replace, weaken the claim, move to **Unverified leads**, or disclose. Never remove a `[citation needed]` or `[UNV]` marker while keeping the unsupported claim. `UNCHECKED` means the check could not run, so verify manually or label `[UNV]`.

## 3. Anti-hallucination audit

Ask explicitly: **did I invent anything?** Check each category:

| Category | Check |
|---|---|
| Facts | Each traces to a source in the evidence table or is well-established common knowledge in the field |
| Sources | Each was located in-session; none recalled and formatted from memory without a `[UNV]` label |
| Quotations | Each was seen verbatim; otherwise converted to paraphrase |
| Statistics | Each number appears in the source or was computed in-session; precision and units match |
| Dates | Each date checked (publication, discovery, guideline version) |
| Sample sizes | Taken from the source, randomized vs analyzed distinguished |
| Study conclusions | Reflect the study's actual results, not its abstract's spin or my extrapolation |
| Identifiers | DOIs, PMIDs, URLs retrieved, not typed from memory |
| Terminology | Used in the field's standard sense |
| Consensus claims | Basis named (review, academy statement, replication) |
| Methodology claims | Describe only what was done in this session |

If uncertainty remains about any item, preserve the uncertainty in the text instead of resolving it by assertion.

## 4. Article-type integrity check

- Is the label (systematic review, meta-analysis, narrative review, explainer, original research) accurate for what was done?
- Are search counts, screening numbers, and statistical results all from actual logs and computations?
- Are limitations of the process (databases, access, single reviewer, dates) disclosed?

## 5. Final quality gate

| Item | Question |
|---|---|
| Accuracy | Are factual statements supported? |
| Sources | Are the strongest available sources used? |
| Verification | Were important sources actually checked? |
| Citation | Does every major claim have appropriate evidence, placed next to it? |
| Integrity | Did anything get invented? |
| Causality | Did association become causation anywhere? |
| Statistics | Are numerical claims correctly interpreted, with absolute effects and uncertainty where relevant? |
| Contradictions | Was opposing evidence searched for and represented proportionally? |
| Bias | Did I favor evidence that supports the initial hypothesis or the user's preference? |
| Recency | Is the literature current enough for this topic? |
| Retractions | Were key sources checked for correction or retraction? |
| Uncertainty | Is uncertainty communicated honestly and, where possible, quantitatively? |
| Methodology | Is what was actually done described accurately? |
| Reproducibility | Could another researcher follow and repeat the process? |
| Writing | Is it clear, precise, and free of unnecessary jargon? |
| Conclusion | Does the conclusion match the evidence and answer the question asked? |

If any critical item (Accuracy, Verification, Integrity, Causality, Methodology, Conclusion) fails, correct the article before delivery.

## 6. Publication-quality standard

Call work "publication-quality" or "publication-ready" only if all of the following hold, and disclose remaining limitations:
- scientifically defensible conclusions matched to evidence strength;
- every substantive claim supported by a verified citation;
- internally consistent (numbers, terminology, claims across abstract, body, and conclusion);
- methods described transparently and truthfully;
- appropriate caution and explicit limitations;
- reproducible where applicable (search strategy, data, code);
- no fabricated sources, results, or quotations;
- structure appropriate to the field and article type, following the relevant reporting guideline;
- references in one consistent style, audited.

Even then, recommend expert human review before submission: no automated process substitutes for peer review, and an AI-only screening and appraisal process does not meet dual-reviewer standards.
