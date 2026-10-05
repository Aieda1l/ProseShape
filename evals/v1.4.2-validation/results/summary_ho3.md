# _ho3: 16 samples, arms ['U', 'O', 'HS', 'PS142c', 'PS14g']

| arm | overall [95% CI] | facts | meaning | voice | natural | proportion | format | mean rank |
|---|---|---|---|---|---|---|---|---|
| U | 5.48 [4.12, 6.80] | 5.00 | 5.00 | 3.95 | 3.70 | 2.86 | 5.00 | 3.86 |
| O | 7.44 [7.02, 7.89] | 4.56 | 4.58 | 4.64 | 4.67 | 4.20 | 4.97 | 2.92 |
| HS | 7.41 [6.97, 7.86] | 4.55 | 4.52 | 4.66 | 4.70 | 4.19 | 4.98 | 3.12 |
| PS142c | 8.02 [7.70, 8.31] | 4.95 | 4.92 | 4.75 | 4.67 | 4.48 | 5.00 | 2.47 |
| PS14g | 7.86 [7.53, 8.20] | 4.77 | 4.73 | 4.64 | 4.73 | 4.36 | 4.98 | 2.62 |

| paired | diff [95% CI] | better/worse/tie |
|---|---|---|
| PS142c − U | +2.53 [+1.17, +4.02] | 9/1/6 |
| PS142c − O | +0.58 [+0.19, +1.02] | 9/2/5 |
| PS142c − HS | +0.61 [+0.20, +1.09] | 8/2/6 |
| PS142c − PS14g | +0.16 [-0.12, +0.48] | 5/5/6 |

| sample | U | O | HS | PS142c | PS14g |
|---|---|---|---|---|---|
| m01_talk_abstract | 2.00 | 7.25 | 6.50 | 9.00 | 7.25 |
| m02_real_estate_listing | 2.00 | 7.25 | 6.50 | 7.50 | 7.25 |
| m03_museum_label | 2.00 | 6.75 | 6.00 | 8.75 | 7.50 |
| m04_hr_policy_email | 2.50 | 7.75 | 7.75 | 8.00 | 8.25 |
| m05_travel_itinerary | 2.25 | 7.50 | 7.25 | 8.50 | 7.50 |
| m06_scifi_scene | 3.75 | 6.00 | 6.00 | 7.75 | 8.00 |
| m07_nearclean_review | 9.00 | 9.00 | 9.00 | 8.75 | 8.50 |
| m08_nearclean_school_email | 7.75 | 7.75 | 7.75 | 8.25 | 9.00 |
| m09_nearclean_standup | 8.00 | 9.00 | 8.75 | 8.50 | 9.00 |
| m10_nearclean_memoir | 8.75 | 8.75 | 8.75 | 8.75 | 9.00 |
| m11_human_thoreau | 7.25 | 7.25 | 7.25 | 7.25 | 7.25 |
| m12_human_chesterton | 7.50 | 7.25 | 7.50 | 7.50 | 7.50 |
| m13_human_lincoln | 7.00 | 7.00 | 7.00 | 7.00 | 7.00 |
| m14_human_eisenhower | 7.00 | 7.00 | 7.00 | 7.00 | 7.00 |
| m15_human_kubernetes | 3.25 | 5.75 | 7.75 | 8.00 | 8.00 |
| m16_human_go_errors | 7.75 | 7.75 | 7.75 | 7.75 | 7.75 |

issue counts (all passes):
  U: under_edit=47
  O: added_fact=9, changed_fact=16, dropped_fact=12, format_damage=2, other=18, under_edit=18
  HS: added_fact=5, changed_fact=3, dropped_fact=22, other=9, over_edit=3, under_edit=22, voice_loss=6
  PS142c: dropped_fact=2, other=20, over_edit=1, under_edit=18, voice_loss=1
  PS14g: added_fact=4, changed_fact=4, dropped_fact=11, other=14, over_edit=8, under_edit=13, voice_loss=6
