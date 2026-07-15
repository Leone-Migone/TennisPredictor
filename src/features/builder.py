"""Build model-ready rows using only information available before each match."""

import numpy as np
import pandas as pd

from .history import HeadToHeadHistory, RecentFormHistory, RestHistory
from .ratings import EloRatings, SurfaceEloRatings


REQUIRED_COLUMNS = [
    "tourney_date", "match_num", "winner_name", "winner_id", "loser_name",
    "loser_id", "winner_rank", "loser_rank", "winner_age", "loser_age",
    "surface", "best_of", "winner_rank_points", "loser_rank_points",
]


def _orient_matches(matches: pd.DataFrame, random_state: int) -> pd.DataFrame:
    missing = sorted(set(REQUIRED_COLUMNS) - set(matches.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    data = matches[REQUIRED_COLUMNS].copy()
    rng = np.random.default_rng(random_state)
    data["target"] = rng.integers(0, 2, size=len(data))

    for field in ("id", "name", "rank", "age", "rank_points"):
        winner = data[f"winner_{field}"]
        loser = data[f"loser_{field}"]
        data[f"player_1_{field}"] = np.where(data["target"].eq(1), winner, loser)
        data[f"player_2_{field}"] = np.where(data["target"].eq(1), loser, winner)

    data = data.dropna(subset=[
        "player_1_id", "player_2_id", "player_1_rank", "player_2_rank",
        "player_1_age", "player_2_age", "player_1_rank_points",
        "player_2_rank_points", "surface",
    ])
    return data.sort_values(["tourney_date", "match_num"], kind="stable").reset_index(drop=True)


def build_model_data(matches: pd.DataFrame, random_state: int = 1) -> pd.DataFrame:
    data = _orient_matches(matches, random_state)
    h2h = HeadToHeadHistory()
    form = RecentFormHistory()
    rest = RestHistory()
    general_elo = EloRatings()
    surface_elos = SurfaceEloRatings()
    generated: list[dict[str, float]] = []

    for row in data.itertuples(index=False):
        player_1, player_2 = row.player_1_id, row.player_2_id
        player_1_won = bool(row.target)
        date = pd.to_datetime(str(int(row.tourney_date)), format="%Y%m%d")
        surface_elo = surface_elos.for_surface(row.surface)
        h2h_diff, h2h_matches = h2h.before_match(player_1, player_2)

        generated.append({
            "h2h_diff": h2h_diff,
            "h2h_matches": h2h_matches,
            "form_diff": form.form(player_1) - form.form(player_2),
            "surface_elo_diff": surface_elo.rating(player_1) - surface_elo.rating(player_2),
            "general_elo_diff": general_elo.rating(player_1) - general_elo.rating(player_2),
            "rest_days_diff": rest.days(player_1, date) - rest.days(player_2, date),
        })

        h2h.update(player_1, player_2, player_1_won)
        form.update(player_1, player_2, player_1_won)
        surface_elo.update(player_1, player_2, player_1_won)
        general_elo.update(player_1, player_2, player_1_won)
        rest.update(player_1, player_2, date)

    features = pd.DataFrame(generated, index=data.index)
    data = pd.concat([data, features], axis=1)
    data["rank_diff"] = data["player_1_rank"] - data["player_2_rank"]
    data["age_diff"] = data["player_1_age"] - data["player_2_age"]
    data["rank_points_diff"] = data["player_1_rank_points"] - data["player_2_rank_points"]
    return data

