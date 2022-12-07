# Majority Voting
This project concerns some agent-based models and simulations of majority voting. The 
main goal is to investigate under which conditions majority voting succeeds in 
selecting the alternative that is in the best interest of the majority. 

## Setup
To run the simulations and generate the data, run the script

```commandline
python main.py
```

which will create a csv file `data/clean.csv`.

To run the statistical analysis, run the notebook XXX. 

## Organization

### The agent-based model: `Community`
The central class `Community` is defined in `community.py`. A `Community` is an 
*agent-based model* consisting of a network of agents, and it can be used to compute 
the estimated accuracy of a given 
community. The networks are generated with homophilic and preferential attachment. 

### The simulation: `Simulation.run()`
The central class method `Simulation.run()` is defined in `simulation.py` and 
produces the csv file `data/clean.csv`. A simulation consists in generating 
`number_of_communities` communities and estimating the accuracy of each community by 
running `number_of_voting_simulations` voting simulations.  

### Statistical analysis: Notebooks
todo

## How to cite
todo
