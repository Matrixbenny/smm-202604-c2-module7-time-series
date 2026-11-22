# Module 7 — branch state and submission status

Written 22 Nov, after a check of every branch. Update this if the state changes.

## The mistake worth avoiding

On **21 Nov at 17:05**, `main` was reset to `4dc350d` — the group scaffold commit
_"Add starter notebooks for Members 3 to 6"_, built on the course starter. This **orphaned Member 1's
commit `4dc350d`** (20 Nov, _"Set up JPM data, team features, Lab 1 and the Lab 2 starter"_) from the
first-parent line of `main`.

Practical effect:

- **No file was lost.** `main` still contains Member 1's `lab_1_data_and_stationarity.ipynb`,
  `data/target_JPM.csv`, `tslab/team.py`, `tslab/config.py` and `tests/test_team.py`, and the notebooks
  still run on JPM with 8 predictor series.
- **The history was rewritten.** `main` now traces back to the starter, not to Member 1's work. Anyone
  reading `git log` sees Member 2 and Member 3's commits as the beginning.

Nobody should reset or force-push `main` again. Member 1's original tip is recoverable as:
`git branch member1-recovered 4dc350d`.

## Verified on `main` at the time of writing

| Check                                 | Result                                                |
| :------------------------------------ | :---------------------------------------------------- |
| `lab_1_data_and_stationarity.ipynb`   | 13 code cells, runs clean, 0 errors                   |
| `lab_2_classical_models.ipynb`        | runs clean, 0 errors                                  |
| `lab_3_machine_learning_models.ipynb` | runs clean, 0 errors                                  |
| `pytest tests`                        | 11 passed                                             |
| Stock in use                          | **JPM** (2,990 rows, 2015-01-02 -> 2026-10-29)        |
| Predictors in use                     | 8 (the seven provided + **XLF**, Member 1's addition) |

## Branch status

| Member | Branch                                 | State                                                                                                                    |
| :----- | :------------------------------------- | :----------------------------------------------------------------------------------------------------------------------- |
| 1      | `feature/member1-data-stationarity`    | Lab 1 complete and on `main`; branch pointer itself was left at the scaffold because of the reset                        |
| 2      | `feature/member2-classical-models`     | merged                                                                                                                   |
| 3      | `feature/member3-machine-learning`     | merged                                                                                                                   |
| 4      | `feature/member4-uncertainty-horizons` | unblocked — `outputs/predictions_classical.csv` and `predictions_ml.csv` are on `main` with an identical 2,789-row index |
| 5      | `feature/member5-neural-networks`      | not started                                                                                                              |
| 6      | `feature/member6-backtest-powerbi`     | not started                                                                                                              |

## Still outstanding before submission

1. **The written verdict** — the section still says _"To be written by the team after Labs 3, 4 and 6
   are final"_. This is rubric row 7 (10 marks) and cannot be faked: it must state plainly whether the
   models beat the naive forecast.
2. **Member 1's contribution row no longer claims the verdict** — it claimed _"wrote the verdict"_ while
   that section was still empty. Corrected to the coordination work actually done.
3. **ARIMA is mislabelled.** `predictions_classical.csv`'s `ARIMA` column is `0.000000` on 1,787 of
   1,789 days — it is the naive forecast under another name. Either the model needs fixing or the
   report must not describe it as ARIMA. `AR(1,0)` and `ARMAX` are genuinely different.
4. **Download date** — the submission claimed _"data from 2 January 2015 to 19 November 2026"_, but the
   committed JPM snapshot ends **29 October 2026**. Corrected to say so; the real date must be confirmed.
5. **CSV files.** `data/forecast_basic.csv`, `forecast_intermediate.csv` and `forecast_advanced.csv` do
   not exist yet.
6. **Power BI** — `powerbi/` is empty.
7. **Video** — not recorded. Must be **<= 4 minutes** (not 10 as in Module 6).
