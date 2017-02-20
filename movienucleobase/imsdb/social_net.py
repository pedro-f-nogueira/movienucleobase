"""
.. module:: calc_net_metrics.py
   :synopsis: Builds the social network and calculates relevant metrics

.. moduleauthor:: Pedro Araujo <pedroaraujo@colorlesscube.com>
.. moduleauthor:: Pedro Nogueira <pedro.fig.nogueira@gmail.com>
"""

import networkx as nx
import pandas as pd
import community


try:
    import pygraphviz
    from networkx.drawing.nx_agraph import graphviz_layout
except ImportError:
    try:
        import pydotplus
        from networkx.drawing.nx_pydot import graphviz_layout
    except ImportError:
        raise ImportError("This example needs Graphviz and either "
                          "PyGraphviz or PyDotPlus")


def return_metrics(nodes, edges):
    """"
    This function build a social netwrok using networkx and
    calculates the degree and betweeness centrailty for each node.
    """

    graph = nx.Graph()

    labels = {}
    a = 0

    # Adding the nodes
    for index, row in nodes.iterrows():
        b = row[1]
        graph.add_node(row[1], label=row[2])
        graph.node[b]['state'] = row[2]
        labels[a] = row[1]
        a += 1

    # Adding the edges
    for index, row in edges.iterrows():
        graph.add_edge(row[2], row[4], weight=row[0])

    node_labels = nx.get_node_attributes(graph, 'state')

    dict_degree_centrality = {}
    dict_betweenness_centrality = {}
    dict_communities = {}

    # Getting the labels to the dictionary
    for i, k in nx.degree_centrality(graph).iteritems():
        dict_degree_centrality[node_labels[i]] = k

    for i, k in nx.betweenness_centrality(graph).iteritems():
        dict_betweenness_centrality[node_labels[i]] = k

    parts = community.best_partition(graph)

    for node in graph.nodes():
        dict_communities[node_labels[node]] = parts.get(node)

    # Calculating metrics
    df_degree_centrality = pd.DataFrame(dict_degree_centrality.items(),
                                        columns=['name', 'degree_centrality'])\
        .sort_values(by='degree_centrality', ascending=False)

    df_betweenness_centrality = pd.DataFrame(dict_betweenness_centrality.items(),
                                             columns=['name', 'betweenness_centrality'])\
        .sort_values(by='betweenness_centrality', ascending=False)

    df_communities = pd.DataFrame(dict_communities.items(),
                                  columns=['name', 'community']) \
        .sort_values(by='community', ascending=False)

    # Joining both dataframes using the char name
    df_metrics = pd.merge(df_degree_centrality, df_betweenness_centrality, on='name', how='inner')
    df_metrics = pd.merge(df_metrics, df_communities, on='name', how='inner')
    df_metrics = pd.merge(df_metrics, nodes, on='name', how='inner')

    return df_metrics
