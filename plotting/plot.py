from pyvis.network import Network
import networkx as nx
from networkx.generators.ego import ego_graph
import pandas as pd


def draw_network(G, ax, edge_list=None, color="red"):
    # draw from existing nx object
    if edge_list is not None:
        G = nx.Graph()
        G.add_edges_from(edge_list)  # using a list of edge tuples
        # pruned network after Max weighted spanning tree algo
        pos = nx.spring_layout(G)
        nx.draw_networkx(G, pos=pos, node_color=color, ax=ax)
        print(nx.info(G))
        return G
    else:
        nx.draw_networkx(G, node_color=color)
        print(nx.info(G))
        return G


def plot_community_class_count(communities):
    count_list = []
    class_list = []
    for i, c in enumerate(communities):
        class_list.append(i)
        count_list.append(len(list(c)))

    df = pd.DataFrame({"class": class_list, "count": count_list})
    df.plot.bar(x="class", y="count")
    return df


def plot_subgraph(G, node_list, ax):
    subgraph = G.subgraph(node_list)
    diameter = nx.diameter(subgraph)
    print("Network diameter of largest component:", diameter)
    draw_network(subgraph, color="red", ax=ax)
    return subgraph


def plot_ego_network(G, n, radius, ax):
    """
    plot ego network around a node n depending
    on radius setting i.e. only include upto
    n nodes directly or indirectly connected to
    this node
    """
    ego_nx = ego_graph(G, n, radius=radius)
    draw_network(ego_nx, ax=ax, color="red")
    return ego_nx


def plot_interactive_network(model, title):
    net = Network(notebook=True)
    net.from_nx(model)
    net.show_buttons(filter=["physics"])
    filename = f"{title}.html"
    net.show(filename)
    return net
