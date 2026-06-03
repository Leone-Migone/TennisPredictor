import pandas as pd
from pathlib import Path

def load_data() -> pd.DataFrame:
    """
    load data for matches
    datas:

    tourney_id: Unique tournament identifier, usually formatted as Year-ID.
    tourney_name: Official name of the tournament.
    surface: Court material type (Hard, Clay, Grass, Carpet).
    draw_size: Total number of players in the tournament bracket.
    tourney_level: Tournament category (G=Grand Slam, M=Masters, A=Tour-level, D=Davis Cup, F=Tour Finals).
    tourney_date: Start date of the tournament week (YYYYMMDD).
    match_num: Chronological match number within the tournament draw.
    winner_id: Unique database identifier for the winning player.
    winner_seed: Tournament seeding assigned to the winner.
    winner_entry: Winner's entry method (Q=Qualifier, WC=Wild Card, LL=Lucky Loser, PR=Protected Ranking).
    winner_name: Full name of the winning player.
    winner_hand: Dominant hand of the winner (R=Right, L=Left, U=Unknown).
    winner_ht: Height of the winner in centimeters.
    winner_ioc: Three-letter country code (IOC) for the winner.
    winner_age: Age of the winner at the start of the tournament.
    loser_id: Unique database identifier for the losing player.
    loser_seed: Tournament seeding assigned to the loser.
    loser_entry: Loser's entry method (Q=Qualifier, WC=Wild Card, LL=Lucky Loser, PR=Protected Ranking).
    loser_name: Full name of the losing player.
    loser_hand: Dominant hand of the loser (R=Right, L=Left, U=Unknown).
    loser_ht: Height of the loser in centimeters.
    loser_ioc: Three-letter country code (IOC) for the loser.
    loser_age: Age of the loser at the start of the tournament.
    score: Final match score.
    best_of: Maximum number of sets possible in the match (3 or 5).
    round: Tournament round (e.g., R128, R64, QF, SF, F).
    minutes: Total match duration in minutes.
    w_ace: Number of aces served by the winner.
    w_df: Number of double faults committed by the winner.
    w_svpt: Total service points played by the winner.
    w_1stIn: Number of first serves made into the box by the winner.
    w_1stWon: Total service points won on first serve by the winner.
    w_2ndWon: Total service points won on second serve by the winner.
    w_SvGms: Total number of service games played by the winner.
    w_bpSaved: Number of break points successfully saved by the winner.
    w_bpFaced: Total number of break points faced by the winner.
    l_ace: Number of aces served by the loser.
    l_df: Number of double faults committed by the loser.
    l_svpt: Total service points played by the loser.
    l_1stIn: Number of first serves made into the box by the loser.
    l_1stWon: Total service points won on first serve by the loser.
    l_2ndWon: Total service points won on second serve by the loser.
    l_SvGms: Total number of service games played by the loser.
    l_bpSaved: Number of break points successfully saved by the loser.
    l_bpFaced: Total number of break points faced by the loser.
    winner_rank: Official singles ranking of the winner at the start of the tournament.
    winner_rank_points: Ranking points held by the winner at the start of the tournament.
    loser_rank: Official singles ranking of the loser at the start of the tournament.
    loser_rank_points: Ranking points held by the loser at the start of the tournament.
    
    """
    df = []
    dDirectory = Path(__file__).resolve().parent.parent / "data" / "tennis_atp"
    startY = 2010
    endY = 2026
    for year in range(startY, endY + 1):
        file_path = dDirectory / f"atp_matches_{year}.csv"
        if not file_path.exists():
            raise FileNotFoundError(f"Missing file: {file_path}")
        df.append(pd.read_csv(file_path))
    
    matches = pd.concat(df, ignore_index=True)
    return matches



    
