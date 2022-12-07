from simulation import Simulation

if __name__ == "__main__":
    number_of_communities = 10 ** 3
    number_of_voting_simulations = 10 ** 2
    simulation = Simulation(
        file="data/clean.csv",
        number_of_communities=number_of_communities,
        number_of_voting_simulations=number_of_voting_simulations,
        elite_competence_range=(0.55, 0.7),
        mass_competence_range=(0.55, 0.7),
        number_of_elites_range=(25, 45),
        probability_homophilic_attachment_range=(0.5, 0.75),
    ).run()
