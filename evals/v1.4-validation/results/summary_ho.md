# _ho: 12 samples, arms ['U', 'O', 'PS', 'HS', 'PS14g']

| arm | overall [95% CI] | facts | meaning | voice | natural | proportion | format | mean rank |
|---|---|---|---|---|---|---|---|---|
| U | 3.75 [2.81, 4.90] | 5.00 | 5.00 | 3.35 | 2.73 | 1.65 | 5.00 | 4.52 |
| O | 7.33 [6.88, 7.79] | 4.27 | 4.35 | 4.44 | 4.56 | 4.19 | 4.98 | 2.52 |
| PS | 5.94 [5.12, 6.75] | 3.60 | 3.58 | 3.90 | 4.44 | 3.15 | 4.50 | 3.75 |
| HS | 7.27 [6.58, 7.90] | 4.50 | 4.52 | 4.38 | 4.33 | 4.00 | 5.00 | 2.38 |
| PS14g | 8.17 [7.79, 8.54] | 4.75 | 4.81 | 4.65 | 4.60 | 4.67 | 4.96 | 1.83 |

| paired | diff [95% CI] | better/worse/tie |
|---|---|---|
| PS14g − U | +4.42 [+3.00, +5.62] | 11/1/0 |
| PS14g − O | +0.83 [+0.19, +1.54] | 7/3/2 |
| PS14g − PS | +2.23 [+1.21, +3.25] | 9/1/2 |
| PS14g − HS | +0.90 [+0.06, +1.75] | 9/2/1 |

| sample | U | O | PS | HS | PS14g |
|---|---|---|---|---|---|
| h01_release_notes | 2.50 | 7.00 | 6.25 | 7.75 | 8.75 |
| h02_cover_letter | 2.25 | 7.00 | 5.50 | 7.25 | 8.75 |
| h03_support_reply | 2.75 | 8.75 | 6.00 | 7.25 | 8.75 |
| h04_readme | 2.25 | 8.00 | 5.75 | 8.75 | 8.75 |
| h05_oped | 2.50 | 7.00 | 5.75 | 7.50 | 8.00 |
| h06_press_release | 3.00 | 7.75 | 7.50 | 7.25 | 7.50 |
| h07_personal_essay | 3.50 | 7.75 | 5.25 | 6.50 | 7.25 |
| h08_fiction_dialogue | 4.50 | 6.25 | 3.25 | 5.25 | 8.25 |
| h09_grant_abstract | 2.25 | 5.75 | 6.75 | 7.50 | 9.00 |
| h10_human_rust | 5.00 | 7.25 | 3.75 | 5.00 | 8.50 |
| h11_human_twain | 8.50 | 8.50 | 8.50 | 8.50 | 7.50 |
| h12_nearclean_slack | 6.00 | 7.00 | 7.00 | 8.75 | 7.00 |

issue counts (all passes):
  U: new_cliche=1, under_edit=46
  O: added_fact=8, changed_fact=17, dropped_fact=22, new_cliche=1, other=20, under_edit=8, voice_loss=1
  PS: added_fact=12, changed_fact=18, dropped_fact=48, format_damage=14, meaning=1, misattribution=1, other=19, over_edit=19, voice_loss=11
  HS: added_fact=5, changed_fact=5, dropped_fact=19, misattribution=1, new_cliche=1, other=20, over_edit=1, under_edit=13, voice_loss=1
  PS14g: added_fact=1, changed_fact=3, dropped_fact=12, format_damage=2, new_cliche=3, other=23, under_edit=2, voice_loss=3
