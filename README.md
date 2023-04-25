# Majority Voting

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7767125.svg)](https://doi.org/10.5281/zenodo.7767125)

Majority voting plays a central role in democratic institutions. I investigate the collective accuracy of majority voting: which refers to the probability that it succeeds in selecting the alternative that is in the best interest of the majority. It would be surprising if majority voting in a community would not succeed in selecting policies that are in the best interest of the majority. However, people may not be perfectly competent in forming their voting decisions, i.e., people may wrongly think that a given political candidate is in their own best interest. In addition, people are often influenced by others before reaching their voting decision. It might be that highly competent and highly influential minorities can skew the outcomes of majority voting in their favour. 

I use an agent-based model to explore the impact of imperfect competence and social influence on majority voting. The agents are placed on influence networks that are generated in a natural way, without the assumption that powerful minorities manipulate the network structure. Surprisingly, in these circumstances, there is a considerable risk that majority voting fails to track the majority’s interests. I consider several possible predictors of collective accuracy. My analysis suggests that the competences of the minority and the majority and the proportional influence of the minority are strong predictors, while, surprisingly, the relative size of the minority is not. The morale is that comparatively competent and disproportionately influential minority groups can skew the outcomes of majority voting, regardless of the size of the minority group.

This repository contains the code for the agent-based model and simulations, for producing some figures, and for the statistical analysis. To get a feel for the agent-based model, click the picture below:

[![A picture of an example of an agent-based model](/notebook/agent-based-model.png  "An example of an agent-based model")](https://heinduijf.github.io/MajorityVoting/)

## 1. Setup
To run the project, you first need to install the required packages
```commandline
pip install -r requirements.txt
```

## 2. Simulation
1. To get a feel for the agent-based model, you can check out the
   [jupyter notebook](NotebookWalkthrough.ipynb), which includes some network visualizations, by either 
   opening the [pages](https://heinduijf.github.io/MajorityVoting/) or by running
```commandline
jupyter-notebook NotebookWalkthrough.ipynb
```
Running the notebook will create several html files in the folder `www` with 
visualizations of agent-based models.

2. To run the simulations and generate the data, run the script
```commandline
python main.py
```
which will create a csv file `data/clean.csv`, a collection of communities in the 
folder `data/communities`, and a README file with the parameter settings for the 
simulation in `data/README.csv`.

3. To generate the figures, run the script
```commandline
python figures.py
```
which will create a folder `new_figures` containing all the figures. 

4. To run the statistical analysis, run the script
```commandline
python statistics.py
```
which will create several csv files in the folder `stats` with the results of the 
statistical analysis.  

## 3. Organization of the project

### The agent-based model: `community.py`
The central class `Community` is defined in `community.py`. A `Community` is an 
*agent-based model* consisting of a network of agents, and it can be used to compute 
the estimated accuracy of a given community. The networks are generated with homophilic 
and preferential attachment. 

### Jupyter notebook: `NotebookWalkthrough.ipynb`
The jupyter notebook walks you through the stages of the agent-based model 
`Community` using some network visualizations. To minimalize the amount of code in the 
notebook, some scripts are stored in `notebook.py`, which is ran in one of the initial notebook cells. 

### Simulations: `simulation.py`
The central class `Simulation` and method `Simulation.run()` is defined in 
`simulation.py`, the method produces the csv file `data/clean.csv`. The method 
`Simulation.run()` runs a simulation consisting of generating `number_of_communities` 
communities and estimating the accuracy of each community by running 
`number_of_voting_simulations` voting simulations.  

### Figures: `figures.py`
The script `figures.py` creates a folder `new_figures` containing all the 
figures. The folder `generate_figures` contains the scripts that generate 
figures. Each script in that folder is associated with one of the figures. 

### Statistical analysis: `statistics.py`
The script `statistics.py` runs the statistical analysis that generates several csv 
files in  the folder `stats`. The folder `stats` contains scripts that generate the 
csv files. Each script in that folder is associated with one of the csv files.  

## 4. Runtime limitations
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

## 5. Licence and citation
This repository accompanies an academic paper (under review). In the meantime, please cite as follows:

[How to cite](CITATION.cff):
- Duijf, H. (2023). MajorityVoting (Version 1.0.0) [Computer software]. https://doi.org/10.5281/zenodo.7767125

Released under the [MIT licence](LICENCE.md).
