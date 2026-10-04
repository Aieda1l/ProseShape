### Ablation: executor model and reference files (run 1 outputs; two blind judge passes, Opus 5.5)

Arms: U untouched; O ordinary editor (Sonnet 5.5); Oo ordinary editor (Opus 5.5); PS ProseShape full bundle (Sonnet 5.5); PSo ProseShape full bundle (Opus 5.5); PSc ProseShape SKILL.md only, no references (Sonnet 5.5); HS HumanScope (Sonnet 5.5).


#### All 13

| Arm | overall mean [95% CI] | facts | meaning | voice | proportionality | mean rank | dropped/added facts flagged (2 passes) |
|---|---|---|---|---|---|---|---|
| U | 3.46 [2.46, 4.65] | 5.00 | 5.00 | 2.85 | 1.62 | 6.62 | 0/0 |
| O | 8.08 [7.46, 8.65] | 4.77 | 4.65 | 4.54 | 4.54 | 2.77 | 7/4 |
| Oo | 7.54 [6.77, 8.27] | 4.15 | 4.31 | 4.65 | 4.27 | 3.50 | 4/12 |
| PS | 7.12 [6.15, 8.04] | 4.23 | 4.04 | 4.19 | 3.85 | 3.85 | 17/4 |
| PSo | 7.08 [6.15, 7.92] | 3.96 | 4.15 | 4.19 | 3.73 | 4.42 | 12/14 |
| PSc | 7.08 [6.19, 7.96] | 4.19 | 4.08 | 4.12 | 3.88 | 4.00 | 15/2 |
| HS | 7.92 [7.19, 8.62] | 4.77 | 4.69 | 4.54 | 4.42 | 2.85 | 5/0 |

#### AI-shaped 10

| Arm | overall mean [95% CI] | facts | meaning | voice | proportionality | mean rank | dropped/added facts flagged (2 passes) |
|---|---|---|---|---|---|---|---|
| U | 2.55 [2.10, 3.20] | 5.00 | 5.00 | 2.40 | 1.10 | 6.65 | 0/0 |
| O | 7.90 [7.25, 8.45] | 4.70 | 4.60 | 4.50 | 4.55 | 2.55 | 7/4 |
| Oo | 7.10 [6.35, 7.85] | 3.90 | 4.10 | 4.55 | 4.05 | 3.90 | 4/12 |
| PS | 6.60 [5.55, 7.60] | 4.00 | 3.75 | 3.95 | 3.60 | 3.95 | 17/4 |
| PSo | 6.55 [5.60, 7.40] | 3.65 | 3.90 | 3.95 | 3.45 | 4.40 | 12/14 |
| PSc | 6.70 [5.85, 7.55] | 3.95 | 3.80 | 3.85 | 3.75 | 4.20 | 15/2 |
| HS | 7.85 [7.20, 8.45] | 4.70 | 4.60 | 4.40 | 4.45 | 2.35 | 5/0 |

#### Controls 3

| Arm | overall mean [95% CI] | facts | meaning | voice | proportionality | mean rank | dropped/added facts flagged (2 passes) |
|---|---|---|---|---|---|---|---|
| U | 6.50 [5.00, 9.00] | 5.00 | 5.00 | 4.33 | 3.33 | 6.50 | 0/0 |
| O | 8.67 [7.00, 10.00] | 5.00 | 4.83 | 4.67 | 4.50 | 3.50 | 0/0 |
| Oo | 9.00 [8.00, 10.00] | 5.00 | 5.00 | 5.00 | 5.00 | 2.17 | 0/0 |
| PS | 8.83 [7.50, 10.00] | 5.00 | 5.00 | 5.00 | 4.67 | 3.50 | 0/0 |
| PSo | 8.83 [7.50, 10.00] | 5.00 | 5.00 | 5.00 | 4.67 | 4.50 | 0/0 |
| PSc | 8.33 [6.00, 10.00] | 5.00 | 5.00 | 5.00 | 4.33 | 3.33 | 0/0 |
| HS | 8.17 [5.50, 10.00] | 5.00 | 5.00 | 5.00 | 4.33 | 4.50 | 0/0 |

#### Paired differences (overall), all 13 samples

| Comparison | mean diff [95% CI] | better/worse/tie |
|---|---|---|
| PSo − Oo | -0.46 [-1.38, +0.42] | 3/8/2 |
| PSo − PS | -0.04 [-0.85, +0.81] | 4/5/4 |
| PS − PSc | +0.04 [-0.62, +0.65] | 4/6/3 |
| PS − O | -0.96 [-1.88, -0.15] | 4/7/2 |
| PSc − O | -1.00 [-1.85, -0.23] | 3/8/2 |
| Oo − O | -0.54 [-1.12, +0.00] | 2/6/5 |
| PSo − HS | -0.85 [-1.81, +0.04] | 4/7/2 |

#### Per-sample overall (mean of 2 passes)

| Sample | U | O | Oo | PS | PSo | PSc | HS |
|---|---|---|---|---|---|---|---|
| s01_ai_blog | 2.0 | 8.0 | 5.5 | 6.0 | 4.5 | 8.5 | 9.0 |
| s02_marketing | 2.0 | 8.0 | 5.5 | 5.0 | 6.5 | 6.0 | 9.0 |
| s03_email_pro | 2.5 | 7.0 | 7.5 | 7.5 | 7.0 | 6.0 | 9.0 |
| s04_tech_docs | 2.0 | 9.0 | 8.5 | 8.0 | 7.0 | 6.5 | 6.5 |
| s05_explainer | 3.0 | 9.0 | 8.0 | 8.0 | 5.0 | 6.5 | 7.5 |
| s06_academic | 2.0 | 8.5 | 8.5 | 7.5 | 7.5 | 8.0 | 8.5 |
| s07_social | 2.0 | 5.5 | 5.5 | 6.0 | 8.0 | 6.5 | 7.5 |
| s08_fiction | 5.0 | 8.0 | 7.5 | 3.5 | 4.0 | 4.0 | 6.0 |
| s09_news_quotes | 3.0 | 8.0 | 8.0 | 9.0 | 7.5 | 9.0 | 8.0 |
| s13_spanish | 2.0 | 8.0 | 6.5 | 5.5 | 8.5 | 6.0 | 7.5 |
| s10_human_tech | 5.5 | 7.0 | 8.0 | 7.5 | 7.5 | 6.0 | 5.5 |
| s11_human_voice | 9.0 | 9.0 | 9.0 | 9.0 | 9.0 | 9.0 | 9.0 |
| s12_email_nearclean | 5.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 |

#### Deterministic checks for ablation arms (run 1)

| Arm | token change AI | token change controls | length ratio AI | numbers added/dropped | cost (13 samples, USD) |
|---|---|---|---|---|---|
| O | 0.25 | 0.09 | 0.83 | 0/0 | 0.18 |
| Oo | 0.33 | 0.03 | 0.88 | 0/0 | 0.35 |
| PS | 0.35 | 0.03 | 0.72 | 0/0 | 0.75 |
| PSo | 0.39 | 0.03 | 0.83 | 2/0 | 1.51 |
| PSc | 0.32 | 0.03 | 0.74 | 0/0 | 0.27 |