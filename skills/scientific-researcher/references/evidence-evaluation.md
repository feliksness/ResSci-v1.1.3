# Evidence Evaluation

How to rank sources, judge how strong a body of evidence is, handle disagreement, and choose wording that matches the evidence.

## Contents
1. Source tiers
2. Primary versus secondary evidence
3. Source independence
4. Rating the strength of a body of evidence
5. Conflicting evidence
6. Null results and publication bias
7. Consensus and scientific debates
8. Recency and version awareness
9. Funding and conflicts of interest
10. Famous claims and popular "facts"
11. Scientific logic: keeping categories apart
12. Logical fallacies to watch for
13. Calibrated language ladder

---

## 1. Source tiers

Use higher tiers as evidence and lower tiers for discovery and context. The ranking is a default, not a law: judge each source by its fitness for the specific claim.

| Tier | Examples | Typical role |
|---|---|---|
| 1 | High-quality systematic reviews and meta-analyses; consensus statements and evidence-based guidelines from recognized bodies; strong peer-reviewed primary studies; major authoritative scientific assessments (e.g., national academies, IPCC-type assessments) | Primary evidence for conclusions |
| 2 | Other peer-reviewed primary research; high-quality narrative reviews; scholarly books and monographs; curated research datasets | Evidence, with appraisal |
| 3 | Preprints; conference proceedings and abstracts; dissertations; institutional research reports | Evidence with explicit caveats about review status |
| 4 | Reputable science journalism; university, museum, and government explanatory pages | Context, discovery, plain-language framing |
| 5 | Blogs, forums, social media, unreferenced websites, Wikipedia | Discovery only; follow their references to real sources |

Context overrides the default ranking when appropriate:
- For an official statistic (national mortality, unemployment, emissions inventory), the issuing agency's dataset outranks a journal article that quotes it.
- For an established physical constant, the authoritative compilation (e.g., CODATA values via NIST) outranks any single paper.
- A poorly conducted systematic review can be weaker than one large, well-conducted trial. Appraise reviews too (AMSTAR 2, ROBIS).
- In mathematics, a peer-reviewed proof or a formally verified proof is the evidence; "tiers" of empirical studies do not apply.
- In fast-moving computer science, peer review often happens at conferences and preprints are standard; still label them.

Lower-tier sources may be cited for what they are (for example, "a widely shared claim on social media states X; we found no peer-reviewed support"), never as substitutes for primary evidence.

## 2. Primary versus secondary evidence

- Use reviews to understand the field: scope, consensus, disagreement, history, and which primary studies matter.
- When a precise finding matters (an effect size, a sample size, a measured value, a date), go to the primary study and cite it. Do not cite a review for a detailed numerical claim if the original is accessible.
- If you cannot access the primary study, cite the review and say so: "as summarized by [review]" and label the claim `[SEC]`.
- Watch for drift: secondary descriptions often round, generalize, or strengthen findings. Compare the review's description with the original when the claim matters.
- Abstracts can overstate findings relative to the results section ("spin"). When the full text is available, check the abstract's claims against the results, especially for non-significant primary outcomes.

## 3. Source independence

Repetition is not replication. Before counting sources as independent confirmation, check whether they share:
- the same dataset, cohort, biobank, or trial (many papers can come from one cohort);
- the same experiment or simulation run;
- the same research group or consortium;
- the same press release, preprint, or single underlying study;
- the same flawed instrument or reference standard.

Trace claims to their origin. If five reviews all rely on the same two trials, the evidence base is two trials.

## 4. Rating the strength of a body of evidence

Rate the body of evidence for each major conclusion, not individual papers. Consider:

| Factor | Question |
|---|---|
| Quantity | How many independent studies, and how large? |
| Design | Can these designs support the conclusion (e.g., causal claims)? |
| Risk of bias | How likely are the results distorted by design or conduct flaws? |
| Consistency | Do results agree in direction and roughly in magnitude? Is heterogeneity explained? |
| Directness | Do studies address the actual population, intervention/exposure, comparator, and outcome of the question? |
| Precision | Are confidence intervals narrow enough to support a decision or conclusion? |
| Magnitude | Is the effect large enough to matter and too large to be explained by plausible bias? |
| Dose–response | Does more exposure produce more effect? |
| Replication | Has the finding been independently reproduced? |
| Plausibility | Is there a coherent, independently supported mechanism? |
| Publication bias | Could unpublished null results change the picture? |

**GRADE (health and many applied sciences).** Start randomized evidence at High and observational evidence at Low. Rate down for risk of bias, inconsistency, indirectness, imprecision, and publication bias. Rate up (mainly observational evidence) for a large effect, a dose–response gradient, or when all plausible residual confounding would reduce the observed effect. Final certainty: High, Moderate, Low, Very low. Apply GRADE per outcome, not per paper.

**Evidence categories (all fields).** Use the canonical categories defined in SKILL.md §6: **Very strong, Strong, Moderate, Limited, Preliminary, Mixed / Conflicting, Insufficient**. Where GRADE was applied, report the GRADE level as well. State the reason for the category in the text when it matters ("we rate this evidence as limited: two small observational studies with inconsistent results").

**Many papers is not strong evidence.** A large number of small, biased, or dependent studies does not outweigh a few large, well-designed, independent ones. Reputation of authors or journals does not substitute for appraisal.

## 5. Conflicting evidence

When results disagree, investigate before concluding. Compare:
- population (age, sex, disease stage, species, strain, geography, era);
- sample size and power;
- design (randomized vs observational; in vitro vs in vivo);
- exposure or intervention definition, dose, timing, duration;
- outcome definition, measurement instrument, and timing;
- statistical model, covariates, handling of missing data;
- inclusion and exclusion criteria;
- follow-up length;
- setting, period, and co-interventions;
- methodological quality and risk of bias;
- funding and conflicts of interest;
- whether later replication attempts succeeded.

Then report: what disagrees, the most plausible explanations, which body of evidence is stronger and why, and what study would resolve it. Do not average conflicting results conceptually ("on balance, X has a modest effect") without understanding why they differ.

## 6. Null results and publication bias

- Search explicitly for null findings, failed replications, negative trials, and studies finding no association. Useful sources: trial registries (results posted but never published), replication projects, registered reports, journals and repositories that publish null results, conference abstracts, and dissertations.
- Compare registered protocols with published outcomes to detect outcome switching.
- Consider whether a literature consists mainly of small positive studies (a classic signature of small-study effects or publication bias).
- If publication bias is plausible and cannot be ruled out, say so and lower confidence.

## 7. Consensus and scientific debates

Never write "scientists agree" without a defensible basis. Name the basis: systematic reviews, statements from scientific academies or professional bodies, formal assessments, surveys of expert opinion, or repeated independent replication. Distinguish:
- **broad consensus** (strong evidence, recognized bodies concur, little credible dissent);
- **majority interpretation** (most experts lean one way; credible minority positions exist);
- **active controversy** (credible evidence on more than one side);
- **unresolved question** (evidence insufficient).

For controversial topics present: the strongest evidence for position A; the strongest evidence for position B; the methodological differences; the quality of each evidence base; the current state of consensus; the remaining uncertainty. Do not manufacture false balance: if one side rests on far stronger evidence, say so. Proportion the text to the evidence.

## 8. Recency and version awareness

- In fast-moving fields (clinical guidelines, infectious disease, ML, genomics, climate attribution), search the last few years explicitly and check for updated guidelines, new trials, and retractions.
- In stable foundational topics, keep landmark studies; cite the original discovery and the current evidence separately.
- Distinguish the date of the original discovery, the date of the current best evidence, and the date of the current consensus statement.
- Check whether a guideline or review has been superseded, and whether a preprint has since been published with changed results.

## 9. Funding and conflicts of interest

Record funding sources and author disclosures when available. Industry funding, advocacy funding, or institutional interest is a reason to look harder at design choices (comparator, dose, outcome selection, analysis, spin), not proof that the results are wrong. Weigh conflicts alongside methodological quality and independent replication. More detail: `research-integrity.md`.

## 10. Famous claims and popular "facts"

Popularity is not evidence. For well-known claims ("we only use 10% of our brains," famous statistics, iconic quotations):
- trace the claim to its original publication, speech, or dataset;
- check whether the original says what is claimed (popular versions often distort);
- check later evidence that corrected or overturned it;
- if attribution is disputed or unverifiable, say so explicitly.

## 11. Scientific logic: keeping categories apart

Keep these distinct in reasoning and in prose:

| Category | What it is |
|---|---|
| Observation / measurement | What was recorded, with its uncertainty |
| Experiment | A manipulation with controls |
| Model / simulation | Output of a formal or computational model under assumptions |
| Prediction / projection | Model-based statement about unobserved or future states |
| Inference | A conclusion drawn from data via reasoning or statistics |
| Interpretation / explanation | A proposed account of why the observations occurred |
| Hypothesis | A testable proposition not yet established |
| Conclusion | What the total evidence supports, with stated confidence |

A model result is not an observation. A theoretical prediction is not an experimental result. A mechanism inferred from correlation is a hypothesis.

## 12. Logical fallacies to watch for

Name these when they appear in sources, in the user's framing, or in your own draft:
- correlation–causation error; post hoc reasoning;
- cherry-picking; confirmation bias;
- appeal to authority (reputation in place of evidence);
- survivorship bias; selection bias; collider bias;
- ecological fallacy (group-level association applied to individuals);
- base-rate neglect (especially in diagnostic tests and screening);
- false dichotomy;
- anecdote as evidence;
- argument from ignorance ("no evidence of harm" read as "evidence of no harm");
- overgeneralization (from one species, population, setting, or condition to all).

## 13. Calibrated language ladder

Same categories as SKILL.md §6, with more wording options and phrasings to avoid.

| Category | Wording | Avoid |
|---|---|---|
| Very strong | "Multiple high-quality studies consistently demonstrate..."; "It is well established that..." (with named basis) | "proves" (except for mathematical proof) |
| Strong | "Evidence strongly supports..."; "Robust evidence indicates..." | "definitively shows" |
| Moderate | "Available evidence suggests..."; "is likely" | "clearly" |
| Limited | "Limited evidence indicates..."; "may" | generalizing beyond the studied population |
| Preliminary | "Preliminary evidence indicates..."; "One study reported..."; "In mice, ..." | treating a single or early study as settled |
| Mixed / Conflicting | "Studies have produced mixed findings..."; "Well-conducted studies conflict on..." | picking the convenient side |
| Insufficient | "Current evidence is insufficient to determine..."; "This has not been adequately studied." | "there is no effect" (absence of evidence is not evidence of absence) |

**Causal versus associational wording** (independent of strength):

| Evidence shows | Use | Avoid |
|---|---|---|
| Association only | "is associated with"; "is correlated with"; "predicts" | "causes," "leads to," "drives," "increases risk" (as a causal verb) |
| Causation established (Section 5 of `study-designs.md`) | "causes," "reduces," "increases" | stronger generalization than the studied population supports |

Hedging should be accurate, not decorative: do not hedge well-established findings into vagueness either.
