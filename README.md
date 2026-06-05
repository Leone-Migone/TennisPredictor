# TennisPredictor
This project aims to build a tennis match prediction system using historical ATP match data. The main goal is to explore how player performance, tournament conditions, rankings, and match history can be used to estimate the likely winner of a match. My inspiration for this project came from the youtube channel Green Code.
## Project LogBook   
04/06/2026 For my first approach this project I decided to initially just use a limited database to then increment progressively the complexity and techicality of the system. I started by defining the repository structure, import the csvs containing the data and starting the preprocessing
05/06/2026 developed basic idea of evaluation model, i decided to keep it simple initially taking only account of difference in ranking, difference in age, surface of the court and the number of set needed in order to win (3,5) using a logistic regression. with this first model I'm getting a fairly solid first baseline.  


## Models
#### 1.Baseline Logistic Regression
The baseline model used only a small number of pre-match features:
- `rank_diff`: difference between player 1's ATP ranking and player 2's ATP ranking
- `age_diff`: difference between player 1's age and player 2's age
- `surface`: court surface, one-hot encoded
- `best_of`: whether the match was best of 3 or best of 5 sets
Accuracy: 66%

### Results

The baseline Logistic Regression model achieved an accuracy of approximately **66%** on the test set.

| Class | Meaning | Precision | Recall | F1-score | Support |
|---|---|---:|---:|---:|---:|
| 0 | Player 1 lost | 0.66 | 0.64 | 0.65 | 4552 |
| 1 | Player 1 won | 0.65 | 0.68 | 0.67 | 4624 |

Overall accuracy: **0.66**

### Logistic Regression with Head-to-Head Features

A second version of the Logistic Regression model was trained by adding two head-to-head features:

- `h2h_diff`: previous wins by player 1 against player 2 minus previous wins by player 2 against player 1
- `h2h_matches`: total number of previous meetings between the two players

These features were calculated chronologically, meaning that only matches played before the current match were used. This avoids data leakage.

However, the model accuracy decreased slightly from approximately **66%** to **65%**.

| Model | Features | Accuracy |
|---|---|---:|
| Baseline Logistic Regression | rank_diff, age_diff, surface, best_of | 0.66 |
| Logistic Regression + H2H | + h2h_diff, h2h_matches | 0.65 |

This suggests that simple head-to-head features did not improve performance for this model. One reason may be that many player pairings have no previous meetings, meaning the H2H values are often zero. Another reason is that older head-to-head results may not reflect the players' current ability.

### Interpretation

The model performs reasonably well for a first baseline, correctly predicting around 66% of match outcomes using only ranking difference, age difference, surface, and match format. The precision, recall, and F1-scores are similar for both classes, suggesting that the model is not heavily biased towards predicting only wins or only losses.

### Logistic Regression with H2H and Ranking Points Difference
This version added one feature to the previous baseline:
- `rank_points_diff`: difference between player 1 and player 2's ATP ranking points

The ranking points feature was added because ATP ranking positions do not always reflect the true gap between players. For example, the points gap between rank 1 and rank 2 can be much larger than the gap between rank 50 and rank 51.  

| Model | Features Added | Accuracy |
|---|---|---:|
| Baseline Logistic Regression | rank_diff, age_diff, surface, best_of | 0.66 |
| Logistic Regression + H2H | h2h_diff, h2h_matches | 0.65 |
| Logistic Regression + H2H + Rank Points | rank_points_diff | 0.6610 |

### Time-Based Model Comparison and introduction of Random Forest

After initially testing models using a random train/test split, a chronological split was introduced to better reflect a real prediction scenario. Matches before 2024 were used for training, while matches from 2024 onwards were used for testing.

| Model | Split Type | Accuracy |
|---|---|---:|
| Logistic Regression | Random split | 0.661 |
| Logistic Regression | Time-based split | 0.641213 |
| Random Forest | Time-based split | 0.624876 |

The time-based split produced lower accuracy than the random split, which is expected because it prevents the model from training on future matches. Logistic Regression performed slightly better than Random Forest on the current feature set, suggesting that the current features mainly provide linear predictive signals, particularly ranking difference and ranking points difference.

## Notes: Ideas, thought process
### Head to Head
from our baseline model, first feature I'm thinking would be important to add is a way to track the players head-to-head, since players can be really good and higher ranked than certain oppenent but still suffer their particular playstile and so lose against them, an example could be Felix Auger-Aliassime against Cobolli, Cobolli has never held a higher ATP ranking than FAA, but is known to be one of FAA's weaknesses and has never lost against the latter.

### ELO system
I thought an elo system could be a good idea to improve the quality of the predictive model, this for 2 main reasons:  
1. the ATP ranking points, even if they could be seen as a sort of ELO system equivalent system, do not alway correctly indicate the level of ability of a player, this because they are based on the previous year results, compared to their performance in each tournament this season, whether they have to defends the points gained the previous year or attempt to gain more by going further (compared to the previous year) in the tournament.
2. Secondly, court surface has a major impact on tennis performance. Some players perform much better on certain surfaces than others, so using only one general rating could hide important differences in ability. For this reason, I am planning to create separate Elo ratings for each surface type:

- `hElo`: hard court Elo
- `gElo`: grass court Elo
- `cElo`: clay court Elo

#### How does ELO work?
Elo is a rating system used to estimate the relative strength of two players. Each player starts with an initial rating, for example 1500. Before a match, the difference between the two players' ratings is used to calculate the expected probability of each player winning. After the match, the winner gains rating points and the loser loses rating points. The amount gained or lost depends on how surprising the result was: beating a much lower-rated player gives only a small increase, while beating a much higher-rated player gives a larger increase.

The expected score for player A is calculated as:

`E_A = 1 / (1 + 10^((R_B - R_A) / 400))`

where `R_A` is player A's rating and `R_B` is player B's rating.

After the match, player A's rating is updated using:

`R_A_new = R_A + K * (S_A - E_A)`

where `R_A_new` is the new rating, `K` controls how quickly ratings change, `S_A` is the actual result of the match, with `1` for a win and `0` for a loss, and `E_A` is the expected score before the match.
