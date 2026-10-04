# _it5: 13 samples, arms ['U', 'O', 'PS', 'HS', 'PS14e']

| arm | overall [95% CI] | facts | meaning | voice | natural | proportion | format | mean rank |
|---|---|---|---|---|---|---|---|---|
| U | 3.46 [2.54, 4.52] | 5.00 | 5.00 | 2.98 | 2.58 | 1.58 | 5.00 | 4.71 |
| O | 8.13 [7.75, 8.50] | 4.58 | 4.67 | 4.60 | 4.81 | 4.54 | 4.88 | 2.06 |
| PS | 6.65 [5.69, 7.58] | 4.08 | 3.90 | 4.08 | 4.54 | 3.50 | 4.65 | 3.40 |
| HS | 7.67 [7.04, 8.27] | 4.52 | 4.46 | 4.46 | 4.67 | 4.31 | 5.00 | 2.62 |
| PS14e | 8.08 [7.62, 8.52] | 4.77 | 4.73 | 4.52 | 4.37 | 4.60 | 4.96 | 2.21 |

| paired | diff [95% CI] | better/worse/tie |
|---|---|---|
| PS14e − U | +4.62 [+3.60, +5.54] | 12/0/1 |
| PS14e − O | -0.06 [-0.62, +0.48] | 5/5/3 |
| PS14e − PS | +1.42 [+0.67, +2.37] | 10/0/3 |
| PS14e − HS | +0.40 [-0.19, +1.10] | 6/4/3 |

| sample | U | O | PS | HS | PS14e |
|---|---|---|---|---|---|
| s01_ai_blog | 2.00 | 7.25 | 6.00 | 7.75 | 8.25 |
| s02_marketing | 2.00 | 8.00 | 5.00 | 8.00 | 7.50 |
| s03_email_pro | 2.75 | 8.25 | 6.75 | 8.25 | 7.25 |
| s04_tech_docs | 2.50 | 8.00 | 7.50 | 6.25 | 8.75 |
| s05_explainer | 2.75 | 8.50 | 6.25 | 7.50 | 7.00 |
| s06_academic | 2.00 | 8.25 | 7.25 | 8.25 | 8.50 |
| s07_social | 2.00 | 6.75 | 5.25 | 7.75 | 8.00 |
| s08_fiction | 4.25 | 7.25 | 2.75 | 5.75 | 8.75 |
| s09_news_quotes | 3.00 | 9.00 | 9.00 | 9.00 | 9.00 |
| s10_human_tech | 6.00 | 8.00 | 6.50 | 6.00 | 7.50 |
| s11_human_voice | 8.50 | 8.50 | 8.50 | 8.50 | 8.50 |
| s12_email_nearclean | 5.25 | 9.50 | 9.50 | 9.50 | 9.50 |
| s13_spanish | 2.00 | 8.50 | 6.25 | 7.25 | 6.50 |

issue counts (all passes):
  U: under_edit=51
  O: added_fact=5, changed_fact=12, dropped_fact=14, format_damage=5, other=16, over_edit=1, under_edit=3
  PS: added_fact=8, changed_fact=15, dropped_fact=30, format_damage=10, other=12, over_edit=14, under_edit=2, voice_loss=9
  HS: added_fact=1, changed_fact=8, dropped_fact=24, other=12, under_edit=8
  PS14e: changed_fact=6, dropped_fact=7, format_damage=1, other=22, over_edit=1, under_edit=12
