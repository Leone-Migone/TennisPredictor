from collections import defaultdict, deque
from dataclasses import dataclass, field

import pandas as pd


@dataclass
class HeadToHeadHistory:
    wins: dict = field(
        default_factory=lambda: defaultdict(lambda: defaultdict(int))
    )

    @staticmethod
    def matchup_key(player_1, player_2):
        return tuple(sorted((player_1, player_2), key=str))

    def before_match(self, player_1, player_2):
        matchup = self.wins[self.matchup_key(player_1, player_2)]
        player_1_wins = matchup[player_1]
        player_2_wins = matchup[player_2]

        return (
            player_1_wins - player_2_wins,
            player_1_wins + player_2_wins,
        )

    def update(self, player_1, player_2, player_1_won):
        winner = player_1 if player_1_won else player_2
        self.wins[self.matchup_key(player_1, player_2)][winner] += 1


@dataclass
class RecentFormHistory:
    window: int = 10
    neutral_form: float = 0.5
    results: dict = field(default_factory=dict)

    def form(self, player_id):
        history = self.results.get(player_id)

        if not history:
            return self.neutral_form

        return sum(history) / len(history)

    def update(self, player_1, player_2, player_1_won):
        for player in (player_1, player_2):
            self.results.setdefault(player, deque(maxlen=self.window))

        self.results[player_1].append(int(player_1_won))
        self.results[player_2].append(int(not player_1_won))


@dataclass
class RestHistory:
    unseen_days: int = 30
    last_match: dict = field(default_factory=dict)

    def days(self, player_id, match_date: pd.Timestamp):
        previous_date = self.last_match.get(player_id)

        if previous_date is None:
            return self.unseen_days

        return (match_date - previous_date).days

    def update(self, player_1, player_2, match_date):
        self.last_match[player_1] = match_date
        self.last_match[player_2] = match_date