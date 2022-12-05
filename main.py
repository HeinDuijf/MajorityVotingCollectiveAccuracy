from generate_data import generate_communities, process_communities_to_csv

if __name__ == "__main__":
    number_of_communities = 10 ** 2
    generate_communities(
        folder="data/communities",
        number_of_communities=number_of_communities,
        elite_competence_range=(0.55, 0.7),
        mass_competence_range=(0.55, 0.7),
        number_of_elites_range=(25, 45),
        probability_homophilic_attachment_range=(0.5, 0.75),
    )

    process_communities_to_csv(
        folder="data/communities",
        results_file="data/clean.csv",
        number_of_communities=number_of_communities,
        number_of_voting_simulations=10 ** 5,
    )
