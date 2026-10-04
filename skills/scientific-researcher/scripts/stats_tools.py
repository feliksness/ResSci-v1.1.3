#!/usr/bin/env python3
"""
stats_tools.py - recompute and sanity-check reported statistics.

Standard library only (Python 3.8+). Every result is computed from the inputs you
supply; nothing is estimated or looked up. Report outputs as "recomputed from the
reported values", and report discrepancies neutrally (typos and rounding are common).

Subcommands
  pcheck    Recompute a p-value from a test statistic (t, F, chi2, z, r) and
            compare it with a reported p-value (statcheck-style consistency check).
  grim      GRIM test: can a mean reported to d decimals arise from n integer scores?
  twobytwo  Risks, risk ratio, odds ratio, risk difference, NNT from a 2x2 table.
  ci2se     Standard error, z and p implied by an estimate and its confidence interval.
  ppv       Predictive values and likelihood ratios from sensitivity, specificity, prevalence.
  smd       Hedges' g (bias-corrected standardized mean difference) with CI.
  meta      Inverse-variance meta-analysis (fixed effect and DerSimonian-Laird random
            effects), heterogeneity, optional Hartung-Knapp-Sidik-Jonkman CI,
            prediction interval, leave-one-out.

Run `python3 stats_tools.py <subcommand> --help` for options.
"""

import argparse
import csv
import math
import re
import sys
from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP

# ---------------------------------------------------------------------------
# Special functions (Numerical Recipes-style implementations)
# ---------------------------------------------------------------------------

_EPS = 3.0e-14
_FPMIN = 1.0e-300
_MAXIT = 10000


def _betacf(a, b, x):
    """Continued fraction for the regularized incomplete beta function (Lentz)."""
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    if abs(d) < _FPMIN:
        d = _FPMIN
    d = 1.0 / d
    h = d
    for m in range(1, _MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < _FPMIN:
            d = _FPMIN
        c = 1.0 + aa / c
        if abs(c) < _FPMIN:
            c = _FPMIN
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < _FPMIN:
            d = _FPMIN
        c = 1.0 + aa / c
        if abs(c) < _FPMIN:
            c = _FPMIN
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < _EPS:
            return h
    raise ArithmeticError("incomplete beta continued fraction did not converge")


def betainc(a, b, x):
    """Regularized incomplete beta I_x(a, b)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    ln_bt = (math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
             + a * math.log(x) + b * math.log1p(-x))
    bt = math.exp(ln_bt)
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def gammaincc(a, x):
    """Regularized upper incomplete gamma Q(a, x)."""
    if x < 0 or a <= 0:
        raise ValueError("invalid arguments to gammaincc")
    if x == 0:
        return 1.0
    gln = math.lgamma(a)
    if x < a + 1.0:
        # series for P(a, x)
        ap, s = a, 1.0 / a
        delta = s
        for _ in range(_MAXIT):
            ap += 1.0
            delta *= x / ap
            s += delta
            if abs(delta) < abs(s) * _EPS:
                break
        p = s * math.exp(-x + a * math.log(x) - gln)
        return 1.0 - p
    # continued fraction for Q(a, x)
    b = x + 1.0 - a
    c = 1.0 / _FPMIN
    d = 1.0 / b
    h = d
    for i in range(1, _MAXIT + 1):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < _FPMIN:
            d = _FPMIN
        c = b + an / c
        if abs(c) < _FPMIN:
            c = _FPMIN
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < _EPS:
            break
    return math.exp(-x + a * math.log(x) - gln) * h


def norm_cdf(z):
    return 0.5 * math.erfc(-z / math.sqrt(2.0))


def norm_sf(z):
    return 0.5 * math.erfc(z / math.sqrt(2.0))


def norm_ppf(p):
    """Inverse standard normal CDF (Acklam's algorithm, refined by one Newton step)."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must be in (0, 1)")
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        x = (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
            ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    elif p <= phigh:
        q = p - 0.5
        r = q * q
        x = (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / \
            (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)
    else:
        q = math.sqrt(-2 * math.log(1 - p))
        x = -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
            ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    # one Newton refinement
    e = norm_cdf(x) - p
    u = e * math.sqrt(2 * math.pi) * math.exp(x * x / 2)
    return x - u / (1 + x * u / 2)


def t_sf(t, df):
    """Upper-tail probability P(T > t) for Student's t."""
    x = df / (df + t * t)
    tail = 0.5 * betainc(df / 2.0, 0.5, x)
    return tail if t >= 0 else 1.0 - tail


def t_ppf(p, df):
    """Quantile of Student's t by bisection on the CDF."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must be in (0, 1)")
    lo, hi = -1e4, 1e4
    for _ in range(300):
        mid = (lo + hi) / 2.0
        if 1.0 - t_sf(mid, df) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def f_sf(f, df1, df2):
    if f <= 0:
        return 1.0
    return betainc(df2 / 2.0, df1 / 2.0, df2 / (df2 + df1 * f))


def chi2_sf(x, df):
    if x <= 0:
        return 1.0
    return gammaincc(df / 2.0, x / 2.0)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fmt(x, digits=4):
    if x is None:
        return "NA"
    if isinstance(x, float):
        if math.isinf(x):
            return "inf" if x > 0 else "-inf"
        if math.isnan(x):
            return "NA"
        if x != 0 and (abs(x) < 1e-4 or abs(x) >= 1e6):
            return f"{x:.{digits}e}"
        return f"{x:.{digits}f}"
    return str(x)


def fmt_p(p):
    if p < 1e-4:
        return f"{p:.2e}"
    return f"{p:.4f}"


def decimals_in(s):
    s = s.strip().lstrip("<>=≤≥ ")
    if "e" in s.lower():
        return None
    return len(s.split(".")[1]) if "." in s else 0


def z_for_level(level):
    return norm_ppf(1 - (1 - level) / 2)


# ---------------------------------------------------------------------------
# pcheck
# ---------------------------------------------------------------------------

def p_from_stat(test, stat, df=None, df2=None, n=None, one_sided=False):
    test = test.lower()
    if test == "z":
        p = 2 * norm_sf(abs(stat))
        return p / 2 if one_sided else p
    if test == "t":
        p = 2 * t_sf(abs(stat), df)
        return p / 2 if one_sided else p
    if test == "r":
        if n is None or n < 3:
            raise ValueError("r requires --n >= 3")
        if abs(stat) >= 1:
            return 0.0
        t = stat * math.sqrt((n - 2) / (1 - stat * stat))
        p = 2 * t_sf(abs(t), n - 2)
        return p / 2 if one_sided else p
    if test == "f":
        return f_sf(stat, df, df2)
    if test == "chi2":
        return chi2_sf(stat, df)
    raise ValueError(f"unknown test {test}")


def cmd_pcheck(args):
    stat = float(args.stat)
    dec = decimals_in(args.stat)
    p = p_from_stat(args.test, stat, args.df, args.df2, args.n, args.one_sided)
    print(f"Test: {'F' if args.test.lower() == 'f' else args.test}  statistic = {args.stat}"
          + (f"  df = {args.df}" if args.df is not None else "")
          + (f", {args.df2}" if args.df2 is not None else "")
          + (f"  n = {args.n}" if args.n is not None else "")
          + ("  (one-sided)" if args.one_sided else "  (two-sided)" if args.test.lower() in ("t", "z", "r") else ""))
    print(f"Recomputed p = {fmt_p(p)}")

    # Range of p compatible with rounding of the reported statistic
    p_lo, p_hi = p, p
    if dec is not None:
        half = 0.5 * 10 ** (-dec)
        cands = []
        for s in (stat - half, stat + half):
            if args.test.lower() in ("f", "chi2") and s <= 0:
                s = 1e-12
            if args.test.lower() == "r":
                s = max(min(s, 0.999999), -0.999999)
            cands.append(p_from_stat(args.test, s, args.df, args.df2, args.n, args.one_sided))
        p_lo, p_hi = min(cands + [p]), max(cands + [p])
        print(f"p range given rounding of the statistic to {dec} decimals: {fmt_p(p_lo)} to {fmt_p(p_hi)}")

    if args.reported_p is None:
        return 0
    rp = args.reported_p.strip()
    alpha = args.alpha
    rp_clean = re.sub(r"^\s*p\s*", "", rp, flags=re.I).replace(" ", "")
    if rp_clean.lower().strip(".") in ("ns", "n.s", "nonsignificant", "non-significant"):
        consistent = p >= alpha or p_hi >= alpha
        verdict = "CONSISTENT" if consistent else f"GROSS INCONSISTENCY (reported non-significant, recomputed p = {fmt_p(p)})"
        print(f"Reported p: {rp}  ->  {verdict}")
        return 0 if consistent else 1
    rp = rp_clean
    try:
        float(rp.lstrip("<>=≤≥"))
    except ValueError:
        print(f"Could not parse reported p '{args.reported_p}'. Use forms like 0.03, '<.001', '=.049', 'ns'.")
        return 2
    if rp.startswith("<") or rp.startswith("≤"):
        bound = float(rp.lstrip("<≤= "))
        consistent = p_lo < bound or math.isclose(p_lo, bound)
        reported_sig = bound <= alpha
    elif rp.startswith(">") or rp.startswith("≥"):
        bound = float(rp.lstrip(">≥= "))
        consistent = p_hi > bound or math.isclose(p_hi, bound)
        reported_sig = False
    else:
        val = float(rp.lstrip("= "))
        rdec = decimals_in(rp)
        half = 0.5 * 10 ** (-rdec) if rdec is not None else 0.0
        consistent = (p_hi >= val - half) and (p_lo <= val + half)
        reported_sig = val < alpha
    recomputed_sig = p < alpha
    if consistent:
        verdict = "CONSISTENT"
    elif reported_sig != recomputed_sig:
        verdict = f"GROSS INCONSISTENCY (significance decision at alpha = {alpha} differs)"
    else:
        verdict = "INCONSISTENT"
    print(f"Reported p: {rp}  ->  {verdict}")
    if not consistent:
        print("Note: check one- vs two-sided testing, df, corrections, and typos before drawing conclusions.")
    return 0 if consistent else 1


# ---------------------------------------------------------------------------
# grim
# ---------------------------------------------------------------------------

def cmd_grim(args):
    mean_s = args.mean.strip()
    dec = decimals_in(mean_s)
    if dec is None:
        print("Provide the mean in plain decimal notation, exactly as reported.")
        return 2
    mean = Decimal(mean_s)
    n, k = args.n, args.items
    if n <= 0 or k <= 0:
        print("--n and --items must be positive integers.")
        return 2
    denom = n * k
    q = Decimal(1).scaleb(-dec)
    print(f"Mean = {mean_s} ({dec} decimals), n = {n}, items = {k}  -> granularity 1/{denom}")
    if denom >= 10 ** dec:
        print("GRIM is uninformative here: n x items >= 10^decimals, so every reported mean is attainable.")
        return 0
    center = int((mean * denom).to_integral_value())
    matches = []
    for s in range(center - 2, center + 3):
        val = Decimal(s) / Decimal(denom)
        for mode in (ROUND_HALF_UP, ROUND_HALF_EVEN):
            if val.quantize(q, rounding=mode) == mean:
                matches.append((s, val))
                break
    if matches:
        s, val = matches[0]
        print(f"CONSISTENT: sum {s} / {denom} = {val:.{dec + 4}f} rounds to {mean_s}")
        return 0
    lo = Decimal(center - 1) / Decimal(denom)
    hi = Decimal(center + 1) / Decimal(denom)
    print(f"INCONSISTENT: no integer total gives {mean_s}. Nearby attainable means: "
          f"{lo:.{dec + 3}f}, {Decimal(center) / Decimal(denom):.{dec + 3}f}, {hi:.{dec + 3}f}")
    print("Possible innocent explanations: typo, missing data changing n, non-integer scale, "
          "or a different n for this variable. Report neutrally.")
    return 1


# ---------------------------------------------------------------------------
# twobytwo
# ---------------------------------------------------------------------------

def wilson(x, n, z):
    """Wilson score interval for a proportion."""
    if n == 0:
        return float("nan"), float("nan")
    p = x / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def newcombe_rd(x1, n1, x0, n0, z):
    """Newcombe hybrid score interval for a difference of independent proportions (method 10)."""
    p1, p0 = x1 / n1, x0 / n0
    l1, u1 = wilson(x1, n1, z)
    l0, u0 = wilson(x0, n0, z)
    rd = p1 - p0
    lower = rd - math.sqrt((p1 - l1) ** 2 + (u0 - p0) ** 2)
    upper = rd + math.sqrt((u1 - p1) ** 2 + (p0 - l0) ** 2)
    return lower, upper


def cmd_twobytwo(args):
    a, b, c, d = args.a, args.b, args.c, args.d
    if min(a, b, c, d) < 0:
        print("Counts must be non-negative.")
        return 2
    n1, n0 = a + b, c + d
    if n1 == 0 or n0 == 0:
        print("Each group needs at least one participant (a+b > 0 and c+d > 0).")
        return 2
    z = z_for_level(args.level)
    pct = int(round(args.level * 100))
    r1, r0 = a / n1, c / n0
    print(f"Exposed/treated:   {a} events / {n1}  risk = {fmt(r1)}")
    print(f"Unexposed/control: {c} events / {n0}  risk = {fmt(r0)}")
    print()

    double_zero = (a == 0 and c == 0) or (b == 0 and d == 0)
    if double_zero:
        print("RR and OR are not estimable: no events (or no non-events) in either group.")
    else:
        aa, bb, cc, dd = a, b, c, d
        corrected = False
        if 0 in (a, b, c, d):
            aa, bb, cc, dd = a + 0.5, b + 0.5, c + 0.5, d + 0.5
            corrected = True
        rr = (aa / (aa + bb)) / (cc / (cc + dd))
        se_lrr = math.sqrt(1 / aa - 1 / (aa + bb) + 1 / cc - 1 / (cc + dd))
        rr_lo, rr_hi = math.exp(math.log(rr) - z * se_lrr), math.exp(math.log(rr) + z * se_lrr)
        p_rr = 2 * norm_sf(abs(math.log(rr) / se_lrr))
        orr = (aa * dd) / (bb * cc)
        se_lor = math.sqrt(1 / aa + 1 / bb + 1 / cc + 1 / dd)
        or_lo, or_hi = math.exp(math.log(orr) - z * se_lor), math.exp(math.log(orr) + z * se_lor)
        print(f"Risk ratio (RR)       = {fmt(rr)}  {pct}% CI {fmt(rr_lo)} to {fmt(rr_hi)}  (p = {fmt_p(p_rr)}, log method)")
        print(f"Odds ratio (OR)       = {fmt(orr)}  {pct}% CI {fmt(or_lo)} to {fmt(or_hi)}  (Woolf)")
        print(f"Relative risk reduction (1 - RR) = {fmt(1 - rr)}")
        if corrected:
            print("  Note: a zero cell was present; 0.5 was added to every cell for RR/OR (Haldane-Anscombe). "
                  "Prefer exact or Bayesian methods for sparse data.")

    rd = r1 - r0
    rd_lo, rd_hi = newcombe_rd(a, n1, c, n0, z)
    print(f"Risk difference (RD = risk exposed - risk unexposed) = {fmt(rd)}  "
          f"{pct}% CI {fmt(rd_lo)} to {fmt(rd_hi)}  (Newcombe hybrid score)")
    if rd < 0:
        print(f"Absolute risk reduction (ARR = control risk - treated risk) = {fmt(-rd)}")
    elif rd > 0:
        print(f"Absolute risk increase (ARI = treated risk - control risk) = {fmt(rd)}")
    if rd != 0:
        nn = 1 / abs(rd)
        beneficial = (rd < 0) != bool(args.outcome_is_good)
        label = "NNT (benefit)" if beneficial else "NNH (harm)"
        print(f"{label} = {fmt(nn, 1)}  (state the follow-up period when reporting)")
        if rd_lo < 0 < rd_hi:
            print("  RD CI includes 0, so the NNT CI is discontinuous (passes through infinity): "
                  f"bounds {fmt(1 / abs(rd_lo), 1)} and {fmt(1 / abs(rd_hi), 1)} lie on opposite sides "
                  "(one benefit, one harm).")
        else:
            print(f"  {pct}% CI: {fmt(1 / max(abs(rd_lo), abs(rd_hi)), 1)} to {fmt(1 / min(abs(rd_lo), abs(rd_hi)), 1)}")
    else:
        print("RD = 0: NNT undefined (infinite).")
    if max(r1, r0) > 0.1 and not double_zero:
        print(f"Note: outcome is common (risk up to {fmt(max(r1, r0), 3)}); the OR overstates the RR. Prefer RR/RD.")
    return 0


# ---------------------------------------------------------------------------
# ci2se
# ---------------------------------------------------------------------------

def cmd_ci2se(args):
    est, lo, hi = args.estimate, args.lower, args.upper
    z = z_for_level(args.level)
    if lo > hi:
        print("Lower bound exceeds upper bound; check the inputs.")
        return 2
    if not lo <= est <= hi:
        print("WARNING: the estimate lies outside its own confidence interval. "
              "This indicates a transcription error or mismatched values; verify against the source.")
    if args.ratio:
        if min(est, lo, hi) <= 0:
            print("Ratio measures must be positive.")
            return 2
        le, ll, lh = math.log(est), math.log(lo), math.log(hi)
        se = (lh - ll) / (2 * z)
        zstat = le / se
        mid = (ll + lh) / 2
        asym = abs(le - mid) / (lh - ll) if lh > ll else 0
        print(f"log(estimate) = {fmt(le)}; SE(log) = {fmt(se)}")
        print(f"z = {fmt(zstat, 3)}; two-sided p = {fmt_p(2 * norm_sf(abs(zstat)))}")
        if asym > 0.05:
            print(f"Warning: estimate is not centred on the log-scale CI (offset {asym:.0%} of CI width). "
                  "Possible rounding, a typo, a non-Wald CI (profile likelihood, exact, bootstrap), "
                  "or a mismatch between estimate and interval.")
    else:
        se = (hi - lo) / (2 * z)
        zstat = est / se
        mid = (lo + hi) / 2
        asym = abs(est - mid) / (hi - lo) if hi > lo else 0
        print(f"SE = {fmt(se)}")
        print(f"z = {fmt(zstat, 3)}; two-sided p = {fmt_p(2 * norm_sf(abs(zstat)))}")
        if asym > 0.05:
            print(f"Warning: estimate is not centred on the CI (offset {asym:.0%} of CI width). "
                  "For ratio measures use --ratio.")
    print("(Assumes a normal-approximation CI; for small samples with t-based CIs the SE is slightly overstated.)")
    return 0


# ---------------------------------------------------------------------------
# ppv
# ---------------------------------------------------------------------------

def cmd_ppv(args):
    se, sp, pr = args.sens, args.spec, args.prev
    for name, v in (("sensitivity", se), ("specificity", sp), ("prevalence", pr)):
        if not 0 <= v <= 1:
            print(f"{name} must be between 0 and 1")
            return 2
    tp, fn = se * pr, (1 - se) * pr
    tn, fp = sp * (1 - pr), (1 - sp) * (1 - pr)
    ppv = tp / (tp + fp) if tp + fp > 0 else float("nan")
    npv = tn / (tn + fn) if tn + fn > 0 else float("nan")
    lrp = se / (1 - sp) if sp < 1 else float("inf")
    lrn = (1 - se) / sp if sp > 0 else float("inf")
    N = args.per
    print(f"Per {N:,} people tested at prevalence {pr:.4g}:")
    print(f"  true positives {tp * N:,.1f}  false positives {fp * N:,.1f}  "
          f"false negatives {fn * N:,.1f}  true negatives {tn * N:,.1f}")
    print(f"PPV = {fmt(ppv)}   NPV = {fmt(npv)}")
    print(f"LR+ = {fmt(lrp, 2)}   LR- = {fmt(lrn, 3)}")
    print("Predictive values apply only at this prevalence and in comparable populations.")
    return 0


# ---------------------------------------------------------------------------
# smd
# ---------------------------------------------------------------------------

def cmd_smd(args):
    m1, s1, n1, m2, s2, n2 = args.m1, args.sd1, args.n1, args.m2, args.sd2, args.n2
    df = n1 + n2 - 2
    sp = math.sqrt(((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / df)
    d = (m1 - m2) / sp
    j = 1 - 3 / (4 * df - 1)
    g = j * d
    var_d = (n1 + n2) / (n1 * n2) + d ** 2 / (2 * (n1 + n2))
    se_g = math.sqrt(j ** 2 * var_d)
    z = z_for_level(args.level)
    pct = int(round(args.level * 100))
    print(f"Pooled SD = {fmt(sp)}; Cohen's d = {fmt(d)}; small-sample correction J = {fmt(j)}")
    print(f"Hedges' g = {fmt(g)}  SE = {fmt(se_g)}  {pct}% CI {fmt(g - z * se_g)} to {fmt(g + z * se_g)}")
    print("Positive g means group 1 mean > group 2 mean. Check that higher scores mean the same "
          "direction (better/worse) across studies before pooling.")
    return 0


# ---------------------------------------------------------------------------
# meta
# ---------------------------------------------------------------------------

def _read_effects(path, ratio, level):
    z = z_for_level(level)
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        cols = {c.strip().lower(): c for c in (reader.fieldnames or [])}
        if "estimate" not in cols:
            raise ValueError("CSV needs columns: study, estimate, and either se or lower+upper")
        has_se = "se" in cols
        has_ci = "lower" in cols and "upper" in cols
        if not (has_se or has_ci):
            raise ValueError("CSV needs an 'se' column or 'lower' and 'upper' columns")
        for i, r in enumerate(reader, 1):
            if not any((v or "").strip() for v in r.values()):
                continue  # blank row
            name = r.get(cols.get("study", ""), f"study {i}") or f"study {i}"
            est = float(r[cols["estimate"]])
            if has_se and r[cols["se"]].strip():
                se = float(r[cols["se"]])  # with --ratio: SE of the log ratio
                y = math.log(est) if ratio else est
            else:
                lo, hi = float(r[cols["lower"]]), float(r[cols["upper"]])
                if ratio:
                    y = math.log(est)
                    se = (math.log(hi) - math.log(lo)) / (2 * z)
                else:
                    y = est
                    se = (hi - lo) / (2 * z)
            if se <= 0:
                raise ValueError(f"non-positive SE for {name}")
            rows.append((name.strip(), y, se))
    return rows


def _pool(rows, level, hksj):
    k = len(rows)
    y = [r[1] for r in rows]
    v = [r[2] ** 2 for r in rows]
    w = [1 / vi for vi in v]
    sw = sum(w)
    fe = sum(wi * yi for wi, yi in zip(w, y)) / sw
    se_fe = math.sqrt(1 / sw)
    q = sum(wi * (yi - fe) ** 2 for wi, yi in zip(w, y))
    dfq = k - 1
    p_q = chi2_sf(q, dfq) if dfq > 0 else float("nan")
    i2 = max(0.0, (q - dfq) / q) if q > 0 else 0.0
    cdl = sw - sum(wi ** 2 for wi in w) / sw
    tau2 = max(0.0, (q - dfq) / cdl) if cdl > 0 else 0.0
    ws = [1 / (vi + tau2) for vi in v]
    sws = sum(ws)
    re = sum(wi * yi for wi, yi in zip(ws, y)) / sws
    se_re = math.sqrt(1 / sws)
    z = z_for_level(level)
    out = {
        "k": k, "fe": fe, "se_fe": se_fe, "fe_ci": (fe - z * se_fe, fe + z * se_fe),
        "p_fe": 2 * norm_sf(abs(fe / se_fe)),
        "Q": q, "df": dfq, "p_Q": p_q, "I2": i2, "tau2": tau2,
        "re": re, "se_re": se_re, "re_ci": (re - z * se_re, re + z * se_re),
        "p_re": 2 * norm_sf(abs(re / se_re)), "weights_re": [wi / sws for wi in ws],
    }
    if hksj and k >= 2:
        qhk = sum(wi * (yi - re) ** 2 for wi, yi in zip(ws, y)) / (k - 1)
        se_hk = math.sqrt(qhk / sws)
        tcrit = t_ppf(1 - (1 - level) / 2, k - 1)
        out["hksj_ci"] = (re - tcrit * se_hk, re + tcrit * se_hk)
        out["hksj_se"] = se_hk
        out["p_hksj"] = 2 * t_sf(abs(re / se_hk), k - 1) if se_hk > 0 else float("nan")
    if k >= 3:
        tcrit = t_ppf(1 - (1 - level) / 2, k - 2)
        half = tcrit * math.sqrt(tau2 + se_re ** 2)
        out["pi"] = (re - half, re + half)
    return out


def cmd_meta(args):
    try:
        rows = _read_effects(args.csv, args.ratio, args.level)
    except (OSError, ValueError, KeyError) as e:
        print(f"Error reading CSV: {e}")
        return 2
    if len(rows) < 2:
        print("Need at least two studies.")
        return 2
    tr = (lambda x: math.exp(x)) if args.ratio else (lambda x: x)
    pct = int(round(args.level * 100))
    res = _pool(rows, args.level, args.hksj)
    scale = "ratio (pooled on log scale, back-transformed)" if args.ratio else "difference / untransformed"
    print(f"Inverse-variance meta-analysis, k = {res['k']} studies; scale: {scale}")
    print()
    print(f"{'Study':30s} {'Estimate':>10s} {'SE(' + ('log' if args.ratio else 'y') + ')':>10s} {'RE weight':>10s}")
    for (name, y, se), wt in zip(rows, res["weights_re"]):
        print(f"{name[:30]:30s} {fmt(tr(y)):>10s} {fmt(se):>10s} {wt:>9.1%}")
    print()
    lo, hi = res["fe_ci"]
    print(f"Fixed effect:     {fmt(tr(res['fe']))}  {pct}% CI {fmt(tr(lo))} to {fmt(tr(hi))}  p = {fmt_p(res['p_fe'])}")
    lo, hi = res["re_ci"]
    print(f"Random effects (DerSimonian-Laird): {fmt(tr(res['re']))}  {pct}% CI {fmt(tr(lo))} to {fmt(tr(hi))}  "
          f"p = {fmt_p(res['p_re'])}")
    if "hksj_ci" in res:
        lo, hi = res["hksj_ci"]
        print(f"  with HKSJ adjustment: {pct}% CI {fmt(tr(lo))} to {fmt(tr(hi))}  p = {fmt_p(res['p_hksj'])}")
    print(f"Heterogeneity: Q = {fmt(res['Q'], 3)} (df = {res['df']}, p = {fmt_p(res['p_Q'])}); "
          f"I^2 = {res['I2']:.1%}; tau^2 = {fmt(res['tau2'])}" + (" (log scale)" if args.ratio else ""))
    if "pi" in res:
        lo, hi = res["pi"]
        print(f"{pct}% prediction interval: {fmt(tr(lo))} to {fmt(tr(hi))}")
    print()
    warnings = []
    if res["k"] < 5:
        warnings.append("Few studies: tau^2 and I^2 are very imprecise; DerSimonian-Laird CIs may be too narrow "
                        "(HKSJ is reported with --hksj).")
    if res["k"] < 10:
        warnings.append("Fewer than 10 studies: funnel-plot asymmetry tests are not informative.")
    warnings.append("Pooling is only meaningful if studies address a sufficiently similar question and are "
                    "independent. Rate certainty (e.g., GRADE) before interpreting.")
    for wmsg in warnings:
        print("Note: " + wmsg)

    if args.loo and res["k"] < 3:
        print()
        print("Leave-one-out skipped: needs at least 3 studies.")
    if args.loo and res["k"] >= 3:
        print()
        print("Leave-one-out (random effects, DerSimonian-Laird):")
        for i, (name, _, _) in enumerate(rows):
            sub = _pool(rows[:i] + rows[i + 1:], args.level, False)
            lo, hi = sub["re_ci"]
            print(f"  without {name[:28]:28s} {fmt(tr(sub['re']))}  ({fmt(tr(lo))} to {fmt(tr(hi))})  I^2 = {sub['I2']:.0%}")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("pcheck", help="recompute p from a test statistic and compare with reported p")
    s.add_argument("--test", required=True, choices=["t", "F", "f", "chi2", "z", "r"])
    s.add_argument("--stat", required=True, help="test statistic exactly as reported (keeps decimals)")
    s.add_argument("--df", type=float, help="degrees of freedom (t, chi2) or numerator df (F)")
    s.add_argument("--df2", type=float, help="denominator df (F)")
    s.add_argument("--n", type=int, help="sample size (for r)")
    s.add_argument("--reported-p", help="reported p, e.g. 0.03, '<.001', '=0.049'")
    s.add_argument("--one-sided", action="store_true", help="one-sided test (t, z, r only)")
    s.add_argument("--alpha", type=float, default=0.05)
    s.set_defaults(func=cmd_pcheck)

    s = sub.add_parser("grim", help="GRIM consistency test for means of integer data")
    s.add_argument("--mean", required=True, help="mean exactly as reported, e.g. 3.47")
    s.add_argument("--n", type=int, required=True, help="number of participants")
    s.add_argument("--items", type=int, default=1, help="number of integer items averaged (default 1)")
    s.set_defaults(func=cmd_grim)

    s = sub.add_parser("twobytwo", help="RR, OR, RD, NNT from a 2x2 table")
    s.add_argument("--a", type=int, required=True, help="events in exposed/treated")
    s.add_argument("--b", type=int, required=True, help="non-events in exposed/treated")
    s.add_argument("--c", type=int, required=True, help="events in unexposed/control")
    s.add_argument("--d", type=int, required=True, help="non-events in unexposed/control")
    s.add_argument("--level", type=float, default=0.95)
    s.add_argument("--outcome-is-good", action="store_true",
                   help="the event is desirable (e.g. recovery), so a positive RD is benefit")
    s.set_defaults(func=cmd_twobytwo)

    s = sub.add_parser("ci2se", help="SE, z, p implied by an estimate and CI")
    s.add_argument("--estimate", type=float, required=True)
    s.add_argument("--lower", type=float, required=True)
    s.add_argument("--upper", type=float, required=True)
    s.add_argument("--ratio", action="store_true", help="ratio measure (OR, RR, HR): work on log scale")
    s.add_argument("--level", type=float, default=0.95)
    s.set_defaults(func=cmd_ci2se)

    s = sub.add_parser("ppv", help="PPV/NPV/likelihood ratios")
    s.add_argument("--sens", type=float, required=True)
    s.add_argument("--spec", type=float, required=True)
    s.add_argument("--prev", type=float, required=True)
    s.add_argument("--per", type=int, default=10000, help="population size for natural frequencies")
    s.set_defaults(func=cmd_ppv)

    s = sub.add_parser("smd", help="Hedges' g from two groups' means, SDs, ns")
    for name in ("m1", "sd1", "m2", "sd2"):
        s.add_argument(f"--{name}", type=float, required=True)
    s.add_argument("--n1", type=int, required=True)
    s.add_argument("--n2", type=int, required=True)
    s.add_argument("--level", type=float, default=0.95)
    s.set_defaults(func=cmd_smd)

    s = sub.add_parser("meta", help="inverse-variance meta-analysis from a CSV")
    s.add_argument("--csv", required=True,
                   help="CSV with columns study,estimate,se  or  study,estimate,lower,upper. "
                        "With --ratio, estimate/lower/upper are ratios and 'se' is the SE of the log ratio.")
    s.add_argument("--ratio", action="store_true", help="ratio measures (pool on log scale)")
    s.add_argument("--level", type=float, default=0.95)
    s.add_argument("--hksj", action="store_true", help="also report Hartung-Knapp-Sidik-Jonkman CI")
    s.add_argument("--loo", action="store_true", help="leave-one-out sensitivity analysis")
    s.set_defaults(func=cmd_meta)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    if getattr(args, "test", None) == "F":
        args.test = "f"
    if args.cmd == "pcheck":
        t = args.test.lower()
        if t in ("t", "chi2") and args.df is None:
            print("--df is required for t and chi2")
            return 2
        if t == "f" and (args.df is None or args.df2 is None):
            print("--df and --df2 are required for F")
            return 2
        if t == "r" and args.n is None:
            print("--n is required for r")
            return 2
        if args.one_sided and t in ("f", "chi2"):
            print("--one-sided applies only to t, z, r")
            return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
