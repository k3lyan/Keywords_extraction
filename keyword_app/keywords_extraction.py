import os
import networkx as nx
from networkx import k_core, core_number, drawing, common_neighbors
from collections import OrderedDict, defaultdict
import itertools
#import matplotlib.pyplot as plt
from datetime import datetime
from keyword_app.services.optimization import density, elbow_function
from keyword_app.services.preprocess import preprocess
from keyword_app.utils.logging_config import setup_custom_logger

logger = setup_custom_logger('root')

def unweighted_edges(w):
    cleant_sentences = preprocess()
    adjacency_count = {}
    for s, sents in enumerate(cleant_sentences):
        len_sentence = len(sents)
        window_range = min(w, len_sentence)
        window_terms = sents[0:window_range]
        indexes = list(itertools.combinations(range(window_range), r=2))
        for edge_index in indexes:
            text_edge = tuple([window_terms[i] for i in edge_index])
            if text_edge in adjacency_count:
                adjacency_count[text_edge] += 1
            else:
                adjacency_count[text_edge] = 1
        if(w<=len_sentence):
            for i in range(w, len_sentence):
                term_dissmissed = sents[i]
                window = sents[(i-w+1):(i+1)]
                for p in range(w-1):
                    candidate_edge = (window[p], term_dissmissed)
                    if candidate_edge in adjacency_count:
                        adjacency_count[candidate_edge] += 1
                    else:
                        adjacency_count[candidate_edge] = 1
    return(adjacency_count)

def unweighted_graph(adjacency_nodes):
    G = nx.Graph()
    G.add_edges_from(adjacency_nodes)
    return(G)

def sorted_dict(initial_dict):
    return OrderedDict(sorted(initial_dict.items(), key=lambda x: x[1]))

def compute_sup_e(H):
    common_neighbors_count = {}
    for e in H.edges:
        common_neighbors_count[e] = len(list(common_neighbors(H, e[0], e[1])))
    return sorted_dict(common_neighbors_count)

def k_truss(G, output_for_density=True):
    #G.remove_edges_from(G.selfloop_edges())
    edges_sorted = compute_sup_e(G)
    k_truss_nodes = {}
    k_truss_nodes = defaultdict(lambda: 0, k_truss_nodes)
    not_all_edges_removed = True
    k = 2
    liste_remove=[]
    output_density = [[k, len(G.nodes()), len(G.edges)]]
    while (not_all_edges_removed):
        liste_remove_k = []
        while(list(edges_sorted.values())[0] <= k-2):
            edge = list(edges_sorted.keys())[0]
            u = edge[0]
            v = edge[1]
            nb_u = list(G.neighbors(u))
            nb_v = list(G.neighbors(v))
            u, v = v, u
            # Among both nodes, we keep the minimum number of neighbors
            # the common neighbors between the 2 nodes will necessarily be in that list
            if (len(nb_u) < len(nb_v)) :
                nbU = nb_u
                u, v = v, u
            else:
                nbU = nb_v
            for w in nbU:
                if(G.has_edge(w,v)):
                    sup_keys = edges_sorted.keys()
                    # Pruning
                    if((v,w) in sup_keys):
                        edges_sorted[(v,w)] -= 1
                    else:
                        edges_sorted[(w,v)] -= 1
                    if((u,w) in sup_keys):
                        edges_sorted[(u,w)] -= 1
                    else:
                        edges_sorted[(w,u)] -= 1
                    edges_sorted = sorted_dict(edges_sorted)
            del(edges_sorted[edge])
            liste_remove_k.append(edge)
            G.remove_edge(edge[0],edge[1])
            if(len(G.edges)==0):
                break
        liste_remove.append(liste_remove_k)
        if(len(list(edges_sorted.keys())) == 0):
            not_all_edges_removed = False
        else:
            k += 1
            sub_G = max(nx.connected_component_subgraphs(G), key=len)
            for node_not_removed in sub_G.nodes:
                k_truss_nodes[node_not_removed] += 1
            if(output_for_density):
                output_density.append([k, len(list(sub_G.nodes)), len(sub_G.edges)])
    #nx.draw(sub_G, with_labels=True, font_color='k', node_color='g', edge_color='y', font_size=max(min(20,500/len(sub_G.nodes)),9), width=1, node_size=0, label='k-subgraph')
    #plt.show()
    #plt.savefig('{}-truss_subgraph.png'.format(k))
    return (k_truss_nodes, k, sub_G, output_density)

def sorted_keywords(k_truss_nodes):
    return sorted(k_truss_nodes, key=k_truss_nodes.get, reverse=True)

def get_optimized_nb_keywords(output_density, density_applied):
    if(density_applied):
        D_n = density(output_density)
        logger.debug(f'elbow_function(D_n): {elbow_function(D_n)}')
        return(output_density[elbow_function(D_n)][1])
    else:
        CD = []
        n = 1
        for i in range(len(output_density)-1):
            CD.append(output_density[i+1][1]-output_density[i][1])
        for i in range(2,len(CD)-1):
            if(CD[i+1]<0 and CD[i]>0):
                n = i
        return(output_density[n][1])

def main():
    t0 = datetime.now()
    unweighted_edges_list = list(unweighted_edges(10).keys())
    G_unweighted = unweighted_graph(unweighted_edges_list)
    k_truss_nodes, k, sub_G, output_density = k_truss(G_unweighted, output_for_density=True)

    optimization_method = False
    if optimization_method:
        nb_keywords = get_optimized_nb_keywords(output_density, True)
    else:
        nb_keywords = int(os.getenv('NB_KW', 10))

    t1 = datetime.now() - t0
    logger.debug(f'K-Truss step: {t1}')
    logger.debug(f'K-max: {k}')
    logger.debug(f'-----------List of keywords ({nb_keywords})-----------')
    for i in range(nb_keywords):
        logger.debug(sorted_keywords(k_truss_nodes)[i])

if __name__ == '__main__':
    main()
