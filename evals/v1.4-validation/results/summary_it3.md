# _it3: 13 samples, arms ['U', 'O', 'PS', 'HS', 'PS14c']

| arm | overall [95% CI] | facts | meaning | voice | natural | proportion | format | mean rank |
|---|---|---|---|---|---|---|---|---|
| U | 3.46 [2.56, 4.54] | 5.00 | 5.00 | 3.04 | 2.58 | 1.58 | 5.00 | 4.73 |
| O | 8.13 [7.69, 8.56] | 4.60 | 4.60 | 4.58 | 4.69 | 4.54 | 4.88 | 2.08 |
| PS | 6.73 [5.83, 7.63] | 4.06 | 3.90 | 4.13 | 4.60 | 3.56 | 4.63 | 3.42 |
| HS | 7.63 [6.98, 8.29] | 4.42 | 4.40 | 4.50 | 4.65 | 4.21 | 5.00 | 2.62 |
| PS14c | 8.06 [7.56, 8.50] | 4.69 | 4.77 | 4.46 | 4.48 | 4.60 | 4.98 | 2.15 |

| paired | diff [95% CI] | better/worse/tie |
|---|---|---|
| PS14c − U | +4.60 [+3.44, +5.62] | 12/0/1 |
| PS14c − O | -0.08 [-0.62, +0.42] | 5/5/3 |
| PS14c − PS | +1.33 [+0.73, +1.96] | 9/1/3 |
| PS14c − HS | +0.42 [+0.06, +0.90] | 8/3/2 |

| sample | U | O | PS | HS | PS14c |
|---|---|---|---|---|---|
| s01_ai_blog | 2.00 | 7.50 | 6.25 | 8.25 | 8.00 |
| s02_marketing | 2.25 | 8.25 | 4.75 | 7.25 | 7.75 |
| s03_email_pro | 2.75 | 7.75 | 7.25 | 8.00 | 8.50 |
| s04_tech_docs | 2.00 | 8.00 | 7.50 | 6.00 | 8.75 |
| s05_explainer | 3.00 | 8.75 | 6.50 | 7.25 | 7.50 |
| s06_academic | 2.25 | 8.00 | 6.75 | 8.75 | 8.25 |
| s07_social | 2.25 | 6.25 | 5.75 | 7.00 | 8.00 |
| s08_fiction | 4.00 | 7.50 | 3.25 | 6.00 | 6.75 |
| s09_news_quotes | 3.00 | 8.75 | 8.75 | 8.75 | 8.50 |
| s10_human_tech | 5.75 | 8.50 | 6.25 | 5.75 | 6.25 |
| s11_human_voice | 8.75 | 8.75 | 8.75 | 8.75 | 8.75 |
| s12_email_nearclean | 5.00 | 9.75 | 9.75 | 9.75 | 9.75 |
| s13_spanish | 2.00 | 8.00 | 6.00 | 7.75 | 8.00 |

issue counts (all passes):
  U: under_edit=50
  O: added_fact=5, changed_fact=9, dropped_fact=16, format_damage=3, other=21, over_edit=1, under_edit=5
  PS: added_fact=9, changed_fact=9, dropped_fact=37, format_damage=10, other=17, over_edit=16, under_edit=4, voice_loss=3
  HS: added_fact=3, changed_fact=8, dropped_fact=32, other=9, under_edit=10
  PS14c: added_fact=2, changed_fact=4, dropped_fact=11, other=25, over_edit=1, under_edit=4, voice_loss=5
