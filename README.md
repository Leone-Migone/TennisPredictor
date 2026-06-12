# TennisPredictor
This project aims to build a tennis match prediction system using historical ATP match data. The main goal is to explore how player performance, tournament conditions, rankings, and match history can be used to estimate the likely winner of a match. My inspiration for this project came from the youtube channel Green Code.
## Project LogBook   
04/06/2026  
For my first approach this project I decided to initially just use a limited database to then increment progressively the complexity and techicality of the system. I started by defining the repository structure, import the csvs containing the data and starting the preprocessing   
  
05/06/2026  
developed basic idea of evaluation model, i decided to keep it simple initially taking only account of difference in ranking, difference in age, surface of the court and the number of set needed in order to win (3,5) using a logistic regression. with this first model I'm getting a fairly solid first baseline.   
  
06/06/2026  
Added head-to-head statistics and ATP ranking points difference. These features were computed chronologically to avoid data leakage and to simulate a realistic prediction scenario.  
  
07/06/2026  
Changed the evaluation methodology from a random train/test split to a chronological split. Matches before 2024 were used for training and matches from 2024 onward for testing, producing more realistic estimates of predictive performance.  
  
08/06/2026  
Implemented two new features:  
Recent form, based on the previous ten matches played by each player.  
Surface-specific Elo ratings (hard, clay and grass).  
Separate Elo systems were maintained for each surface and updated chronologically after every match. The addition of surface-specific Elo provided the largest improvement so far, increasing accuracy from 64.58% to 65.30%.

09/06/2026
Experimented with Random Forest as an alternative model. Despite its ability to model non-linear relationships, it performed worse than Logistic Regression on the current feature set.

This suggested that the existing features mainly provided linear predictive information.

10/06/2026
Implemented a recent-form feature based on the previous ten matches played by each player. Players with no previous matches were assigned a neutral form value of 0.5.

The addition of recent form had little impact on overall performance.

10/06/2026
Designed and implemented a surface-specific Elo system. Separate ratings were maintained for:

- Hard courts
- Clay courts
- Grass courts

For each match, only information available before that match was used to compute Elo differences. Surface Elo provided the largest improvement seen so far and highlighted the importance of court surface in tennis.

11/06/2026
Introduced a general Elo rating in addition to the surface-specific ratings. The idea was to combine overall player strength with surface specialisation.

This resulted in a further improvement and produced the best performance obtained so far.

11/06/2026
Replaced Logistic Regression with XGBoost in order to capture non-linear relationships between features. Tuned several hyperparameters, including:

- Number of trees
- Maximum tree depth
- Learning rate
- Row subsampling
- Column subsampling

XGBoost achieved the highest accuracy of the project so far, approximately 65.4%.

12/06/2026
Investigated whether recovery time affected match outcomes by introducing a rest-days feature. The feature measured the number of days since each player's previous match.

Contrary to expectations, adding rest days reduced model accuracy. This suggests that recovery time alone does not adequately capture fatigue or match sharpness.


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


### Logistic Regression with Recent Form and Surface-Specific Elo

To further improve the model, a player form feature and a surface-specific Elo system were introduced.

#### Recent Form

For each player, recent form was calculated using the outcomes of their previous ten matches. Form is represented as the proportion of wins in those matches. If a player had no previous matches in the dataset, a neutral value of 0.5 was assigned.

#### Surface-Specific Elo

An Elo rating system was implemented to estimate the relative strength of players. Unlike ATP ranking points, Elo ratings are updated after every match and therefore react more quickly to changes in performance.

Since court surface has a significant influence on tennis matches, separate Elo ratings were maintained for each surface:

* **hElo**: Hard court Elo
* **gElo**: Grass court Elo
* **cElo**: Clay court Elo

Before each match, the players' Elo ratings for the corresponding surface were used to compute the feature:

* **surface_elo_diff** = Player 1 surface Elo − Player 2 surface Elo

The ratings were updated chronologically after every match using the standard Elo formula:

```
Expected score:

E_A = 1 / (1 + 10^((R_B - R_A)/400))

Rating update:

R_A_new = R_A + K × (S_A − E_A)
```

where:

* `R_A` and `R_B` are the players' current ratings;
* `S_A` is the match result (1 for a win and 0 for a loss);
* `K = 32` controls how quickly ratings change;
* `E_A` is the expected probability of player A winning.

#### Results

Using a chronological split, with matches before 2024 used for training and matches from 2024 onwards used for testing, the following results were obtained:

| Model                                                                      |   Accuracy |
| -------------------------------------------------------------------------- | ---------: |
| Logistic Regression + rank difference + age difference + surface + best of |     64.12% |
| + Head-to-head features                                                    |     64.45% |
| + Ranking points difference                                                |     64.58% |
| + Recent form                                                              |     64.58% |
| + Surface-specific Elo                                                     | **65.30%** |

The introduction of surface-specific Elo produced the largest improvement among the additional features tested. This suggests that player strength varies considerably across different surfaces and that a dynamic rating system captures this information more effectively than ATP rankings alone.

### XGBoost

After experimenting with Logistic Regression and Random Forest, an XGBoost classifier was introduced. XGBoost is a gradient boosting algorithm that builds an ensemble of decision trees sequentially, with each new tree attempting to correct the errors made by the previous trees. Unlike Logistic Regression, XGBoost is capable of modelling nonlinear relationships and interactions between features.

The model was trained using the same chronological split as previous experiments, with matches before 2024 used for training and matches from 2024 onwards used for testing.

#### Features Used

- `rank_diff`
- `age_diff`
- `surface`
- `best_of`
- `h2h_diff`
- `h2h_matches`
- `rank_points_diff`
- `form_diff`
- `surface_elo_diff`
- `general_elo_diff`

#### Hyperparameters

```python
n_estimators = 300
max_depth = 4
learning_rate = 0.05
subsample = 0.8
colsample_bytree = 0.8
```

#### Results

| Model | Accuracy |
|---------|---------:|
| Logistic Regression + Surface Elo | 65.30% |
| Random Forest | 62.49% |
| XGBoost + Surface Elo | 65.36% |
| XGBoost + Surface Elo + General Elo | **65.42%** |
| XGBoost + Surface Elo + General Elo + Rest Days | 65.11% |

#### General Elo

In addition to surface-specific Elo ratings, a general Elo rating was introduced. Unlike surface Elo, which measures performance on a specific court type, general Elo tracks a player's overall strength regardless of surface.

For every match, the feature

```
general_elo_diff = player_1_general_elo - player_2_general_elo
```

was calculated using only information available before the current match, ensuring that no future information leaked into the model.

Adding this feature produced a small but consistent improvement, increasing accuracy from approximately 65.36% to 65.42%.

#### Rest Days

Another feature investigated was the number of days since each player's previous match. The intuition behind this idea was that fatigue and recovery time may influence performance.

A rest difference feature was defined as:

```
rest_diff = player_1_rest_days - player_2_rest_days
```

However, adding this feature reduced accuracy to approximately 65.11%.

One possible explanation is that rest days alone do not capture whether a player benefits from additional recovery or instead loses match rhythm. Furthermore, tournament scheduling means that both players often have similar rest periods, limiting the amount of information provided by the feature.

#### Features importance


#### Interpretation

Although the improvements obtained from XGBoost were relatively small, the model consistently outperformed both Logistic Regression and Random Forest. Surface-specific Elo remained one of the most influential features, while the addition of a general Elo rating provided a further modest increase in predictive performance.

The results suggest that dynamic rating systems capture player strength better than static ATP rankings alone, and that combining several sources of information can gradually improve prediction accuracy.


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

