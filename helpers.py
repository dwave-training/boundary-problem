# Copyright 2024 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import networkx as nx
import matplotlib

matplotlib.use("agg")
from matplotlib import pyplot as plt


def build_graph(img):
    """Builds a weighted graph from a grid of black/white squares and creates an image of the graph.

    Args:
        img(2D list): grid of black/white squares
    """

    G = nx.Graph()

    x_dim = len(img)
    y_dim = len(img[0])

    for i in range(x_dim):
        for j in range(y_dim):
            G.add_node((i, j), pos=(i, j), color=img[i][j])

            if j < y_dim - 1:
                G.add_edge(
                    (i, j), (i, j + 1), weight=abs(img[i][j] - img[i][j + 1])
                )
            if i < x_dim - 1:
                G.add_edge(
                    (i, j), (i + 1, j), weight=abs(img[i][j] - img[i + 1][j])
                )

    pos = nx.get_node_attributes(G, "pos")
    nx.draw(G, pos, node_color="black")
    color_map = ["white" if img[i][j] == 0 else "black" for (i, j) in G]
    nx.draw_networkx_nodes(G, pos, node_size=200, node_color=color_map)
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    filename = "image_graph.png"
    plt.savefig(filename, bbox_inches="tight")
    print("\nYour initial graph is saved to {}\n".format(filename))

    return G


def draw_solution(lut, G):
    """Draws the graph version of the solution.

    Args:
        lut(dict): sample returned from the QPU
        G(NetworkX graph): graph version of the problem
    """

    # Interpret best result in terms of nodes and edges
    cut_edges = [(u, v) for u, v in G.edges if lut[u] != lut[v]]
    uncut_edges = [(u, v) for u, v in G.edges if lut[u] == lut[v]]

    # Display best result
    plt.clf()
    pos = nx.get_node_attributes(G, "pos")
    color_map = [
        "white" if G.nodes[a]["color"] == 0 else "black" for a in G.nodes
    ]
    nx.draw_networkx_nodes(G, pos, node_color=color_map, edgecolors="black")
    nx.draw_networkx_edges(
        G, pos, edgelist=uncut_edges, style="dashdot", alpha=0.1, width=3
    )
    nx.draw_networkx_edges(
        G, pos, edgelist=cut_edges, style="solid", width=3, edge_color="red"
    )
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    filename = "boundary_graph.png"
    plt.savefig(filename, bbox_inches="tight")
    print("Your graph is saved to {}\n".format(filename))


def draw_boundary(lut, G, img):
    """Draws the solution on the grid of black/white squares.

    Args:
        lut(dict): sample from the QPU
        G(NetworkX Graph): problem graph
        img(2D list): initial problem set up
    """

    # Interpret best result in terms of nodes and edges
    cut_edges = [(u, v) for u, v in G.edges if lut[u] != lut[v]]

    plt.clf()

    rects = []
    for i in range(len(img)):
        for j in range(len(img[0])):
            left, bottom, width, height = (i, j, 1, 1)

            if img[i][j] == 0:
                c = "white"
            else:
                c = "black"

            r = plt.Rectangle(
                (left, bottom), width, height, facecolor=c, alpha=0.9
            )
            rects.append(r)

    fig, ax = plt.subplots()
    for r in rects:
        ax.add_patch(r)

    ax.set_xlim(0, len(img))
    ax.set_ylim(0, len(img[0]))
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    lw = 2.5

    for a, b in cut_edges:
        if a[0] + 1 == b[0]:  # horizontal cut edge
            plt.plot([a[0] + 1, b[0]], [b[1], b[1] + 1], "r-", linewidth=lw)
        elif b[0] + 1 == a[0]:
            plt.plot([b[0] + 1, a[0]], [a[1], a[1] + 1], "r-", linewidth=lw)
        elif a[1] + 1 == b[1]:  # vertical cut edge
            plt.plot([b[0], b[0] + 1], [b[1], b[1]], "r-", linewidth=lw)
        elif b[1] + 1 == a[1]:
            plt.plot([a[0], a[0] + 1], [a[1], a[1]], "r-", linewidth=lw)

    filename = "boundary_line.png"
    plt.savefig(filename, bbox_inches="tight")
    print("Your grid is saved to {}\n".format(filename))
