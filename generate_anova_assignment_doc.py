"""
Generate the concise, professional academic ANOVA Research Report in Word format.
All question statements and task prompts have been removed and summarized.
Output Target: Practical_Application_of_ANOVA_Jeff_Tarimo.docx (same folder as script)
"""

import os
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(SCRIPT_DIR, "Practical_Application_of_ANOVA_Jeff_Tarimo.docx")
FONT = "Times New Roman"

doc = Document()

# Base margins
for section in doc.sections:
    section.top_margin = section.bottom_margin = Inches(1)
    section.left_margin = section.right_margin = Inches(1)

# Normal style
normal = doc.styles["Normal"]
normal.font.name = FONT
normal.font.size = Pt(11.5)
normal.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
normal.paragraph_format.line_spacing = 1.35
normal.paragraph_format.space_after = Pt(4)

# Headings
for name, size in (("Heading 1", 13.5), ("Heading 2", 12), ("Heading 3", 11.5)):
    st = doc.styles[name]
    st.font.name = FONT
    st.font.size = Pt(size)
    st.font.bold = True
    st.font.color.rgb = RGBColor(15, 32, 67) # Deep academic navy
    st.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    rfonts = st.element.rPr.rFonts
    rfonts.set(qn("w:ascii"), FONT)
    rfonts.set(qn("w:hAnsi"), FONT)
    st.paragraph_format.space_before = Pt(10 if name == "Heading 1" else 6)
    st.paragraph_format.space_after = Pt(3)
    st.paragraph_format.line_spacing = 1.15
    st.paragraph_format.keep_with_next = True
doc.styles["Heading 3"].font.italic = True


# Helpers
def para(text, bold_lead=None, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    p.alignment = align
    if bold_lead:
        p.add_run(bold_lead).bold = True
    p.add_run(text)
    return p


def bullets(items):
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(2)
        if isinstance(item, tuple):
            p.add_run(item[0]).bold = True
            p.add_run(item[1])
        else:
            p.add_run(item)


def box(title, text, bg="F4F6F7", border_color="BDC3C7"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.style = "Table Grid"
    cell = tbl.rows[0].cells[0]
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), bg)
    cell._tc.get_or_add_tcPr().append(shd)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(2)
    if title:
        p.add_run(f"{title}: ").bold = True
    p.add_run(text)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def table(headers, rows, widths=None):
    tbl = doc.add_table(rows=1, cols=len(headers))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        c = tbl.rows[0].cells[i]
        c.text = ""
        r = c.paragraphs[0].add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), "EAECEE")
        c._tc.get_or_add_tcPr().append(shd)
    for row in rows:
        cells = tbl.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            r = cells[i].paragraphs[0].add_run(str(val))
            r.font.size = Pt(9.5)
    for row in tbl.rows:
        for i, c in enumerate(row.cells):
            for p in c.paragraphs:
                p.paragraph_format.line_spacing = 1.05
                p.paragraph_format.space_after = Pt(1.5)
            if widths:
                c.width = Inches(widths[i])
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return tbl


def add_page_number_footer(section):
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    for tag, text in (("begin", None), (None, "PAGE"), ("end", None)):
        if tag:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), tag)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = text
        run._r.append(el)


# ================================================================ COVER PAGE
for _ in range(2):
    doc.add_paragraph()

for line, size in (("ZETECH UNIVERSITY", 18), ("DEPARTMENT OF BUSINESS AND SOCIAL SCIENCES", 12)):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(line)
    r.bold = True
    r.font.size = Pt(size)

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("PRACTICAL APPLICATION OF ANALYSIS OF VARIANCE (ANOVA)\nEXECUTIVE RESEARCH & STATISTICAL REPORT")
r.bold = True
r.font.size = Pt(14)

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run(
    "A Rigorous Applied Empirical Analysis of One-Way & Factorial ANOVA Designs, "
    "Diagnostic Validations, Effect Sizes, and Operational Decision Models"
)
r.italic = True
r.font.size = Pt(10.5)

for _ in range(3):
    doc.add_paragraph()

details = [
    ("Candidate Name:", "Jeff Tarimo"),
    ("Course / Unit:", "Research Methods"),
    ("Core Topic:", "Analysis of Variance (ANOVA)"),
    ("Statistical Ecosystem:", "Open-Source Scientific Python (SciPy, Statsmodels, Pandas, NumPy)"),
    ("GitHub Repositories:", "https://github.com/scipy/scipy | https://github.com/statsmodels/statsmodels"),
    ("Evaluation Alpha:", "alpha = 0.05"),
    ("Date:", "October 2026"),
]
for label, value in details:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.15
    p.add_run(f"{label} ").bold = True
    p.add_run(value)

# Body Section
body = doc.add_section(WD_SECTION.NEW_PAGE)
body.footer.is_linked_to_previous = False
add_page_number_footer(body)
sectPr = body._sectPr
pg = OxmlElement("w:pgNumType")
pg.set(qn("w:start"), "1")
sectPr.append(pg)

# ================================================================ SECTION 1
doc.add_heading("1. COMPARATIVE EVALUATION OF INSTRUCTIONAL MODALITIES (ONE-WAY ANOVA)", level=1)
para(
    "This investigation evaluates the empirical impact of three distinct instructional delivery modalities on student academic mastery: "
    "Traditional In-Person Lectures (Method A), Blended Learning (Method B), and Fully Online Learning (Method C). "
    "Final examination marks (scale 0-100) were obtained from randomly selected, independent cohorts of students under identical assessment standards."
)

table(
    ["Instructional Modality", "Sample Observations (Exam Scores)", "n", "Sum (T)", "Mean (X-bar)", "Variance (s^2)", "Std Dev (s)"],
    [
        ["Method A: Traditional Lectures", "68, 70, 65, 72, 66", "5", "341", "68.20", "8.20", "2.8636"],
        ["Method B: Blended Learning", "72, 74, 76, 78, 75", "5", "375", "75.00", "5.00", "2.2361"],
        ["Method C: Fully Online Learning", "75, 78, 80, 82, 79", "5", "394", "78.80", "6.70", "2.5884"],
        ["Overall Sample / Grand Metrics", "N = 15 total subjects", "15", "G = 1110", "X_grand = 74.00", "Pooled s^2 = 6.63", "Total s^2 = 26.29"]
    ],
    widths=[1.7, 1.4, 0.4, 0.6, 0.8, 0.8, 0.8]
)

doc.add_heading("1.1 Statistical Hypotheses & Diagnostic Verification", level=2)
bullets([
    ("Null Hypothesis (H0): ", "mu_A = mu_B = mu_C. Mean academic performance is invariant across traditional, blended, and online instruction."),
    ("Alternative Hypothesis (H1): ", "At least one instructional modality produces a significantly different population mean score."),
    ("Independence: ", "Satisfied through independent random selection and distinct cohort assignments with zero paired observations."),
    ("Normality (Shapiro-Wilk): ", "Method A (W = 0.9622, p = 0.8234), Method B (W = 0.9993, p = 0.9998), Method C (W = 0.9840, p = 0.9546), and model residuals (W = 0.9621, p = 0.7283) all confirm normal Gaussian distributions (p > 0.05)."),
    ("Homoscedasticity (Levene's Test): ", "Centered at the median, W = 0.2090, p = 0.8143 >> 0.05. Variance ratio s_max^2 / s_min^2 = 8.20 / 5.00 = 1.64 < 3.0 confirms equal population variances.")
])

doc.add_heading("1.2 ANOVA Decomposition & Statistical Significance", level=2)
para(
    "Using the correction factor CF = (1110)^2 / 15 = 82,140.00, variance is partitioned into Between-Groups (treatment) and Within-Groups (residual error):"
)

table(
    ["Source of Variation", "Sum of Squares (SS)", "df", "Mean Square (MS)", "F-Statistic", "p-value", "Critical F (alpha=0.05)"],
    [
        ["Between Groups (Instructional Methods)", "288.40", "2", "144.2000", "21.7387", "0.000102", "3.8853"],
        ["Within Groups (Experimental Error)", "79.60", "12", "6.6333", "-", "-", "-"],
        ["Total Variation", "368.00", "14", "-", "-", "-", "-"]
    ],
    widths=[2.1, 1.1, 0.5, 1.0, 0.9, 0.9, 1.1]
)
para(
    "Inference: Because F_calc (21.74) greatly exceeds F_crit (3.89) and p = 0.000102 < 0.001, we reject the null hypothesis H0. "
    "Instructional method exerts a highly significant effect on academic performance. "
    "Effect size analysis yields eta^2 = 288.40 / 368.00 = 0.7837 (78.37%) and population-adjusted omega^2 = 0.7344 (73.44%), "
    "demonstrating that over three-quarters of the variance in exam outcomes is directly governed by teaching format."
)

doc.add_heading("1.3 Post-Hoc Pairwise Contrasts (Tukey's HSD)", level=2)
para(
    "To isolate specific pairwise differences while maintaining the family-wise error rate at alpha = 0.05, "
    "Tukey's Honestly Significant Difference test was computed (q_crit = 3.773, SE = 1.1518, HSD = 4.346 marks):"
)

table(
    ["Contrast Pair", "Mean Difference", "p-adjusted", "95% Confidence Interval", "Statistical Conclusion", "Practical Takeaway"],
    [
        ["Method A vs. Method B", "+6.80", "0.0034", "[+2.4543, +11.1457]", "Significant (Reject H0)", "Blended learning significantly outperforms traditional lectures."],
        ["Method A vs. Method C", "+10.60", "0.0001", "[+6.2543, +14.9457]", "Significant (Reject H0)", "Online learning significantly outperforms traditional lectures."],
        ["Method B vs. Method C", "+3.80", "0.0893", "[-0.5457, +8.1457]", "Not Significant (Retain H0)", "Blended and Online formats yield comparable academic achievement."]
    ],
    widths=[1.5, 0.9, 0.8, 1.3, 1.2, 1.8]
)
box(
    "Executive Recommendation",
    "Traditional lecture delivery is statistically inferior to both blended and online modalities. "
    "Because blended and fully online learning achieve statistically comparable high performance (p = 0.0893), "
    "the institution should transition toward digital and hybrid pedagogical models based on infrastructure availability and student preference.",
    bg="EAFAF1"
)

# ================================================================ SECTION 2
doc.add_heading("2. FACTORIAL ANALYSIS OF STUDY MODALITY AND GENDER (TWO-WAY ANOVA)", level=1)
para(
    "To analyze the simultaneous and interactive influences of study style and demographic factors, a 2 x 2 balanced factorial design "
    "is employed with continuous Test Performance as the Dependent Variable (DV) and two categorical Independent Variables: "
    "Factor A: Study Method (Group Study vs. Individual Study) and Factor B: Gender (Male vs. Female)."
)

doc.add_heading("2.1 Hypotheses & Factorial Advantages", level=2)
bullets([
    ("Main Effect of Study Method: ", "H0_A: mu_Group = mu_Individual vs. H1_A: mu_Group != mu_Individual."),
    ("Main Effect of Gender: ", "H0_B: mu_Male = mu_Female vs. H1_B: mu_Male != mu_Female."),
    ("Interaction Effect (Study Method x Gender): ", "H0_AB: (alpha*beta)_ij = 0 vs. H1_AB: (alpha*beta)_ij != 0 (the impact of study method depends on gender).")
])
para(
    "Methodological Superiority: A two-way ANOVA is strongly preferred over single-factor designs because it: "
    "(1) isolates interaction/moderation dynamics that are completely invisible in one-way tests, "
    "(2) reduces residual error variance by partitioning gender variance out of SS_error, thereby increasing statistical power, "
    "(3) requires fewer experimental participants than running multiple separate trials, and "
    "(4) broadens external generalizability across diverse student sub-populations."
)

doc.add_heading("2.2 Empirical Findings & Moderation Dynamics", level=2)
box(
    "Observed Statistical Results",
    "• Main Effect of Study Method: Statistically Significant (p < 0.05)\n"
    "• Main Effect of Gender: Not Statistically Significant (p > 0.05)\n"
    "• Interaction Effect (Study Method x Gender): Statistically Significant (p < 0.05)",
    bg="FCF3CF"
)
bullets([
    ("Supremacy of the Interaction Effect: ", "In factorial ANOVA, a significant interaction supersedes the main effects. One cannot issue an unconditional blanket claim that 'group study is universally better' because its efficacy is moderated by gender."),
    ("Gender Main Effect Reconciliation: ", "Averaging across both study methods, overall mean scores between males and females appear equal (non-significant main effect). However, this aggregate parity masks strong within-modality divergences."),
    ("Analytical Next Steps: ", "The researcher must avoid broad generalizations, generate an interaction line plot, and execute Simple Main Effects tests (evaluating study method separately within males and within females) to deliver targeted instructional interventions.")
])

# ================================================================ SECTION 3
doc.add_heading("3. STATISTICAL DIAGNOSTICS, CORE ASSUMPTIONS & REMEDIAL FRAMEWORK", level=1)
para(
    "The validity of ANOVA inference rests on the Gauss-Markov assumptions that guarantee test statistics adhere to the theoretical F-distribution. "
    "Rigorous empirical research requires structured pre-testing diagnostics and corrective protocols."
)

doc.add_heading("3.1 The Four Core Assumptions & Testing Procedures", level=2)
bullets([
    ("1. Independence of Observations: ", "Residual errors must be uncorrelated: cov(e_ij, e_i'j') = 0. Enforced via randomized sampling and assignment."),
    ("2. Normality of Residuals: ", "Residuals must follow a normal Gaussian distribution: e_ij ~ N(0, sigma^2). "
     "Tested inferentially via the Shapiro-Wilk test (W statistic, optimal power for n < 50) and visually via Normal Q-Q plots (linear alignment along a 45-degree reference line confirms normality)."),
    ("3. Homogeneity of Variances (Homoscedasticity): ", "Equal group variances: sigma_1^2 = ... = sigma_k^2. "
     "Tested inferentially via Levene's Test (median-centered, robust to non-normality) and Bartlett's Test (high power for strict normality). "
     "Heuristically verified via Hartley's F-max variance ratio (s_max^2 / s_min^2 < 3.0)."),
    ("4. Measurement Scaling: ", "The dependent variable must be continuous (interval/ratio), with categorical treatment factors.")
])

doc.add_heading("3.2 Diagnostic Remedial Decision Matrix", level=2)
table(
    ["Violated Assumption", "Empirical Diagnostic", "Primary Remedy", "Mathematical & Practical Mechanism"],
    [
        ["Severe Non-Normality", "Shapiro-Wilk p < 0.05; Curving Q-Q plots", "Data Transformation or Kruskal-Wallis", "Apply log(X), sqrt(X), or Box-Cox transforms; if skewness persists, deploy non-parametric Kruskal-Wallis H-test."],
        ["Heteroscedasticity", "Levene's p < 0.05; Variance ratio > 3.0", "Welch's Heteroscedastic ANOVA", "Applies Satterthwaite-Welch adjusted degrees of freedom without assuming variance equality (scipy.stats.f_oneway)."],
        ["Combined Violations", "Heavy-tailed skewness + unequal scatter", "Permutation / Bootstrap Resampling", "Re-samples empirical data with replacement (e.g., 10,000 iterations) to derive non-parametric empirical F-distributions."],
        ["Dependent Observations", "Correlated residuals, repeated measures", "Repeated Measures / Mixed-Effects Models", "Account for intra-subject covariance using Greenhouse-Geisser sphericity corrections or Linear Mixed Models (statsmodels.mixedlm)."]
    ],
    widths=[1.5, 1.4, 1.5, 2.1]
)

# ================================================================ SECTION 4
doc.add_heading("4. OPERATIONAL DECISION MAKING & FAMILY-WISE ERROR CONTROL", level=1)
para(
    "A multi-shift organizational evaluation comparing employee productivity across four distinct schedules yields: "
    "F(3, 36) = 5.27, p = 0.004 at alpha = 0.05."
)

doc.add_heading("4.1 Statistical & Practical Significance", level=2)
bullets([
    ("Hypothesis & Rejection: ", "With df1 = 3 and df2 = 36, F_calc = 5.27 > F_crit(0.05, 3, 36) = 2.87, and p = 0.004 < 0.05. "
     "We reject H0. Productivity levels differ significantly across shift schedules."),
    ("Practical Effect Size (Eta-Squared): ", 
     "eta^2 = (df1 * F) / (df1 * F + df2) = (3 * 5.27) / [(3 * 5.27) + 36] = 15.81 / 51.81 = 0.3051 (30.51%). "
     "A remarkable 30.51% of all employee productivity variation is directly attributable to shift assignment, representing a very large operational effect (Cohen's benchmark >= 14%)."),
    ("Managerial Action: ", "Management should conduct post-hoc pairwise contrasts to identify lagging shifts (e.g. nocturnal rotas), optimize rest intervals, and redesign shift scheduling to capture major output gains.")
])

doc.add_heading("4.2 Preservation of Nominal Alpha vs. Multiple t-Tests", level=2)
para(
    "Conducting multiple pairwise two-sample t-tests across k = 4 shift schedules requires c = 4(3)/2 = 6 pairwise tests. "
    "This practice severely inflates the Family-Wise Error Rate (FWER):"
)
box(
    "Family-Wise Type I Error Inflation Formula",
    "alpha_FW = 1 - (1 - alpha)^c = 1 - (1 - 0.05)^6 = 1 - (0.95)^6 = 1 - 0.7351 = 0.2649 (26.49%)",
    bg="FADBD8"
)
bullets([
    ("Alpha Inflation: ", "Running six t-tests produces an intolerable 26.5% chance of falsely declaring a non-existent difference (over a 1-in-4 false positive risk). ANOVA strictly maintains the experiment-wise error rate at 5%."),
    ("Omnibus Protection: ", "ANOVA tests for any overall difference across all groups simultaneously, shielding against data snooping."),
    ("Variance Pooling: ", "ANOVA computes a single pooled error variance (MS_error) utilizing all 40 employees (36 degrees of freedom), providing superior statistical power and precision over small-sample pairwise t-tests.")
])

# Save Document
doc.save(OUTPUT)
print(f"Successfully generated summarized Word report: {OUTPUT}")
