"""Checks for our group's additions in tslab/team.py."""

import numpy as np
import pandas as pd

from tslab.features import check_no_lookahead
from tslab.team import ALL_FEATURES_JPM, FEATURE_GROUPS_JPM, build_features_jpm, make_dataset_jpm


def _synthetic_frame(n=400, seed=0):
    rng = np.random.default_rng(seed)
    index = pd.bdate_range("2020-01-01", periods=n)
    close = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, n)))
    frame = pd.DataFrame(index=index)
    frame["Close"] = close
    frame["Open"] = close * (1 + rng.normal(0, 0.002, n))
    frame["High"] = np.maximum(frame["Open"], close) * 1.01
    frame["Low"] = np.minimum(frame["Open"], close) * 0.99
    frame["Volume"] = rng.integers(1_000_000, 2_000_000, n).astype(float)
    for name in ["SP500", "TECH", "GOLD", "BRENT", "USD", "VIX", "FIN"]:
        frame[name] = 50 * np.exp(np.cumsum(rng.normal(0, 0.01, n)))
    frame["US10Y"] = 3 + np.cumsum(rng.normal(0, 0.02, n))
    return frame


def test_sector_group_is_added_and_complete():
    features = build_features_jpm(_synthetic_frame())
    assert "sector_fin" in FEATURE_GROUPS_JPM
    assert set(ALL_FEATURES_JPM) <= set(features.columns)


def test_team_features_have_no_lookahead():
    assert check_no_lookahead(_synthetic_frame(), build_features_jpm, n_checks=5)


def test_target_is_next_day_log_return():
    frame = _synthetic_frame()
    data = make_dataset_jpm(frame)
    day = data.index[10]
    position = frame.index.get_loc(day)
    expected = np.log(frame["Close"].iloc[position + 1] / frame["Close"].iloc[position])
    assert abs(data.loc[day, "target_return"] - expected) < 1e-12
