# Majority Voting

This project concerns agent-based models and simulations of majority voting. The 
main goal is to investigate under which conditions majority voting succeeds in 
selecting the alternative that is in the best interest of the majority. 

## 1. Setup
0. To run the project, you first need to install the required packages
```commandline
pip install -r requirements.txt
```
1. To run the simulations and generate the data, run the script
```commandline
python main.py
```
which will create a csv file `data/clean.csv`, a collection of communities in the 
folder `data/communities`, and a README file with the parameter settings for the 
simulation in `data/README.csv`.
2. To generate the figures, run the script
```commandline
python figures.py
```
which will create a folder `new_figures` containing all the figures. 
3. To run the statistical analysis, run the script
```commandline
python statistics.py
```
which will create several csv files in the folder `stats` with the results of the 
statistical analysis.  

## 2. Organization of the project

### The agent-based model: `Community`
The central class `Community` is defined in `community.py`. A `Community` is an 
*agent-based model* consisting of a network of agents, and it can be used to compute 
the estimated accuracy of a given community. The networks are generated with homophilic 
and preferential attachment. 

### Simulations: `Simulation.run()`
The central class `Simulation` and method `Simulation.run()` is defined in 
`simulation.py`, the method produces the csv file `data/clean.csv`. The method 
`Simulation.run()` runs a simulation consisting of generating `number_of_communities` 
communities and estimating the accuracy of each community by running 
`number_of_voting_simulations` voting simulations.  

### Figures
The script `figures.py` creates a folder `new_figures` containing all the 
figures. The folder `generate_figures` contains the scripts that generate 
figures. Each script in that folder is associated with one of the figures. 

### Statistical analysis
The script `statistics.py` runs the statistical analysis that generates several csv 
files in  the folder `stats`. The folder `stats` contains scripts that generate the 
csv files. Each script in that folder is associated with one of the csv files.  

## 3. Runtime issues
1. Runtime can be an issue for `Simulation.run()`. To run the simulation (with 
parameters `number_of_communities = 10 ** 5` and
`number_of_voting_simulations = 10 ** 5`), we used a virtual machine with 16 cores 
and 64 GB RAM, which took approximately 5 days to finish. 

2. Runtime can also be a minor issue for two scripts in the folder 
`generate_figures`, which are also included in the script `figures.py`. We ran these 
scripts on a basic laptop (2 cores 8 GB RAM). 
   1. The script `figure_accuracy_homophily.py`) takes approximately 10 minutes 
   (with parameters `number_of_communities=200` and `number_of_voting_simulations=200`). 
   2. The script `figure_distribution_in_degree.py` takes approximately 20 minutes to 
      finish (for 10**5 communities).

## 4. Licence and citation
See `about` the repository or the files `LICENCE.md` and `CITATION.cff`.
