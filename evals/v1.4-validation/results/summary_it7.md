# _it7: 13 samples, arms ['U', 'O', 'PS', 'HS', 'PS14g']

| arm | overall [95% CI] | facts | meaning | voice | natural | proportion | format | mean rank |
|---|---|---|---|---|---|---|---|---|
| U | 3.37 [2.48, 4.42] | 5.00 | 5.00 | 2.96 | 2.60 | 1.60 | 4.98 | 4.67 |
| O | 7.90 [7.46, 8.27] | 4.65 | 4.60 | 4.52 | 4.71 | 4.54 | 4.87 | 2.15 |
| PS | 6.44 [5.58, 7.27] | 4.00 | 3.88 | 4.00 | 4.54 | 3.48 | 4.58 | 3.50 |
| HS | 7.62 [7.00, 8.17] | 4.46 | 4.42 | 4.52 | 4.63 | 4.31 | 4.98 | 2.77 |
| PS14g | 8.17 [7.87, 8.48] | 4.83 | 4.79 | 4.52 | 4.60 | 4.63 | 4.94 | 1.90 |

| paired | diff [95% CI] | better/worse/tie |
|---|---|---|
| PS14g − U | +4.81 [+3.69, +5.81] | 12/0/1 |
| PS14g − O | +0.27 [-0.19, +0.73] | 8/3/2 |
| PS14g − PS | +1.73 [+1.06, +2.46] | 10/0/3 |
| PS14g − HS | +0.56 [+0.06, +1.12] | 7/4/2 |

| sample | U | O | PS | HS | PS14g |
|---|---|---|---|---|---|
| s01_ai_blog | 2.00 | 7.50 | 6.00 | 8.50 | 7.75 |
| s02_marketing | 2.00 | 7.50 | 4.75 | 8.25 | 8.00 |
| s03_email_pro | 2.25 | 8.00 | 6.50 | 8.00 | 8.25 |
| s04_tech_docs | 2.00 | 7.50 | 7.00 | 6.00 | 8.75 |
| s05_explainer | 3.00 | 8.50 | 6.00 | 7.50 | 7.25 |
| s06_academic | 2.25 | 8.00 | 7.00 | 8.00 | 9.00 |
| s07_social | 2.00 | 5.75 | 5.25 | 7.50 | 8.00 |
| s08_fiction | 4.50 | 7.50 | 3.00 | 6.00 | 7.75 |
| s09_news_quotes | 3.00 | 8.75 | 8.50 | 8.75 | 8.50 |
| s10_human_tech | 5.75 | 8.25 | 6.50 | 5.75 | 7.25 |
| s11_human_voice | 8.25 | 8.25 | 8.25 | 8.25 | 8.25 |
| s12_email_nearclean | 4.75 | 9.00 | 9.00 | 9.00 | 9.00 |
| s13_spanish | 2.00 | 8.25 | 6.00 | 7.50 | 8.50 |

issue counts (all passes):
  U: under_edit=52
  O: added_fact=5, changed_fact=12, dropped_fact=13, format_damage=4, other=25, under_edit=3
  PS: added_fact=9, changed_fact=12, dropped_fact=40, format_damage=9, other=16, over_edit=15, under_edit=3, voice_loss=5
  HS: changed_fact=7, dropped_fact=29, format_damage=1, other=11, over_edit=1, under_edit=7
  PS14g: changed_fact=1, dropped_fact=9, format_damage=1, misattribution=1, other=22, over_edit=1, under_edit=6
