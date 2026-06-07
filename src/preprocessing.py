import pandas as pd
import numpy as np
from pathlib import Path
def create_model_data(data):
    # drop these columns since a lot of values are missing
    processed_data = data.drop(columns=['loser_seed', 'winner_entry', 'loser_entry', 'winner_seed'])
    # drop matches with no recorded stats
    #processed_data = processed_data.dropna(subset=['w_ace'])
    # fill with meadian the categories that are missing just a couple hundred values, and that wont matter too match in elo calculation
    #cols_tofill = ['winner_ht', 'loser_ht', 'winner_age', 'loser_age', 'winner_rank', 'loser_rank']
    #processed_data[cols_tofill] = processed_data[cols_tofill].fillna(processed_data[cols_tofill].median())


    #FOR NOW ONLY USING THIS SIMPLIFIED DATABASE
    selected_cols = [
        "tourney_date",
        "match_num",
        "winner_name",
        "winner_id",
        "loser_name",
        "loser_id",
        "winner_rank",
        "loser_rank",
        "winner_age",
        "loser_age",
        "surface",
        "best_of",
        "winner_rank_points",
        "loser_rank_points"
    ]
    
    data = processed_data[selected_cols].copy()

    np.random.seed(1)
    orientation = np.random.randint(0, 2, size=len(data))
    # If orientation == 1, player_1 is winner
    # If orientation == 0, player_1 is loser
    data["target"] = orientation

    data["player_1_id"] = np.where(data["target"] == 1, data["winner_id"], data["loser_id"])
    data["player_1_name"] = np.where(data["target"] == 1, data["winner_name"], data["loser_name"])
    data["player_1_rank"] = np.where(data["target"] == 1, data["winner_rank"], data["loser_rank"])
    data["player_1_age"] = np.where(data["target"] == 1, data["winner_age"], data["loser_age"])
    data["player_1_rank_points"] = np.where(data["target"] == 1, data["winner_rank_points"], data["loser_rank_points"])
    
    
    data["player_2_id"] = np.where(data["target"] == 1, data["loser_id"], data["winner_id"])
    data["player_2_name"] = np.where(data["target"] == 1, data["loser_name"], data["winner_name"])
    data["player_2_rank"] = np.where(data["target"] == 1, data["loser_rank"], data["winner_rank"])
    data["player_2_age"] = np.where(data["target"] == 1, data["loser_age"], data["winner_age"])
    data["player_2_rank_points"] = np.where(data["target"] == 1, data["loser_rank_points"], data["winner_rank_points"])
    

    # Difference features
    data["rank_diff"] = data["player_1_rank"] - data["player_2_rank"]
    data["age_diff"] = data["player_1_age"] - data["player_2_age"]
    #difference in atp points, since ranking sometimes dont fully reflect the gap that there can be between two positions
    data["rank_points_diff"] = data["player_1_rank_points"] - data["player_2_rank_points"]

    # Final clean dataframe
    final_cols = [
        "tourney_date",
        "match_num",
        "player_1_id",
        "player_1_name",
        "player_2_id",
        "player_2_name",
        "player_1_rank",
        "player_2_rank",
        "player_1_age",
        "player_2_age",
        "rank_diff",
        "age_diff",
        "surface",
        "best_of",
        "target",
        "player_1_rank_points",
        "player_2_rank_points",
        "rank_points_diff"
    ]
    
    # Drop rows with missing values in critical columns
    data = data.dropna(subset=["player_1_rank", "player_2_rank","player_1_age", "player_2_age", "rank_diff", "age_diff", "surface","rank_points_diff","player_1_rank_points","player_2_rank_points"])
    
    #order matches by date and match number
    data = data.sort_values(by=["tourney_date", "match_num"])
    clean_data = data[final_cols].copy()

    p1_h2h_wins = []
    p2_h2h_wins = []

    p1_form = []
    p2_form = []

    p1_recent_matches = []
    p2_recent_matches = []

    #dictionary that tracks head to heads
    h2h_tracker = {}
    #dictionary that tracks player form
    form_tracker = {}
    #dictionary that tracks players ELO
    ELO_tracker = {}

    p1ELO = 0
    p2ELO = 0



    for i, row in clean_data.iterrows():
        p1 = row["player_1_id"]
        p2 = row["player_2_id"]
        target = row["target"]
        
        
        #key to search up rivalry
        #Sorting them ensures the matchup key is the same regardless of whos p1 or p2    
        matchup_k = tuple(sorted([p1,p2]))
        
        #if not played before
        if p1 not in form_tracker:
            form_tracker[p1] = []
        if p2 not in form_tracker:
            form_tracker[p2] = []

        if p1 not in ELO_tracker:
            ELO_tracker[p1] = 1500
        if p2 not in ELO_tracker:
            ELO_tracker[p2] = 1500

        #get last 10 results
        p1_ten = form_tracker[p1][-10:]
        p2_ten = form_tracker[p2][-10:]

        #no history use neutral form
        if len(p1_ten) == 0:
            p1_current_form = 0.5
        else:
            p1_current_form = sum(p1_ten) / len(p1_ten)

        if len(p2_ten) == 0:
            p2_current_form = 0.5
        else:
            p2_current_form = sum(p2_ten) / len(p2_ten)
        
        p1_form.append(p1_current_form)
        p2_form.append(p2_current_form)


        p1_recent_matches.append(len(p1_ten))
        p2_recent_matches.append(len(p2_ten))

        #initialize to 0
        if matchup_k not in h2h_tracker:
            h2h_tracker[matchup_k] = { p1: 0, p2: 0 }
        
        # record win till now
        p1_h2h_wins.append(h2h_tracker[matchup_k][p1])
        p2_h2h_wins.append(h2h_tracker[matchup_k][p2])

        p1ELO = ELO_tracker[p1]
        p2ELO = ELO_tracker[p2]

        #expected probability based on ELO
        E_a = 1 / (1 + 10**((p2ELO-p1ELO)/400))
        

        # update the tracker with the result of this match for the future
        if target == 1:
            h2h_tracker[matchup_k][p1] += 1
            form_tracker[p1].append(1)
            form_tracker[p2].append(0)
            #update ELO with match result
            ELO_tracker[p1] = p1ELO + 32 * (1 - E_a) 
            ELO_tracker[p2] = p2ELO + 32 * (0 - E_a)

        else:
            h2h_tracker[matchup_k][p2] += 1
            form_tracker[p1].append(0)
            form_tracker[p2].append(1)
            ELO_tracker[p1] = p1ELO + 32 * (0 - E_a) 
            ELO_tracker[p2] = p2ELO + 32 * (1 - E_a)

        

    clean_data['p1_historical_h2h_wins'] = p1_h2h_wins
    clean_data['p2_historical_h2h_wins'] = p2_h2h_wins
    #calculate difference in head to head
    clean_data['h2h_diff'] = clean_data["p1_historical_h2h_wins"] - clean_data["p2_historical_h2h_wins"]
    #number of head to head matches
    clean_data['h2h_matches'] = clean_data["p1_historical_h2h_wins"] + clean_data["p2_historical_h2h_wins"]
    clean_data['p1_form'] = p1_form
    clean_data['p2_form'] = p2_form
    clean_data["form_diff"] = clean_data['p1_form'] - clean_data['p2_form']
    #elo for each player and helo diff
    clean_data["p1_elo"] = ELO_tracker[p1]
    clean_data["p2_elo"] = ELO_tracker[p2]
    clean_data["elo_diff"] = clean_data["p1_elo"] - clean_data["p2_elo"]
    clean_data = clean_data.reset_index(drop=True)


    return clean_data
