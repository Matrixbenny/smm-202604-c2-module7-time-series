# Module 7 â€” branch state and submission status

Written 22 Nov, after a check of every branch. Update this if the state changes.

## The mistake worth avoiding

On **21 Nov at 17:05**, `main` was reset to `4dc350d` â€” the group scaffold commit
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
| Stock in use                          | **JPM** (2,989 rows, 2015-01-02 -> 2026-11-19)        |
| Predictors in use                     | 8 (the seven provided + **XLF**, Member 1's addition) |

## Branch status

| Member | Branch                                 | State                                                                                                                    |
| :----- | :------------------------------------- | :----------------------------------------------------------------------------------------------------------------------- |
| 1      | `feature/member1-data-stationarity`    | Lab 1 complete and on `main`; branch pointer itself was left at the scaffold because of the reset                        |
| 2      | `feature/member2-classical-models`     | merged                                                                                                                   |
| 3      | `feature/member3-machine-learning`     | merged                                                                                                                   |
| 4      | `feature/member4-uncertainty-horizons` | unblocked â€” `outputs/predictions_classical.csv` and `predictions_ml.csv` are on `main` with an identical 2,789-row index |
| 5      | `feature/member5-neural-networks`      | not started                                                                                                              |
| 6      | `feature/member6-backtest-powerbi`     | not started                                                                                                              |

## Still outstanding before submission

1. **The written verdict** â€” the section still says _"To be written by the team after Labs 3, 4 and 6
   are final"_. This is rubric row 7 (10 marks) and cannot be faked: it must state plainly whether the
   models beat the naive forecast.
2. **Member 1's contribution row no longer claims the verdict** â€” it claimed _"wrote the verdict"_ while
   that section was still empty. Corrected to the coordination work actually done.
3. **ARIMA is mislabelled.** `predictions_classical.csv`'s `ARIMA` column is `0.000000` on 1,787 of
   1,789 days â€” it is the naive forecast under another name. Either the model needs fixing or the
   report must not describe it as ARIMA. `AR(1,0)` and `ARMAX` are genuinely different.
4. **Download date** â€” the submission claimed _"data from 2 January 2015 to 19 November 2026"_, but the
   committed JPM snapshot ends **29 October 2026**. Corrected to say so; the real date must be confirmed.
5. **CSV files.** `data/forecast_basic.csv`, `forecast_intermediate.csv` and `forecast_advanced.csv` do
   not exist yet.
6. **Power BI** â€” `powerbi/` is empty.
7. **Video** â€” not recorded. Must be **<= 4 minutes** (not 10 as in Module 6).

## Reproducibility check (22 Nov)

All four examinable notebooks were re-executed from a clean kernel on `main`:
`lab_1` 13 cells, `lab_2` 24, `lab_3` 20, `lab_4` 22 - **0 errors each**.

Re-running regenerates the outputs. The **core metrics reproduce** to 13 significant figures
(price RMSE, MAE, out-of-sample R2, directional accuracy - e.g. Ridge 2.9724529084 vs
2.9724529084). Two things drift slightly:

| Item | Committed | Re-run | Changes a conclusion? |
| :--- | :--- | :--- | :--- |
| ARIMA DM p | 0.2259 | 0.1746 | No - both far above 0.05 |
| Gradient boosting DM p | 0.0783 | 0.1402 | No - both above 0.05 |
| ARMAX DM p | 0.3004 | 0.3048 | No |
| Ridge DM p | 0.8140 | 0.8140 | No - identical |
| Drift DM p | 0.6809 | 0.6809 | No - identical |

Cause: the Diebold-Mariano statistic depends on the long-run variance estimate, which is sensitive
to floating-point accumulation order, and the neural networks depend on framework-level randomness
beyond the seed. **Every headline number in the written verdict holds in both runs**: no model beats
the naive forecast, Ridge p = 0.81, Drift p = 0.68, LSTM p = 0.0002, coverage 79.8% at 1 day and
66.6% at 63 days, and the 63-day forecast of 344.19 with range 296.17-390.33.

**Do not commit regenerated `outputs/` or `data/forecast_*.csv` unless you also update the verdict**,
or the document and the files will disagree.
