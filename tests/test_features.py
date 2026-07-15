import pytest

from src.features.history import HeadToHeadHistory
from src.features.ratings import EloRatings, SurfaceEloRatings


def test_equal_players_begin_with_equal_probability():
    elo = EloRatings()

    assert elo.expected_score("player-a", "player-b") == pytest.approx(0.5)


def test_elo_update_is_zero_sum():
    elo = EloRatings()

    elo.update("player-a", "player-b", player_1_won=True)

    assert elo.rating("player-a") == pytest.approx(1516)
    assert elo.rating("player-b") == pytest.approx(1484)
    assert elo.rating("player-a") + elo.rating("player-b") == pytest.approx(3000)


def test_surface_ratings_are_independent():
    ratings = SurfaceEloRatings()

    ratings.for_surface("Hard").update("a", "b", True)

    assert ratings.for_surface("Hard").rating("a") > 1500
    assert ratings.for_surface("Clay").rating("a") == 1500


def test_h2h_contains_only_previous_matches():
    history = HeadToHeadHistory()

    assert history.before_match("a", "b") == (0, 0)

    history.update("a", "b", True)

    assert history.before_match("a", "b") == (1, 1)