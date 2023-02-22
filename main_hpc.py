from simulation import Simulation

if __name__ == "__main__":
    # Variables for the size of the simulation
    number_of_communities = 10 ** 5
    number_of_voting_simulations = 10 ** 5
    number_of_nodes = 10 ** 2
    filename_csv = "/home/hduijf/data/volume_2/clean"
    folder_communities = "/home/hduijf/data/volume_2/communities"

    Simulation(
        filename_csv=filename_csv,
        folder_communities=folder_communities,
        number_of_communities=number_of_communities,
        number_of_voting_simulations=number_of_voting_simulations,
        number_of_nodes=number_of_nodes,
        elite_competence_range=(0.55, 0.7),
        mass_competence_range=(0.55, 0.7),
        number_of_elites_range=(25, 45),
        probability_homophilic_attachment_range=(0.5, 0.75),
    ).run()
