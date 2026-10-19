# Analysis of Variance (ANOVA): Practical Application & Empirical Evaluation
**Unit:** Research Methods  
**Institution:** Zetech University  
**Author:** Jeff Tarimo  
**Date:** October 2026  

[![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## Executive Overview

This repository contains the empirical implementation, diagnostic testing, and publication-ready reporting for applied **Analysis of Variance (ANOVA)** in educational and operational research. The study applies both One-Way and Two-Way Factorial ANOVA designs, validates all underlying Gauss-Markov assumptions, derives exact effect sizes ($\eta^2$, $\omega^2$), and conducts multiple comparison post-hoc analyses with Family-Wise Error Rate (FWER) controls.

All statistical modeling and document generation are implemented using standard open-source scientific Python packages.

---

## Open-Source Scientific Python Ecosystem

| Library | GitHub Repository | Primary Functionality in this Study |
| :--- | :--- | :--- |
| **SciPy** | [`https://github.com/scipy/scipy`](https://github.com/scipy/scipy) | One-way ANOVA decomposition (`scipy.stats.f_oneway`), normality testing (`scipy.stats.shapiro`), homoscedasticity testing (`scipy.stats.levene`), and critical F-distribution functions. |
| **Statsmodels** | [`https://github.com/statsmodels/statsmodels`](https://github.com/statsmodels/statsmodels) | Ordinary Least Squares (OLS) regression modeling, ANOVA tables (`anova_lm`), and Tukey's Honestly Significant Difference (`pairwise_tukeyhsd`). |
| **Pandas** | [`https://github.com/pandas-dev/pandas`](https://github.com/pandas-dev/pandas) | Relational data structuring, cohort aggregation, and descriptive summary tables. |
| **NumPy** | [`https://github.com/numpy/numpy`](https://github.com/numpy/numpy) | Vectorized matrix linear algebra and sum-of-squares computations ($SS_{between}, SS_{within}, SS_{total}$). |
| **python-docx** | [`https://github.com/python-openxml/python-docx`](https://github.com/python-openxml/python-docx) | Programmatic compilation of the summarized academic executive report (`.docx`). |

---

## Repository Structure

```text
research methods/
├── anova_research_methods.py                      # Core Python statistical engine (ANOVA, tests, Tukey HSD)
├── generate_anova_assignment_doc.py              # Script compiling the formatted Word report
├── Practical_Application_of_ANOVA_Jeff_Tarimo.docx# Formatted Executive Research Report (Word)
├── README.md                                     # Project documentation & GitHub overview
└── .gitignore                                    # Git ignore configuration
```

---

## Summary of Empirical Findings

### 1. One-Way ANOVA: Instructional Modalities
- **Design:** Three independent cohorts ($n=5$ each) evaluated under Traditional Lectures (A), Blended Learning (B), and Fully Online Learning (C).
- **Diagnostics:** Normality verified across all cohorts via Shapiro-Wilk ($p > 0.05$; Residuals $W = 0.9621, p = 0.7283$). Homoscedasticity confirmed via Levene's test ($W = 0.2090, p = 0.8143$) and variance ratio ($s_{\max}^2 / s_{\min}^2 = 1.64 < 3.0$).
- **Test Result:** $F(2, 12) = 21.74, p = 0.000102 < 0.001$. Null hypothesis rejected.
- **Effect Size:** $\eta^2 = 78.37\%$, adjusted $\omega^2 = 73.44\%$ (very large effect).
- **Tukey HSD Post-Hoc:**
  - Method A vs. B: Mean diff $= +6.80, p = 0.0034$ (Statistically Significant)
  - Method A vs. C: Mean diff $= +10.60, p = 0.0001$ (Statistically Significant)
  - Method B vs. C: Mean diff $= +3.80, p = 0.0893$ (Not Significant at $\alpha = 0.05$)
  - **Takeaway:** Traditional lectures are statistically inferior; blended and online learning achieve comparable high performance.

### 2. Two-Way Factorial ANOVA: Study Method & Gender
- **Design:** $2 \times 2$ factorial evaluating Study Method (Group vs. Individual) and Gender (Male vs. Female).
- **Findings:** Significant Study Method main effect ($p < 0.05$), non-significant Gender main effect ($p > 0.05$), and statistically significant Interaction ($p < 0.05$).
- **Methodological Rule:** Significant interaction supersedes main effects. The efficacy of study method depends on gender; simple main effects and interaction plots are required rather than one-size-fits-all policies.

### 3. Statistical Assumptions & Remedial Framework
- Four core assumptions: Independence, Normality, Homoscedasticity, and Scale of Measurement.
- Normality tested via Shapiro-Wilk and Q-Q plots.
- Homogeneity tested via Levene's test, Bartlett's test, and Hartley's $F_{\max}$ ratio.
- Systematic remedies: Log/Box-Cox transformations, Welch's heteroscedastic ANOVA, Kruskal-Wallis non-parametric test, and permutation/bootstrap resampling.

### 4. Operational Decision Making & Error Rate Control
- **Shift Schedule Study:** $F(3, 36) = 5.27, p = 0.004 < 0.05$. Null hypothesis rejected.
- **Practical Impact:** $\eta^2 = 30.51\%$ of total productivity variance explained by shift assignment.
- **Family-Wise Error Rate (FWER) Protection:** Conducting $c = 6$ pairwise t-tests across 4 shifts inflates Type I error to $\alpha_{FW} = 1 - (1 - 0.05)^6 = 26.49\%$. ANOVA preserves nominal $\alpha = 0.05$ while maximizing power via pooled variance ($df = 36$).

---

## How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tarimojeff/zetech-anova-research-methods.git
   cd "research methods"
   ```

2. **Install requirements:**
   ```bash
   pip install numpy scipy pandas statsmodels python-docx
   ```

3. **Execute statistical calculations:**
   ```bash
   python anova_research_methods.py
   ```

4. **Generate the Word executive report:**
   ```bash
   python generate_anova_assignment_doc.py
   ```

---

## Author
**Jeff Tarimo**  
Zetech University  
Contact: `tarimojeff@gmail.com`
