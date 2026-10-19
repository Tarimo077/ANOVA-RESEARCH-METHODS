"""
Practical Application of Analysis of Variance (ANOVA)
Unit: Research Methods
Topic: Analysis of Variance (ANOVA)
Institution: Zetech University
Author: Jeff Tarimo

Open-Source Python Libraries Used:
- SciPy: https://github.com/scipy/scipy
- Statsmodels: https://github.com/statsmodels/statsmodels
- Pandas: https://github.com/pandas-dev/pandas
- NumPy: https://github.com/numpy/numpy
- python-docx: https://github.com/python-openxml/python-docx
"""

import numpy as np
import scipy.stats as stats
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

def run_q1_analysis():
    print("=" * 70)
    print("Q1: ONE-WAY ANOVA PRACTICAL SCENARIO - FULL STATISTICAL OUTPUT")
    print("=" * 70)

    # Dataset
    data = {
        'Method A (Traditional)': [68, 70, 65, 72, 66],
        'Method B (Blended)': [72, 74, 76, 78, 75],
        'Method C (Online)': [75, 78, 80, 82, 79]
    }

    scores = []
    groups = []
    for grp, vals in data.items():
        scores.extend(vals)
        groups.extend([grp] * len(vals))

    df = pd.DataFrame({'score': scores, 'method': groups})

    # Summary Statistics
    print("\n1. DESCRIPTIVE STATISTICS:")
    summary_list = []
    for grp, vals in data.items():
        n = len(vals)
        mean = np.mean(vals)
        var = np.var(vals, ddof=1)
        std = np.std(vals, ddof=1)
        sum_x = np.sum(vals)
        sum_x2 = np.sum(np.array(vals)**2)
        summary_list.append({
            'Group': grp, 'n': n, 'Sum (T)': sum_x, 'Sum of X^2': sum_x2,
            'Mean': round(mean, 2), 'Variance': round(var, 2), 'Std Dev': round(std, 4)
        })
    sum_df = pd.DataFrame(summary_list)
    print(sum_df.to_string(index=False))

    grand_total = np.sum(scores)
    grand_mean = np.mean(scores)
    total_n = len(scores)
    print(f"\nTotal N = {total_n}, Grand Total (G) = {grand_total}, Grand Mean = {grand_mean:.2f}")

    # Manual Sum of Squares Verification
    cf = (grand_total ** 2) / total_n
    ss_total = np.sum(np.array(scores)**2) - cf
    ss_between = sum([((np.sum(vals))**2)/len(vals) for vals in data.values()]) - cf
    ss_within = ss_total - ss_between

    df_between = len(data) - 1
    df_within = total_n - len(data)
    df_total = total_n - 1

    ms_between = ss_between / df_between
    ms_within = ss_within / df_within
    f_stat = ms_between / ms_within
    p_val = 1 - stats.f.cdf(f_stat, df_between, df_within)
    f_crit = stats.f.ppf(0.95, df_between, df_within)

    print("\n2. ANOVA TABLE COMPUTATIONS:")
    print(f"SS Between = {ss_between:.4f}, df = {df_between}, MS Between = {ms_between:.4f}")
    print(f"SS Within  = {ss_within:.4f}, df = {df_within}, MS Within  = {ms_within:.4f}")
    print(f"SS Total   = {ss_total:.4f}, df = {df_total}")
    print(f"F-Statistic = {f_stat:.4f}, Critical F(2, 12, alpha=0.05) = {f_crit:.4f}")
    print(f"p-value = {p_val:.6e}")

    # Statsmodels OLS Model
    model = ols('score ~ C(method)', data=df).fit()
    anova_lm_table = sm.stats.anova_lm(model, typ=1)
    print("\nStatsmodels OLS ANOVA Table:")
    print(anova_lm_table)

    # Effect Size
    eta_sq = ss_between / ss_total
    omega_sq = (ss_between - df_between * ms_within) / (ss_total + ms_within)
    print(f"\nEffect Size:")
    print(f"Eta-squared (eta^2)   = {eta_sq:.4f} ({eta_sq*100:.2f}% of variance explained)")
    print(f"Omega-squared (omega^2) = {omega_sq:.4f} ({omega_sq*100:.2f}% of population variance explained)")

    # Assumption Checks
    print("\n3. ASSUMPTIONS DIAGNOSTICS:")
    print("a) Normality (Shapiro-Wilk Test):")
    for grp, vals in data.items():
        w, p = stats.shapiro(vals)
        print(f"   - {grp}: W = {w:.4f}, p = {p:.4f} -> {'Normal' if p > 0.05 else 'Non-normal'}")
    w_res, p_res = stats.shapiro(model.resid)
    print(f"   - Residuals: W = {w_res:.4f}, p = {p_res:.4f} -> {'Normal' if p_res > 0.05 else 'Non-normal'}")

    print("b) Homogeneity of Variances (Levene Test):")
    w_lev, p_lev = stats.levene(data['Method A (Traditional)'], data['Method B (Blended)'], data['Method C (Online)'], center='median')
    print(f"   - Levene Statistic = {w_lev:.4f}, p = {p_lev:.4f} -> {'Equal variances (Homoscedastic)' if p_lev > 0.05 else 'Unequal variances'}")
    var_ratio = max([np.var(v, ddof=1) for v in data.values()]) / min([np.var(v, ddof=1) for v in data.values()])
    print(f"   - Max Variance / Min Variance Ratio = {var_ratio:.2f} (< 3.0 threshold)")

    # Post-Hoc Test (Tukey HSD)
    print("\n4. POST-HOC TEST (TUKEY HSD at alpha = 0.05):")
    tukey = pairwise_tukeyhsd(endog=df['score'], groups=df['method'], alpha=0.05)
    print(tukey.summary())

def run_q4_analysis():
    print("\n" + "=" * 70)
    print("Q4: INTERPRETATION & DECISION MAKING COMPUTATIONS")
    print("=" * 70)
    df1, df2 = 3, 36
    f_val = 5.27
    p_given = 0.004
    p_exact = 1 - stats.f.cdf(f_val, df1, df2)
    f_crit = stats.f.ppf(0.95, df1, df2)
    eta_sq = (df1 * f_val) / (df1 * f_val + df2)

    # Family-wise error rate for 4 groups: c = 4*3/2 = 6 pairwise tests
    k = 4
    c = k * (k - 1) // 2
    fwer = 1 - (1 - 0.05) ** c

    print(f"Given: F({df1}, {df2}) = {f_val}, reported p = {p_given}")
    print(f"Exact calculated p-value: {p_exact:.5f}")
    print(f"Critical F-value (alpha=0.05): {f_crit:.4f}")
    print(f"Decision: F_calc ({f_val}) > F_crit ({f_crit:.4f}) and p ({p_exact:.5f}) < 0.05 -> Reject H0")
    print(f"Calculated Effect Size (Eta-squared): {eta_sq:.4f} ({eta_sq*100:.2f}% of variance explained)")
    print(f"Number of Pairwise Comparisons: c = {c}")
    print(f"Accumulated Family-Wise Type I Error Rate: {fwer:.4f} ({fwer*100:.2f}%)")

if __name__ == "__main__":
    run_q1_analysis()
    run_q4_analysis()
