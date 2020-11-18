# Predicting Winners of PDGA Elite Events Using Machine Learning

This is a personal project that attempts to answer a question noone has asked: Can we use machine learning algorithms to predict the winners of elite professional disc golf tournaments?  

The answer to that queston is kind of.  Using three factors (player, tournament, and the player's most recent PDGA rating prior to the tournament), when estimating which players will finish in the top 5 of any given tournament, we can achieve an overall accuracy of 85% and a precision of 70% within the top 5.  This probably isn't good enough to bet money on, but it is a start. 

The current model focuses on the top 100 male pros in 2019 based on pdga rating.  I consider all [elite series](https://www.pdga.com/tour/search?date_filter[min][date]=2010-01-01&date_filter[max][date]=2020-12-31&EventType[]=E) events from 2010-2020.  The model relies on data from PDGA.com. 

Here are some additional factors I would like to include in the model:

* Weather: Rain/Temperature/Windiness
* Scored practice rounds played leading up to the tournament
* Disaggregate based on the course played on (Instaed of just the tournament)
* Which tournaments have a good enough parking lot for McBeth's [McLaren](https://discgolf.ultiworld.com/livewire/paul-mcbeth-bought-a-mclaren/)


## Code Files

The code below must be run in the order specified below.  Note that the scrape_all_players.py file has a terrible run time.  I am working on making an updated version that only pulls data for the players we are interested in.

1. Scrape Data
    - scrape_all_players.py
    - scrape_elite_events.py
    - scrape_ratings_history.py
2. Build Data
    - build_input_data.py
3. Run ML Models
    - elite_pros_machine.py
    
## ML Model Overview

The dependent variable in my analysis is categorical with two possibilities: finish in the top 5 at a tournament or not in the top 5.  

My factors are the most recent PDGA rating for each player prior to each tournament, dummies for the players, and dummies for the tournament.  I standardize the tournament factor so that the same tournament played multiple times over the years would have the same dummy flag equal to one.  As an example, the Beaver State Fling has been played as an elite series event several times over the years.  Each time it is played, the "beaver_state" dummy will be 1.  This allows the model to control for differences between courses.  Maybe a player can't compete on the wide open bombs needed to win in Emporia, but could shred a woods course in North Carolina.  We want to be able to see these differences.


I consider six possible classification algorithms:

1. Logistic Regression
2. Linear Discriminant Analysis
3. K Neighbors Classification
4. Decision Tree Classification
5. Gaussian Naive Bayes
6. C-Support Vector Classification

While a number of the models performed well, based on the accuracy scores I selected Logistic Regression as the most succesful model.



    

## Contact

If you have any questions or suggestions, I can be reached on [LinkedIn](www.linkedin.com/in/samtauke) or at samtauke@gmail.com
