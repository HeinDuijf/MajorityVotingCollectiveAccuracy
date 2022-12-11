from simulation import Simulation

if __name__ == "__main__":
    number_of_communities = 1
    number_of_voting_simulations = 100000
    number_of_nodes = 10**2

    # Todo: the function Simulation.run() does not return anything,
    # so the variable simulation isn't anything. It's also not used
    # Why do we set some variables above, and some below?
    # Be careful with the name 'file', it is also a python builtin. --> filename is better
    simulation = Simulation(
        file="data/clean.csv",
        number_of_communities=number_of_communities,
        number_of_voting_simulations=number_of_voting_simulations,
        number_of_nodes=number_of_nodes,
        elite_competence_range=(0.55, 0.7),
        mass_competence_range=(0.55, 0.7),
        number_of_elites_range=(25, 45),
        probability_homophilic_attachment_range=(0.5, 0.75),
    ).run()
