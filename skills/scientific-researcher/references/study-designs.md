# Study Designs, Risk of Bias, and Causal Inference

## Contents
1. Identifying the design
2. What each design can support
3. Bias catalogue
4. Choosing a risk-of-bias or quality tool
5. Causal inference
6. Generalizability (external validity)

---

## 1. Identifying the design

Identify the design from the methods section, not from the title or the authors' label (papers sometimes call a retrospective chart review a "cohort study" or a single-arm study a "trial"). Record: randomized or not; prospective or retrospective; longitudinal or cross-sectional; unit of analysis; comparison group; how exposure and outcome were measured.

## 2. What each design can support

| Design | Can reasonably support | Cannot by itself support | Key weaknesses |
|---|---|---|---|
| Randomized controlled trial (RCT) | Causal effect of an assigned intervention in the trial population | Effects in very different populations; long-term or rare harms if underpowered | Allocation concealment, blinding, attrition, selective reporting, limited generalizability |
| Cluster / crossover / adaptive trial | As RCT, with design-specific assumptions | Ignoring clustering or carryover | Unit-of-analysis errors, carryover, contamination |
| Prospective cohort | Associations, temporal order, incidence, risk estimates | Causation without addressing confounding | Confounding, loss to follow-up, measurement error |
| Retrospective cohort | As cohort, with record-based data | — | Data quality, missing covariates, immortal-time bias |
| Case-control | Associations for rare outcomes (odds ratios) | Incidence or absolute risk (without sampling information) | Recall bias, control selection |
| Cross-sectional | Prevalence; associations at one time point | Temporal order; causation | Reverse causation, prevalence–incidence bias |
| Ecological | Group-level patterns; hypothesis generation | Individual-level inference | Ecological fallacy, confounding |
| Case series / case report | Describing novel phenomena; signals; hypothesis generation | Frequency, causation, efficacy | No comparison group, selection |
| Diagnostic accuracy study | Sensitivity, specificity, predictive values in the studied setting | Clinical benefit of testing | Spectrum bias, imperfect reference standard, verification bias |
| Prognostic / prediction-model study | Risk prediction performance | Causal effects of predictors | Overfitting, leakage, lack of external validation |
| Qualitative study | Experiences, meanings, processes, mechanisms of implementation | Prevalence or effect sizes | Transferability, reflexivity |
| Mixed methods | Integration of both | Claims beyond each component | Integration quality |
| Laboratory experiment | Causal effects under controlled conditions | Effects outside those conditions | Artifacts, calibration, small n, pseudo-replication |
| Animal experiment | Mechanisms and effects in the species/strain studied | Human effects without bridging evidence | Translation failure, lack of randomization/blinding, small n |
| In vitro | Cellular/molecular mechanisms under culture conditions | Organism-level effects | Non-physiological doses, cell-line issues (misidentification, contamination) |
| Mechanistic study | How an effect could occur | That it does occur in the target population | Plausibility mistaken for evidence |
| Computational study / simulation | Consequences of stated assumptions and parameters | Real-world truth without validation | Assumptions, parameter uncertainty, validation |
| Natural / quasi-experiment | Causal effects under specific identifying assumptions | Causation if assumptions fail | Assumption violations (see §5) |
| Systematic review / meta-analysis | Summary of available evidence | Better evidence than its included studies | Garbage in, garbage out; heterogeneity; publication bias |

**Timing terms.** *Prospective* means data collected forward from exposure; *retrospective* means using existing data or recall. *Longitudinal* means repeated measures over time. These modify, not replace, the design label.

## 3. Bias catalogue

| Bias | Description | Where common |
|---|---|---|
| Selection bias | Study sample or analytic sample differs systematically from target population or between groups | Observational studies, case-control control selection |
| Confounding | A common cause of exposure and outcome distorts the association | All non-randomized designs |
| Measurement / information bias | Systematic error in measuring exposure or outcome | All designs |
| Recall bias | Differential recall by outcome status | Case-control, retrospective surveys |
| Performance bias | Groups receive different care besides the intervention | Unblinded trials |
| Detection bias | Outcome assessed differently between groups | Unblinded assessors |
| Attrition bias | Differential loss to follow-up or missing data | Trials, cohorts |
| Reporting bias / selective outcome reporting | Only favorable outcomes or analyses reported | All; check registries and protocols |
| Publication bias | Studies with positive results more likely published | Literatures as a whole |
| Survivorship bias | Only "surviving" units observed | Business, ecology, medicine (prevalent users) |
| Collider bias | Conditioning on a common effect induces spurious association | Hospital-based samples, selected cohorts, adjusting for mediators/colliders |
| Immortal-time bias | Period during which outcome could not occur misclassified | Pharmacoepidemiology with time-varying exposure |
| Lead-time / length-time bias | Earlier detection appears to extend survival | Screening studies |
| Healthy-user / adherer bias | People who adhere differ in health behaviors | Observational drug and supplement studies |
| Reverse causation | Outcome (or its precursor) influences exposure | Cross-sectional and short-follow-up studies |
| Spectrum bias | Test accuracy differs by disease spectrum | Diagnostic studies |
| Data leakage | Information from test data influences training | ML studies |
| p-hacking | Trying analyses until p < 0.05 | Flexible analysis pipelines |
| HARKing | Hypothesizing after results are known, presented as a priori | Exploratory studies written as confirmatory |
| Researcher degrees of freedom | Many undisclosed analytic choices | Any study without pre-registration |

## 4. Choosing a risk-of-bias or quality tool

Use a tool whose assumptions match the design. Use the current official version of each tool, and describe how you applied it. Do not apply a tool mechanically; judgments need reasons tied to the paper's text.

| Design | Tool (examples) | Core domains |
|---|---|---|
| Randomized trials | **RoB 2** | Randomization process; deviations from intended interventions; missing outcome data; measurement of the outcome; selection of the reported result |
| Non-randomized studies of interventions | **ROBINS-I** | Confounding; selection of participants; classification of interventions; deviations from intended interventions; missing data; measurement of outcomes; selection of the reported result |
| Non-randomized studies of exposures | **ROBINS-E** | Similar structure adapted to exposures |
| Diagnostic accuracy | **QUADAS-2** (QUADAS-C for comparative) | Patient selection; index test; reference standard; flow and timing |
| Observational cohort / case-control (simpler appraisal) | **Newcastle–Ottawa-type scales**, JBI checklists | Selection; comparability; outcome or exposure ascertainment |
| Prediction models | **PROBAST** (and its AI extension where relevant) | Participants; predictors; outcome; analysis |
| Animal studies | **SYRCLE RoB** | Adapted from Cochrane domains for animal experiments |
| Systematic reviews | **AMSTAR 2**, **ROBIS** | Protocol, search, selection, RoB handling, synthesis, publication bias |
| Qualitative studies | **CASP**, **JBI** qualitative checklist | Aims, design, recruitment, data, reflexivity, analysis rigor |
| Missing evidence in meta-analysis | **ROB-ME** | Risk of bias due to missing results |
| Body of evidence | **GRADE** (quantitative), **GRADE-CERQual** (qualitative) | See `evidence-evaluation.md` §4 |

Notes:
- Summary scores from quality scales can hide fatal flaws; prefer domain-level judgments.
- A single reviewer (including an AI) applying a tool is not equivalent to independent dual assessment. Disclose this.
- When no validated tool fits (e.g., physics experiments, computational studies), appraise against design-specific criteria: controls, calibration, replication, uncertainty quantification, validation, and code/data availability.

## 5. Causal inference

**Do not write "X causes Y" when the evidence only shows association.** Ask:

1. **Temporal order:** did exposure precede outcome?
2. **Confounding:** what common causes could explain the association? Were they measured and adjusted for appropriately? Could unmeasured confounding plausibly explain it (consider an E-value or quantitative bias analysis if reported)?
3. **Reverse causation:** could early disease or the outcome drive exposure?
4. **Selection effects:** could selection into the study or analysis (including conditioning on a collider) create the association?
5. **Measurement:** could error in exposure or outcome measurement create or mask it?
6. **Intervention evidence:** do randomized trials or natural experiments manipulating the exposure agree?
7. **Consistency and specificity:** does it replicate across populations, designs, and methods with different bias structures (triangulation)?
8. **Dose–response:** is there a gradient?
9. **Mechanism:** is there an independently supported mechanism?

The Bradford Hill considerations (strength, consistency, specificity, temporality, biological gradient, plausibility, coherence, experiment, analogy) are aids to judgment, not a checklist that "proves" causation; only temporality is strictly necessary.

**Quasi-experimental and causal-inference designs** (each rests on assumptions you should state):

| Method | Key assumption to check |
|---|---|
| Directed acyclic graphs (DAGs) | The graph reflects true causal structure; used to choose adjustment sets and spot colliders |
| Target trial emulation | Clear specification of eligibility, time zero, treatment strategies; avoids immortal-time bias |
| Instrumental variables | Instrument affects exposure (relevance), affects outcome only through exposure (exclusion), shares no confounders with outcome (independence) |
| Mendelian randomization | Same IV assumptions using genetic variants; watch horizontal pleiotropy, population stratification, weak instruments |
| Difference-in-differences | Parallel trends absent treatment; no simultaneous shocks |
| Regression discontinuity | No manipulation at the threshold; continuity of other factors |
| Interrupted time series | No co-occurring events; adequate pre-period |
| Synthetic control | Good pre-treatment fit; no spillovers |
| Propensity scores / weighting | No unmeasured confounding; positivity; correct model |
| Sibling / within-person designs | Removes shared confounders but can amplify measurement error and selection |

**Mechanism versus adaptation versus association.** A mechanism explains how; an adaptation claim explains why something evolved (requires evolutionary evidence); an association says only that two things co-vary.

## 6. Generalizability (external validity)

State the population, setting, period, and conditions to which findings apply. Ask whether the study population resembles the target population in ways that modify the effect (age, sex, comorbidity, baseline risk, species, strain, environment, technology version). Explicitly flag extrapolation: from animals to humans, from trial participants to routine care, from one country or era to another, from benchmark datasets to deployment.
