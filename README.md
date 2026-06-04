# TennisPredictor
This project aims to build a tennis match prediction system using historical ATP match data. The main goal is to explore how player performance, tournament conditions, rankings, and match history can be used to estimate the likely winner of a match. My inspiration for this project came from the youtube channel Green Code.
## Project LogBook   
04/06/2026 For my first approach this project I decided to initially just use a limited database to then increment progressively the complexity and techicality of the system. I started by defining the repository structure, import the csvs containing the data and starting the preprocessing
05/06/2026 developed basic idea of evaluation model, i decided to keep it simple initially taking only account of difference in ranking, difference in age, surface of the court and the number of set needed in order to win (3,5).   



## Ideas, thought process
### ELO system
Since surface its so impacting in tennis matches i decided that each player should be assigned 3 different elos relative to each type of surfaces:   
hELO: for hard courts  
gELO: for grass courts  
cELO: for clay courts  
