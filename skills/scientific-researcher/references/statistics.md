# Statistical Reasoning

Correct interpretation of common statistics, frequent misreadings, checks you can run, and meta-analysis rules.

## Contents
1. Ground rules
2. Descriptive statistics
3. Uncertainty: SE, CI, and intervals
4. P-values and significance
5. Effect measures: relative and absolute
6. Diagnostic and screening accuracy
7. Correlation and regression
8. Power, sample size, and multiplicity
9. Bayesian inference
10. Red flags in reported statistics
11. Recomputation with `stats_tools.py`
12. Meta-analysis
13. Reporting numbers in prose

---

## 1. Ground rules

- Never report a number you did not read in a source or compute in-session.
- Never claim a test, model, or analysis was run unless it was. If you computed something, say how (software, method, inputs).
- Statistical significance is not practical significance, and non-significance is not evidence of no effect.
- Report magnitude and uncertainty together: effect estimate, confidence (or credible) interval, and, where relevant, absolute effect.
- Check units, denominators, and time frames before comparing numbers across studies.

## 2. Descriptive statistics

| Statistic | Use | Watch for |
|---|---|---|
| Mean | Symmetric distributions | Skewed data (costs, lengths of stay, income) where mean ≫ median |
| Median (IQR) | Skewed data, ordinal data | Cannot be pooled like means without assumptions |
| Variance / SD | Spread of individual observations | SD versus SE confusion |
| Range | Extremes | Sensitive to outliers and sample size |
| Proportion | Binary outcomes | Denominator: per enrolled, per analyzed, per person-time? |
| Rate | Events per person-time | Different time units across studies |

## 3. Uncertainty: SE, CI, and intervals

- **SD** describes variability of individuals; **SE** describes uncertainty of an estimate (SE = SD/√n for a mean). Error bars must state which.
- **95% confidence interval:** a procedure that, over repeated samples, captures the true parameter 95% of the time. It is *not* a 95% probability that this specific interval contains the true value (that is a Bayesian credible-interval statement).
- Overlapping 95% CIs do not imply a non-significant difference. Non-overlapping 95% CIs for two independent estimates do imply p < 0.05 for the difference (about p < 0.006 when the two SEs are similar). Test the difference directly rather than eyeballing intervals.
- A wide CI spanning both meaningful benefit and meaningful harm means the study is inconclusive, not "no effect."
- **Prediction interval** (meta-analysis): the range in which the effect in a new setting is expected to fall; often much wider than the CI of the pooled mean.
- For ratio measures, CIs are symmetric on the log scale; SE(log ratio) ≈ (ln(upper) − ln(lower)) / (2 × 1.96).

## 4. P-values and significance

- A p-value is the probability of data at least as extreme as observed, *assuming the null hypothesis and all model assumptions are true*.
- It is **not** the probability that the null hypothesis is true, the probability that the result is due to chance, or a measure of effect size or importance.
- p = 0.049 and p = 0.051 are practically identical evidence. Avoid binary "significant/not significant" storytelling; report estimates and intervals.
- Large samples make trivial effects "significant"; small samples make important effects "non-significant."
- Statements from statisticians' bodies (e.g., the American Statistical Association's statement on p-values) caution against using p < 0.05 as a sole criterion; follow that spirit.

## 5. Effect measures: relative and absolute

From a 2×2 table (exposed: a events, b non-events; unexposed: c events, d non-events):

| Measure | Formula | Interpretation |
|---|---|---|
| Risk in exposed / unexposed | a/(a+b), c/(c+d) | Absolute risks |
| Risk ratio (RR) | [a/(a+b)] / [c/(c+d)] | Relative change in risk |
| Odds ratio (OR) | (a·d)/(b·c) | Ratio of odds; approximates RR only when the outcome is rare (roughly < 10%) |
| Risk difference (RD) | a/(a+b) − c/(c+d) | Absolute change; what matters for individuals and policy |
| Absolute risk reduction (ARR) | control risk − treated risk (= −RD when the treated group is "exposed") | Positive when treatment lowers risk |
| NNT / NNH | 1/|RD| | Number treated for one additional benefit or harm; state time frame. If the RD CI crosses 0, the NNT CI passes through infinity |
| Hazard ratio (HR) | From survival models | Ratio of instantaneous event rates; assumes proportional hazards; not a risk ratio |
| Relative risk reduction | 1 − RR | Sounds large even when absolute benefit is tiny |

Rules:
- Pair relative effects with absolute effects and baseline risk wherever possible ("a 50% relative reduction, from 2 to 1 per 1,000 over 5 years").
- Do not interpret an OR as an RR when the outcome is common; the OR exaggerates the RR. Conversions using baseline risk are approximations.
- Hazard ratios do not translate directly into "X% less likely to die"; they describe rates over follow-up.
- Standardized mean differences (Cohen's d, Hedges' g) are unit-free; convey what they mean on the original scale when possible. Conventional "small/medium/large" thresholds are field-dependent rules of thumb.

## 6. Diagnostic and screening accuracy

- **Sensitivity** = TP/(TP+FN); **specificity** = TN/(TN+FP): properties of the test in a population and setting.
- **PPV** and **NPV** depend strongly on prevalence. A test with 99% sensitivity and 99% specificity has a PPV of only about 50% at 1% prevalence. Always state prevalence when interpreting predictive values (base-rate neglect is a common error).
- **Likelihood ratios** combine sensitivity and specificity; they convert pre-test odds to post-test odds.
- **ROC / AUC** summarize discrimination across thresholds; AUC says nothing about calibration or clinical utility at a chosen threshold.
- Accuracy estimates from case-control-type diagnostic studies (severe cases versus healthy controls) are usually inflated (spectrum bias).

## 7. Correlation and regression

- Pearson r measures linear association; Spearman ρ measures monotonic association. Neither implies causation; r² is the share of variance explained in that sample.
- Regression coefficients are conditional associations given the model; their causal reading depends on the adjustment set being correct (see `study-designs.md` §5).
- Adjusting for mediators or colliders can bias estimates. More covariates is not automatically better.
- Watch for overfitting (many predictors, few events), extrapolation beyond the data range, multicollinearity, and unreported model selection.
- Regression to the mean can create apparent improvements in groups selected for extreme values.
- Ecological correlations do not license individual-level conclusions.

## 8. Power, sample size, and multiplicity

- Underpowered studies produce imprecise estimates, and the significant ones tend to overestimate effect sizes (the "winner's curse").
- Post hoc power calculated from the observed effect adds nothing beyond the p-value; interpret the CI instead.
- **Multiple comparisons:** testing many outcomes, subgroups, time points, or models inflates false positives. Check for correction (Bonferroni, Holm, false discovery rate) or pre-registration. Treat unplanned subgroup findings as hypothesis-generating; check for a formal test of interaction.
- **Heterogeneity of treatment effects:** a significant effect in one subgroup and a non-significant effect in another is not evidence that the subgroups differ.

## 9. Bayesian inference

- Posterior ∝ likelihood × prior. Report the prior, its justification, and sensitivity to alternative priors.
- A 95% credible interval does support the statement "95% probability the parameter lies in this interval, given the model and prior."
- Bayes factors compare models; they depend on the priors on parameters under each model.
- Do not mix Bayesian and frequentist interpretations in the same sentence.

## 10. Red flags in reported statistics

- p-values clustered just below 0.05; many tests with only significant ones reported.
- Means inconsistent with integer data and sample size (GRIM failures); SDs impossible for the scale (GRIMMER/SPRITE-type checks).
- Test statistic, degrees of freedom, and p-value that do not agree.
- Percentages that do not match the counts or denominators.
- Effect sizes implausibly large for the field (for example, a single brief intervention with a huge effect on a complex behavior).
- Baseline tables in randomized trials with too-similar or too-different groups.
- Outcome switching relative to registration or protocol.
- Primary outcome not reported, or reported only in a subgroup.
- Relative effects reported without absolute risks.

These are reasons to scrutinize and to say "the reported statistics appear internally inconsistent," not grounds to allege misconduct (see `research-integrity.md`).

## 11. Recomputation with `stats_tools.py`

Standard library only. Examples:

```bash
# Does a reported t(28) = 2.10, p = .03 hold up?
python3 scripts/stats_tools.py pcheck --test t --stat 2.10 --df 28 --reported-p 0.03

# Is a mean of 3.47 possible with n = 21 integer responses (one item)?
python3 scripts/stats_tools.py grim --mean 3.47 --n 21

# Relative and absolute effects from a 2x2 table (RD CI by Newcombe's hybrid score method)
python3 scripts/stats_tools.py twobytwo --a 15 --b 85 --c 30 --d 70

# SE and p-value implied by a ratio estimate with 95% CI
python3 scripts/stats_tools.py ci2se --estimate 0.75 --lower 0.60 --upper 0.94 --ratio

# Predictive values at a given prevalence
python3 scripts/stats_tools.py ppv --sens 0.99 --spec 0.99 --prev 0.01

# Hedges' g from group summaries
python3 scripts/stats_tools.py smd --m1 10.2 --sd1 3.1 --n1 40 --m2 8.9 --sd2 3.4 --n2 42

# Inverse-variance meta-analysis from a CSV (study,estimate,se  or  study,estimate,lower,upper)
python3 scripts/stats_tools.py meta --csv effects.csv --ratio --hksj
```

Report recomputed values as "recomputed by us from the reported statistics," and report discrepancies neutrally.

## 12. Meta-analysis

Summarizing studies narratively is not a meta-analysis. Perform quantitative pooling only when:
- the studies address a sufficiently similar question (population, intervention/exposure, comparator, outcome);
- effect estimates and their uncertainty are actually available (extracted, not guessed) on a common metric;
- the studies are independent (or dependence is modeled);
- pooling makes scientific sense given heterogeneity and risk of bias.

When pooling:
- **Effect measure:** choose RR, OR, RD, HR, MD, or SMD appropriate to the outcome; pool ratio measures on the log scale.
- **Model:** fixed-effect assumes one true effect; random-effects assumes a distribution of true effects. Random-effects is usually more defensible across diverse studies, but DerSimonian–Laird underestimates uncertainty when studies are few; consider the Hartung–Knapp–Sidik–Jonkman adjustment or REML-based methods.
- **Heterogeneity:** report Cochran's Q, I² (with caution: I² is not an absolute measure and is imprecise with few studies), τ², and a prediction interval.
- **Sensitivity analyses:** leave-one-out, excluding high risk-of-bias studies, alternative models.
- **Subgroups and meta-regression:** pre-specify; observational across studies; beware ecological bias and few studies per covariate.
- **Small-study effects / publication bias:** funnel plots and tests (e.g., Egger's) need roughly 10 or more studies and are not definitive; asymmetry has causes other than publication bias.
- **Certainty:** rate the pooled result with GRADE or an equivalent.

Never fabricate a pooled estimate, a forest plot, heterogeneity statistics, or a funnel plot. If data are insufficient, do a structured narrative synthesis (e.g., following the SWiM guideline) and say why pooling was not done.

## 13. Reporting numbers in prose

- Give the estimate, interval, and units: "mean difference −3.1 mmHg (95% CI −4.5 to −1.7)."
- State the comparison and time frame.
- Do not report more decimal places than the data justify (false precision).
- When quoting a number from a source, keep the source's precision; do not round in a direction that strengthens the claim.
