# _it1: 13 samples, arms ['U', 'O', 'PS', 'HS', 'PS14a']

| arm | overall [95% CI] | facts | meaning | voice | natural | proportion | format | mean rank |
|---|---|---|---|---|---|---|---|---|
| U | 3.48 [2.56, 4.62] | 5.00 | 5.00 | 3.00 | 2.60 | 1.60 | 5.00 | 4.73 |
| O | 8.17 [7.79, 8.56] | 4.54 | 4.56 | 4.62 | 4.87 | 4.60 | 4.87 | 2.04 |
| PS | 6.71 [5.75, 7.62] | 3.98 | 3.87 | 4.04 | 4.63 | 3.52 | 4.62 | 3.19 |
| HS | 7.62 [6.98, 8.23] | 4.44 | 4.40 | 4.38 | 4.60 | 4.29 | 5.00 | 2.62 |
| PS14a | 7.71 [7.15, 8.23] | 4.79 | 4.69 | 4.35 | 4.29 | 4.40 | 4.90 | 2.42 |

| paired | diff [95% CI] | better/worse/tie |
|---|---|---|
| PS14a − U | +4.23 [+3.08, +5.23] | 11/0/2 |
| PS14a − O | -0.46 [-1.12, +0.10] | 4/7/2 |
| PS14a − PS | +1.00 [+0.12, +1.94] | 8/3/2 |
| PS14a − HS | +0.10 [-0.48, +0.67] | 5/4/4 |

| sample | U | O | PS | HS | PS14a |
|---|---|---|---|---|---|
| s01_ai_blog | 2.00 | 7.50 | 6.25 | 8.25 | 8.00 |
| s02_marketing | 2.75 | 8.25 | 4.50 | 7.50 | 8.00 |
| s03_email_pro | 2.25 | 8.25 | 6.75 | 8.00 | 8.00 |
| s04_tech_docs | 2.00 | 8.25 | 7.50 | 6.50 | 8.75 |
| s05_explainer | 2.75 | 8.00 | 6.75 | 7.75 | 7.00 |
| s06_academic | 2.25 | 8.50 | 8.25 | 8.25 | 7.50 |
| s07_social | 2.25 | 7.00 | 5.50 | 7.50 | 8.00 |
| s08_fiction | 5.00 | 7.50 | 3.25 | 6.25 | 7.75 |
| s09_news_quotes | 2.75 | 9.00 | 8.50 | 9.00 | 6.75 |
| s10_human_tech | 5.50 | 8.75 | 6.25 | 5.50 | 5.50 |
| s11_human_voice | 9.00 | 9.00 | 9.00 | 9.00 | 9.00 |
| s12_email_nearclean | 4.75 | 9.25 | 9.25 | 9.25 | 9.25 |
| s13_spanish | 2.00 | 7.00 | 5.50 | 6.25 | 6.75 |

issue counts (all passes):
  U: under_edit=49
  O: added_fact=4, changed_fact=13, dropped_fact=19, format_damage=2, other=11, over_edit=1, under_edit=2
  PS: added_fact=8, changed_fact=12, dropped_fact=37, format_damage=10, other=10, over_edit=12, under_edit=3, voice_loss=7
  HS: added_fact=1, changed_fact=8, dropped_fact=28, other=17, under_edit=10, voice_loss=1
  PS14a: changed_fact=6, dropped_fact=4, format_damage=5, misattribution=2, new_cliche=1, other=31, under_edit=9
