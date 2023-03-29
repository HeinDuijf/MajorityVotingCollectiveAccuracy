import random as rd

import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network

from community import Community
from config import vote_for_elites, vote_for_mass

elite_color = "#FFC107"
mass_color = "#9C27B0"


def set_node_attributes(com: Community, color_type: str = "type"):
    if color_type == "type":
        for node in com.nodes:
            if node in com.nodes_elite:
                com.network.nodes[node]["color"] = elite_color
            else:
                com.network.nodes[node]["color"] = mass_color
    elif color_type == "opinion":
        for node in com.nodes:
            if com.network.nodes[node]["opinion"] == vote_for_elites:
                com.network.nodes[node]["color"] = elite_color
            else:
                com.network.nodes[node]["color"] = mass_color
    elif color_type == "vote":
        for node in com.nodes:
            if com.network.nodes[node]["vote"] == vote_for_elites:
                com.network.nodes[node]["color"] = elite_color
            else:
                com.network.nodes[node]["color"] = mass_color
    for node in com.nodes:
        com.network.nodes[node]["label"] = str(node)
        com.network.nodes[node]["size"] = com.network.in_degree(node) + 1
        com.network.nodes[node]["level"] = com.network.in_degree(node)


def visualize(com: Community, color_type="type"):
    set_node_attributes(com=com, color_type=color_type)
    nx_net = com.network
    nt = Network(
        height="500px",
        width="100%",
        directed=True,
        notebook=True,
        neighborhood_highlight=True,
        cdn_resources="remote",
    )
    nt.set_edge_smooth("curvedCCW")
    nt.from_nx(nx_net)
    nt.hrepulsion(node_distance=200, damping=0.4)
    nt.prep_notebook()
    return nt
