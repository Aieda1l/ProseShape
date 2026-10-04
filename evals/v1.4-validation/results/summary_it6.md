# _it6: 13 samples, arms ['U', 'O', 'PS', 'HS', 'PS14f']

| arm | overall [95% CI] | facts | meaning | voice | natural | proportion | format | mean rank |
|---|---|---|---|---|---|---|---|---|
| U | 3.50 [2.56, 4.62] | 5.00 | 5.00 | 3.08 | 2.62 | 1.62 | 5.00 | 4.75 |
| O | 8.21 [7.83, 8.58] | 4.69 | 4.60 | 4.62 | 4.73 | 4.62 | 4.88 | 1.87 |
| PS | 6.58 [5.73, 7.42] | 4.08 | 3.88 | 4.06 | 4.60 | 3.46 | 4.63 | 3.63 |
| HS | 7.65 [7.02, 8.27] | 4.50 | 4.48 | 4.54 | 4.65 | 4.25 | 5.00 | 2.48 |
| PS14f | 8.06 [7.65, 8.44] | 4.83 | 4.83 | 4.50 | 4.42 | 4.58 | 4.96 | 2.27 |

| paired | diff [95% CI] | better/worse/tie |
|---|---|---|
| PS14f − U | +4.56 [+3.50, +5.50] | 12/0/1 |
| PS14f − O | -0.15 [-0.63, +0.37] | 4/6/3 |
| PS14f − PS | +1.48 [+0.71, +2.35] | 9/1/3 |
| PS14f − HS | +0.40 [-0.25, +1.08] | 6/5/2 |

| sample | U | O | PS | HS | PS14f |
|---|---|---|---|---|---|
| s01_ai_blog | 2.00 | 7.50 | 6.00 | 8.25 | 7.50 |
| s02_marketing | 2.25 | 8.25 | 4.75 | 8.00 | 7.50 |
| s03_email_pro | 2.25 | 8.50 | 7.00 | 8.00 | 7.00 |
| s04_tech_docs | 2.00 | 8.00 | 6.75 | 6.25 | 8.50 |
| s05_explainer | 3.25 | 8.25 | 6.25 | 7.00 | 7.25 |
| s06_academic | 2.00 | 8.50 | 6.75 | 8.50 | 8.00 |
| s07_social | 2.25 | 6.75 | 5.00 | 7.00 | 8.50 |
| s08_fiction | 4.75 | 7.25 | 3.50 | 6.00 | 8.50 |
| s09_news_quotes | 3.00 | 9.00 | 8.25 | 9.00 | 7.75 |
| s10_human_tech | 6.00 | 8.25 | 6.50 | 6.00 | 7.25 |
| s11_human_voice | 8.75 | 8.75 | 8.75 | 8.75 | 8.75 |
| s12_email_nearclean | 5.00 | 9.50 | 9.50 | 9.50 | 9.50 |
| s13_spanish | 2.00 | 8.25 | 6.50 | 7.25 | 8.75 |

issue counts (all passes):
  U: under_edit=51
  O: added_fact=5, changed_fact=11, dropped_fact=14, format_damage=4, other=18, over_edit=1, under_edit=4
  PS: added_fact=9, changed_fact=12, dropped_fact=34, format_damage=10, other=15, over_edit=13, under_edit=3, voice_loss=5
  HS: added_fact=1, changed_fact=9, dropped_fact=27, other=16, under_edit=9
  PS14f: changed_fact=1, dropped_fact=9, format_damage=2, other=27, under_edit=5, voice_loss=3
