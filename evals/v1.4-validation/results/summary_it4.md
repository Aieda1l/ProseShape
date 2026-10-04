# _it4: 13 samples, arms ['U', 'O', 'PS', 'HS', 'PS14d']

| arm | overall [95% CI] | facts | meaning | voice | natural | proportion | format | mean rank |
|---|---|---|---|---|---|---|---|---|
| U | 3.38 [2.48, 4.44] | 5.00 | 5.00 | 3.08 | 2.62 | 1.60 | 5.00 | 4.83 |
| O | 8.04 [7.62, 8.46] | 4.63 | 4.54 | 4.60 | 4.77 | 4.46 | 4.90 | 2.06 |
| PS | 6.56 [5.65, 7.46] | 4.04 | 3.83 | 4.08 | 4.44 | 3.46 | 4.65 | 3.50 |
| HS | 7.58 [6.90, 8.23] | 4.44 | 4.35 | 4.60 | 4.71 | 4.19 | 5.00 | 2.69 |
| PS14d | 8.23 [7.83, 8.63] | 4.75 | 4.87 | 4.54 | 4.56 | 4.69 | 5.00 | 1.92 |

| paired | diff [95% CI] | better/worse/tie |
|---|---|---|
| PS14d − U | +4.85 [+3.73, +5.81] | 12/0/1 |
| PS14d − O | +0.19 [-0.21, +0.62] | 6/4/3 |
| PS14d − PS | +1.67 [+0.94, +2.44] | 10/0/3 |
| PS14d − HS | +0.65 [+0.21, +1.13] | 7/3/3 |

| sample | U | O | PS | HS | PS14d |
|---|---|---|---|---|---|
| s01_ai_blog | 2.00 | 7.00 | 5.75 | 8.00 | 8.00 |
| s02_marketing | 2.00 | 8.00 | 5.00 | 7.25 | 8.50 |
| s03_email_pro | 2.00 | 8.25 | 7.00 | 8.00 | 7.75 |
| s04_tech_docs | 2.25 | 8.25 | 7.00 | 6.25 | 8.50 |
| s05_explainer | 3.00 | 8.00 | 6.00 | 7.50 | 8.00 |
| s06_academic | 2.00 | 8.00 | 7.00 | 8.00 | 9.00 |
| s07_social | 2.25 | 6.50 | 5.00 | 7.75 | 8.50 |
| s08_fiction | 4.25 | 7.50 | 3.25 | 5.75 | 7.75 |
| s09_news_quotes | 3.25 | 9.00 | 8.75 | 9.00 | 8.75 |
| s10_human_tech | 5.50 | 8.00 | 6.25 | 5.50 | 7.00 |
| s11_human_voice | 8.50 | 8.50 | 8.50 | 8.50 | 8.50 |
| s12_email_nearclean | 5.00 | 9.75 | 9.75 | 9.75 | 9.75 |
| s13_spanish | 2.00 | 7.75 | 6.00 | 7.25 | 7.00 |

issue counts (all passes):
  U: under_edit=50
  O: added_fact=5, changed_fact=10, dropped_fact=17, format_damage=3, other=25, over_edit=1, under_edit=2
  PS: added_fact=7, changed_fact=14, dropped_fact=37, format_damage=10, other=11, over_edit=18, under_edit=4, voice_loss=6
  HS: added_fact=2, changed_fact=8, dropped_fact=31, other=9, under_edit=9, voice_loss=1
  PS14d: added_fact=2, changed_fact=4, dropped_fact=6, new_cliche=1, other=22, over_edit=1, under_edit=5, voice_loss=1
