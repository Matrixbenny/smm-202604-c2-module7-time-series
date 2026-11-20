"""
Our group's additions to the lab package, for the JPM forecast.

Everything here builds on tslab.features without changing it, so the
lecturer's notebooks keep working exactly as before.

What we add, and why
--------------------
JPM is a bank. The provided predictors include a TECHNOLOGY sector fund
(XLK), which is the natural peer group for a tech stock such as NVDA but not
for a bank. We therefore add the FINANCIAL sector fund (XLF, column "FIN"
in data/predictors.csv) as a new predictor group, "sector_fin":

    FIN_ret_1d            the financial sector's return today
    FIN_ret_5d            the financial sector's return over the past week
    relative_to_FIN_5d    did JPM beat its own sector this week?

All three use values known at the close of day t, the same timing rule as
every other predictor in build_features, so they are known BEFORE the day
that we forecast (t+1). check_no_lookahead(frame, build_features_jpm)
proves this, and Notebook lab_1 runs that check.

Every notebook in our submission imports from here:

    from tslab.team import build_features_jpm, make_dataset_jpm, \
        FEATURE_GROUPS_JPM, ALL_FEATURES_JPM
"""

import numpy as np

from .features import FEATURE_GROUPS, build_features, log_return

SECTOR_PREDICTOR = "FIN"


def build_features_jpm(frame):
    """The Notebook 4 feature table plus the financial-sector group."""
    out = build_features(frame)
    out["FIN_ret_1d"] = log_return(frame[SECTOR_PREDICTOR], 1)
    out["FIN_ret_5d"] = log_return(frame[SECTOR_PREDICTOR], 5)
    out["relative_to_FIN_5d"] = out["ret_5d"] - out["FIN_ret_5d"]
    return out


FEATURE_GROUPS_JPM = {
    **FEATURE_GROUPS,
    "sector_fin": ["FIN_ret_1d", "FIN_ret_5d", "relative_to_FIN_5d"],
}

ALL_FEATURES_JPM = [name for group in FEATURE_GROUPS_JPM.values() for name in group]


def make_dataset_jpm(frame, horizon=1):
    """
    Same as tslab.features.make_dataset, but with our feature table.

    Returns the features, `close` (known on day t), `target_close` (the close
    on day t+horizon) and `target_return` (the log return from t to
    t+horizon, which is what every model predicts). The last `horizon` rows
    have no target yet; drop them before training with
    dataset.dropna(subset=["target_return"]).
    """
    features = build_features_jpm(frame)
    data = features.copy()
    data["close"] = frame["Close"]
    # The only negative shift in the project: these are the ANSWERS, not inputs.
    data["target_close"] = frame["Close"].shift(-horizon)
    data["target_return"] = np.log(frame["Close"].shift(-horizon) / frame["Close"])
    data = data.replace([np.inf, -np.inf], np.nan)
    feature_ready = data[ALL_FEATURES_JPM].notna().all(axis=1)
    return data[feature_ready]
