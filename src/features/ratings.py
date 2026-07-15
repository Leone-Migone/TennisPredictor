from dataclasses import dataclass, field


@dataclass
class EloRatings:
    initial_rating: float = 1500.0
    k_factor: float = 32.0
    ratings: dict[object, float] = field(default_factory=dict)

    def rating(self, player_id: object) -> float:
        return self.ratings.get(player_id, self.initial_rating)

    def expected_score(self, player_1: object, player_2: object) -> float:
        difference = self.rating(player_2) - self.rating(player_1)
        return 1.0 / (1.0 + 10.0 ** (difference / 400.0))

    def update(
        self,
        player_1: object,
        player_2: object,
        player_1_won: bool,
    ) -> None:
        rating_1 = self.rating(player_1)
        rating_2 = self.rating(player_2)
        expected_1 = self.expected_score(player_1, player_2)

        score_1 = float(player_1_won)
        change = self.k_factor * (score_1 - expected_1)

        self.ratings[player_1] = rating_1 + change
        self.ratings[player_2] = rating_2 - change


@dataclass
class SurfaceEloRatings:
    initial_rating: float = 1500.0
    k_factor: float = 32.0
    ratings_by_surface: dict[str, EloRatings] = field(default_factory=dict)

    def for_surface(self, surface: str) -> EloRatings:
        normalized_surface = str(surface).strip().lower()

        if normalized_surface not in self.ratings_by_surface:
            self.ratings_by_surface[normalized_surface] = EloRatings(
                initial_rating=self.initial_rating,
                k_factor=self.k_factor,
            )

        return self.ratings_by_surface[normalized_surface]