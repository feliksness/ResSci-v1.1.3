# Field-Specific Methods

Evidence standards, common pitfalls, and sources by discipline. Read only the sections relevant to the task.

## Contents
1. Where to search
2. Medicine and public health
3. Biology and life sciences
4. Neuroscience and psychology
5. Chemistry and materials science
6. Physics
7. Astronomy and astrophysics
8. Earth, environmental, and climate science (including geology)
9. Mathematics
10. Computer science and machine learning
11. Engineering
12. Social sciences
13. General experimental science
14. History of science
15. Interdisciplinary research

---

## 1. Where to search

Pick sources suited to the field; no single database covers everything. Note which ones you could actually access.

| Field | Primary sources | Also useful |
|---|---|---|
| Biomedicine, health | PubMed/MEDLINE, PubMed Central, Europe PMC, Cochrane Library | Embase, CINAHL (subscriptions); ClinicalTrials.gov, WHO ICTRP; medRxiv; guideline bodies (WHO, NICE, CDC, specialty societies); regulatory documents (FDA, EMA) |
| Life sciences | PubMed, Europe PMC, bioRxiv | Domain databases (GenBank, UniProt, PDB, model-organism databases) |
| Psychology | PubMed, PsycINFO (subscription), PsyArXiv | OSF registries, replication project reports |
| Chemistry, materials | Crossref, publisher databases, ChemRxiv | SciFinder/Reaxys (subscriptions), PubChem, Materials Project, NIST databases |
| Physics, astronomy | arXiv, NASA ADS | INSPIRE-HEP (particle physics), collaboration publications, NIST/CODATA constants |
| Earth, climate | Crossref, publisher databases, ESSOAr/ESS Open Archive | IPCC assessment reports, NOAA, NASA, Copernicus/ECMWF, USGS, national geological surveys |
| Mathematics | arXiv (math), zbMATH Open | MathSciNet (subscription), formal proof libraries |
| Computer science | arXiv (cs), DBLP, ACL Anthology, OpenReview, ACM DL, IEEE Xplore | Public leaderboards (verify against the papers; note the date), code repositories |
| Engineering | IEEE Xplore, ASCE/ASME libraries, Crossref | Standards bodies (ISO, ASTM, IEC), government technical reports |
| Social sciences, economics | SSRN, RePEc/IDEAS, NBER working papers, SocArXiv | Official statistics agencies, World Bank/OECD data, registered reports |
| Cross-disciplinary | Crossref, OpenAlex, Semantic Scholar, Google Scholar, CORE, BASE | Web of Science, Scopus (subscriptions); institutional repositories |

Use general web search to discover, then go to the authoritative record.

## 2. Medicine and public health

Apply the strictest standards: errors here cause direct harm.
- Separate the evidence ladder explicitly: laboratory → animal → observational human → randomized trial → systematic review → clinical guideline. State which rung supports each claim.
- Distinguish **efficacy** (ideal conditions), **effectiveness** (routine practice), **safety** (harms, including rare and long-term), **association**, and **clinical significance** (minimal clinically important difference).
- Use patient-important outcomes over surrogate endpoints; flag when a claim rests on a surrogate (e.g., biomarker change rather than mortality).
- Report absolute risks and NNT/NNH alongside relative effects.
- Check trial registration and compare registered with reported outcomes.
- A small positive study does not establish that an intervention is safe or effective.
- Do not turn preliminary findings into recommendations. When describing recommendations, quote the guideline body, its date, and its strength-of-recommendation grading. Do not give individual diagnostic or treatment advice; suggest consulting a clinician for personal decisions.
- Reporting guidelines: CONSORT (trials), STROBE (observational), STARD (diagnostic), TRIPOD (prediction models, including the AI extension), CARE (case reports), PRISMA (reviews), SPIRIT (trial protocols), CHEERS (economic evaluations).

## 3. Biology and life sciences

- Distinguish species-specific findings from general principles; name the model organism, strain, sex, age, and conditions.
- Distinguish in vitro, ex vivo, in vivo (animal), and human evidence. Results in model organisms do not automatically generalize to humans; most promising animal findings do not translate.
- Check cell-line authentication concerns and known misidentified lines when cell work is central.
- Separate genetic from environmental explanations; heritability estimates are population- and environment-specific and do not describe individuals.
- Separate proximate mechanism from ultimate (evolutionary) explanation; adaptation claims need evolutionary evidence, not just a plausible story.
- Avoid anthropomorphic language unless it is a standard technical term.
- Omics studies: check multiple-testing control, replication cohorts, batch effects, and population stratification.
- Reporting guideline for animal research: ARRIVE.

## 4. Neuroscience and psychology

- Be alert to the replication record: many classic effects have failed large-scale replication. Search for replication attempts and registered reports.
- Small samples and flexible analyses are common; check pre-registration and power.
- Neuroimaging: beware reverse inference (activation of region X does not imply process Y), circular analysis ("double dipping"), and uncorrected multiple comparisons.
- Self-report measures: check validity and reliability in the population studied.
- WEIRD samples (Western, educated, industrialized, rich, democratic) limit generalizability.
- Distinguish statistical from clinical significance in mental health outcomes.

## 5. Chemistry and materials science

- Verify chemical names (IUPAC and common), molecular formulas, CAS numbers when cited, and units.
- Record reaction conditions (solvent, temperature, pressure, catalyst loading, time, atmosphere) when reporting results; yields depend on them.
- Distinguish observed from proposed mechanisms; computational (e.g., DFT) predictions from experimental confirmation.
- Material properties are conditional (temperature, humidity, processing, measurement protocol); do not present them as universal constants.
- Check characterization evidence (spectra, diffraction, microscopy) supports identity and purity claims.
- Device performance claims (batteries, solar cells, catalysts) require standardized protocols; compare like with like and note certified versus self-reported values.
- Never invent yields, spectra, reaction mechanisms, or property values.

## 6. Physics

- Report measurement uncertainty (statistical and systematic separately where given).
- Distinguish theory, phenomenological model, simulation, and measurement.
- Check dimensional consistency and units in every equation you write.
- Particle and nuclear physics: note significance conventions (e.g., the 5σ discovery threshold) and look-elsewhere effects.
- Distinguish confirmed results from anomalies awaiting independent confirmation.
- Use authoritative constants (CODATA via NIST).

## 7. Astronomy and astrophysics

- Separate direct observation, derived quantity (which depends on models, e.g., distance ladders, mass estimates), and interpretation.
- State instrument, survey, data release, and calibration where relevant.
- Note selection effects (e.g., detection biases in exoplanet surveys) and small-number statistics.
- Distinguish candidates from confirmed detections (exoplanets, transients, biosignature claims).
- Model-dependent cosmological parameters should be reported with the model and dataset combination used; note tensions between methods rather than picking one.

## 8. Earth, environmental, and climate science (including geology)

- Distinguish observations, reanalyses, model simulations, and projections. Never present model projections as observations.
- Projections depend on scenarios; name the scenario and model ensemble, and report ranges.
- State dataset provenance, version, spatial and temporal resolution, and known biases.
- Consider spatial and temporal scale; local findings may not generalize regionally or globally.
- Separate correlation from physical causation; detection and attribution studies have specific methods.
- Geology and paleoclimate: dating methods carry uncertainties; proxy records require calibration and have resolution limits.
- For climate assessments, IPCC reports use calibrated uncertainty language ("likely," "very likely") with defined probability ranges; preserve that language exactly when citing.

## 9. Mathematics

- Verify definitions and notation; different sources use different conventions.
- State assumptions explicitly; check whether each step uses them.
- Distinguish theorem, lemma, conjecture, proof, proof sketch, and heuristic argument. Do not call an argument a proof unless every step is justified.
- Check derivations step by step; test special cases, boundary cases, small examples, and limiting behavior; check dimensions in applied contexts.
- Independently re-derive important results when possible; use computation (symbolic or numeric) to test identities and catch errors, while remembering that numerical checks are not proofs.
- Cite the source of a theorem; for famous results note who proved it and when, and whether a proof has been formally verified or remains disputed.

## 10. Computer science and machine learning

- Identify the algorithm, architecture, dataset (version and split), preprocessing, hyperparameters, compute budget, and number of runs/seeds.
- Check for train–test leakage (duplicates across splits, temporal leakage, preprocessing fit on full data, benchmark contamination of pretraining data).
- Distinguish benchmark results from real-world performance; distinguish in-distribution from out-of-distribution evaluation.
- Report variance across seeds; single-run differences of a fraction of a point are often noise.
- Check baselines are fairly tuned and compared under the same compute.
- Note whether code, data, and weights are available; reproducibility claims require them.
- Never invent benchmark numbers or leaderboard positions; leaderboards change quickly, so give dates.
- Never imply code was run if it was not. When you run code, report environment and versions.

## 11. Engineering

- Distinguish laboratory tests, field tests, simulations, and design calculations.
- Cite the applicable standard and its version when compliance or test methods matter.
- Report safety factors, tolerances, and operating conditions; performance outside tested conditions is extrapolation.
- Failure analyses: separate the observed failure mode from the inferred root cause.

## 12. Social sciences

- Identify the unit of analysis and the population; beware ecological inference.
- Causal claims need credible identification strategies (see `study-designs.md` §5).
- Survey research: sampling frame, response rate, weighting, question wording, mode effects.
- Qualitative research is evaluated on credibility, transferability, dependability, and reflexivity rather than statistical generalization.
- Context and time matter: findings may not transfer across countries, institutions, or decades.
- Check working papers for later published versions with changed results.

## 13. General experimental science

Distinguish observed measurement, interpretation, hypothesis, and mechanism. Check:
- controls (positive, negative, vehicle/sham);
- replicates (biological versus technical; pseudo-replication);
- randomization and blinding of allocation and assessment;
- sample size justification;
- calibration and measurement uncertainty;
- reproducibility across labs;
- artifacts, contamination, and laboratory conditions;
- whether the mechanism was tested or inferred from correlation.

## 14. History of science

- Verify dates and original publications; quote originals where possible, distinguishing quotation from paraphrase and translation.
- Distinguish what was believed at the time from current evidence; avoid "whig history" (reading the past as a march to the present).
- Do not attribute a modern concept to a historical scientist without textual evidence.
- Priority disputes and famous anecdotes (apples, eureka moments) are often embellished; check historical scholarship.

## 15. Interdisciplinary research

- Define each technical term per field when meanings differ (e.g., "significance," "model," "bias," "validity," "stress").
- Apply each field's own evidence standards to its claims; do not assume they are interchangeable.
- Identify where fields disagree and why (different methods, assumptions, data).
- Distinguish genuine methodological compatibility from superficial terminology overlap.
- When combining findings across fields, state the weakest link in the inferential chain.
