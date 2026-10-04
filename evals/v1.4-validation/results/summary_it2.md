# _it2: 13 samples, arms ['U', 'O', 'PS', 'HS', 'PS14b']

| arm | overall [95% CI] | facts | meaning | voice | natural | proportion | format | mean rank |
|---|---|---|---|---|---|---|---|---|
| U | 3.52 [2.58, 4.62] | 5.00 | 5.00 | 3.13 | 2.63 | 1.67 | 4.98 | 4.67 |
| O | 8.00 [7.48, 8.46] | 4.63 | 4.67 | 4.63 | 4.73 | 4.58 | 4.85 | 2.08 |
| PS | 6.69 [5.77, 7.58] | 4.10 | 3.88 | 4.12 | 4.65 | 3.62 | 4.65 | 3.42 |
| HS | 7.69 [7.04, 8.33] | 4.50 | 4.42 | 4.62 | 4.75 | 4.33 | 5.00 | 2.65 |
| PS14b | 8.10 [7.77, 8.44] | 4.77 | 4.77 | 4.52 | 4.58 | 4.63 | 5.00 | 2.17 |

| paired | diff [95% CI] | better/worse/tie |
|---|---|---|
| PS14b − U | +4.58 [+3.44, +5.56] | 12/0/1 |
| PS14b − O | +0.10 [-0.29, +0.54] | 4/6/3 |
| PS14b − PS | +1.40 [+0.73, +2.12] | 10/1/2 |
| PS14b − HS | +0.40 [-0.02, +0.87] | 8/2/3 |

| sample | U | O | PS | HS | PS14b |
|---|---|---|---|---|---|
| s01_ai_blog | 2.00 | 7.00 | 5.50 | 8.00 | 8.25 |
| s02_marketing | 2.25 | 8.00 | 4.75 | 7.25 | 8.00 |
| s03_email_pro | 2.75 | 8.25 | 6.75 | 8.25 | 8.50 |
| s04_tech_docs | 2.25 | 7.75 | 7.25 | 6.00 | 8.25 |
| s05_explainer | 3.00 | 8.75 | 6.75 | 7.00 | 7.75 |
| s06_academic | 2.00 | 8.50 | 7.00 | 9.00 | 8.00 |
| s07_social | 2.00 | 5.75 | 5.75 | 7.75 | 8.00 |
| s08_fiction | 4.25 | 7.25 | 3.25 | 5.50 | 7.00 |
| s09_news_quotes | 3.00 | 9.00 | 9.00 | 9.00 | 8.50 |
| s10_human_tech | 6.50 | 7.75 | 7.00 | 6.50 | 7.25 |
| s11_human_voice | 8.50 | 8.50 | 8.50 | 8.50 | 8.50 |
| s12_email_nearclean | 5.25 | 9.50 | 9.50 | 9.50 | 9.50 |
| s13_spanish | 2.00 | 8.00 | 6.00 | 7.75 | 7.75 |

issue counts (all passes):
  U: under_edit=51
  O: added_fact=5, changed_fact=9, dropped_fact=13, format_damage=5, other=18, over_edit=2, under_edit=3
  PS: added_fact=9, changed_fact=9, dropped_fact=33, format_damage=10, other=14, over_edit=12, under_edit=2, voice_loss=7
  HS: added_fact=2, changed_fact=6, dropped_fact=25, other=12, over_edit=1, under_edit=6, voice_loss=1
  PS14b: added_fact=2, changed_fact=4, dropped_fact=9, other=29, under_edit=4
