import random as rd

import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network

from community import Community
from config import vote_for_elites, vote_for_mass

elite_color = "#FFC107"
mass_color = "#9C27B0"


def set_node_attributes(com: Community, color_type: str = "type"):
    def translate_to_color(symbol):
        if symbol == vote_for_elites or symbol == "elite":
            return elite_color
        else:
            return mass_color

    for node in com.nodes:
        com.network.nodes[node]["label"] = str(node)
        com.network.nodes[node]["size"] = com.network.in_degree(node) + 1
        com.network.nodes[node]["level"] = com.network.in_degree(node)
        if color_type == "type":
            com.network.nodes[node]["color"] = translate_to_color(
                com.network.nodes[node]["type"]
            )
        elif color_type == "opinion":
            com.network.nodes[node]["color"] = translate_to_color(
                com.network.nodes[node]["opinion"]
            )
        elif color_type == "vote":
            com.network.nodes[node]["color"] = translate_to_color(
                com.network.nodes[node]["vote"]
            )


def visualize(com: Community, color_type="type"):
    set_node_attributes(com=com, color_type=color_type)
    nt = Network(
        height="500px",
        width="100%",
        directed=True,
        notebook=True,
        neighborhood_highlight=True,
        cdn_resources="remote",
    )
    nt.set_edge_smooth("curvedCCW")
    for node in com.nodes_elite:
        nt.add_node(node, x=-1000, **com.network.nodes[node])
    for node in com.nodes_mass:
        nt.add_node(node, x=1000, **com.network.nodes[node])

    hide_edges = False
    if color_type == "vote":
        hide_edges = True
    elif color_type == "type":
        nt.inherit_edge_colors(False)

    for edge in com.network.edges():
        nt.add_edge(
            edge[0],
            edge[1],
            hidden=hide_edges,
            color=com.network.nodes[edge[1]]["color"],
        )
    nt.hrepulsion(node_distance=200, damping=0.4)
    nt.prep_notebook()
    return nt
