import numpy as np
import pandas as pd
import networkx as nx
from scipy.special import comb

def Sample(edge_prob):
    p = np.random.uniform()
    if p <= edge_prob:
        return True
    else:
        return False
    
def Get_Edge_Probability(G, p, min_matepair):
    edges = list(G.edges())
    edge_prob = {}
    if p > 1: p = 1
    q = 1-p

    for e in edges:
        bsize = G.edges[e]['bsize']
        prob = 0
        for i in range(min_matepair, bsize+1):
            prob += comb(bsize, i)*pow(p, i)*pow(q, bsize-i)
        edge_prob[e] = prob
    return edge_prob

def Get_Terminal_Nodes(bubble):
    counts = {}
    for k in bubble:
        try: counts[k] += 1
        except KeyError: counts[k] = 1
    terms = []
    for k in counts:
        if counts[k] == 2:
            terms.append(k)
    assert len(terms) == 2, "Error"
    return terms
        
    
def Return_Bubble_Type(Sampled_Subgraph, Source, Target):
    Simple_Paths = list(nx.all_simple_paths(Sampled_Subgraph, Source, Target, 50))
    num_paths = len(Simple_Paths)
    if num_paths == 0:
        Simple_Paths = list(nx.all_simple_paths(Sampled_Subgraph, Target, Source, 50))
        num_paths = len(Simple_Paths)
    bub_type = 'None'
    min_nodes = np.inf
    
    if num_paths <= 1: 
        return bub_type
    for Path in Simple_Paths:
        number_nodes = len(Path)
        if number_nodes < min_nodes: min_nodes = number_nodes
    if min_nodes == 2 and num_paths >= 2: bub_type = 'indel'
    elif min_nodes > 2 and num_paths == 2: bub_type = 'SimpleSV'
    elif min_nodes > 2 and num_paths > 2: bub_type = 'ComplexSV'
    return bub_type

def Downsample(Graph, bubbles, Edge_Probabilities):
    variant_counter = dict({'indel':0,'SimpleSV':0,'ComplexSV':0,'None':0})
    for b in bubbles:
        b = b.strip().split("\t")
        terms = Get_Terminal_Nodes(b)
        start, end = terms[0], terms[1]
        g_subgraph = Graph.subgraph(b).copy()
        Edges = list(g_subgraph.edges())
        for E in Edges:
            mate_pair = g_subgraph.edges[E]['bsize']
            edge_presence = Sample(Edge_Probabilities[E])
            if not edge_presence: 
                g_subgraph.remove_edge(*E)
        Bubble_Type = Return_Bubble_Type(g_subgraph, start, end)
        variant_counter[Bubble_Type] += 1
    return variant_counter

def ANCHOR(Graph, bubbles, p, min_matepair=3, bootstrap = 1000):
    anchor_list = []
    Edge_Probabilities = Get_Edge_Probability(Graph, p, min_matepair)
    for i in range(bootstrap):
        variant_counter = Downsample(Graph, bubbles, Edge_Probabilities)
        anchor_list.append(variant_counter)
    df_anchor = pd.DataFrame(anchor_list)
    return df_anchor

def Get_Bubble_Counts(Graph, bubbles):
    variant_counter = dict({'indel':0,'SimpleSV':0,'ComplexSV':0,'None':0})
    for b in bubbles:
        b = b.strip().split("\t")
        terms = Get_Terminal_Nodes(b)
        start, end = terms[0], terms[1]
        g_subgraph = Graph.subgraph(b).copy()
        Bubble_Type = Return_Bubble_Type(g_subgraph, start, end)
        if Bubble_Type == "None":
            print(b)
        variant_counter[Bubble_Type] += 1
    return variant_counter