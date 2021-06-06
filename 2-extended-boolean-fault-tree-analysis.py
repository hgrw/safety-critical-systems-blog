#!/usr/bin/python
import argparse
import networkx as nx
import json
import cutsets
from lib.probability_tools import node_probability


def main():
    parser = argparse.ArgumentParser(description="Generate canonical form, mocus, fit scores")
    parser.add_argument("-H", "--Help",
                        help="2-extended-boolean-fault-tree-analysis.py -i <inputfile> [--no-mocus] [--top-only]",
                        required=False,
                        default="")
    parser.add_argument("-i", "--input", help="graphml file for analysis", required=True, default="")
    parser.add_argument("-n", "--no-mocus", help="disable mocus calculation", action='store_true')
    parser.add_argument("-t", "--top-fit-only", help="only calculate system fit score", action='store_true')
    argument = parser.parse_args()

    # Extract tree from graphml file
    tree = nx.read_graphml(argument.input)

    # Extract nodes from tree, of form {'node key': {node name, FIT%, operator, [children]}, ...}
    nodes = {key: {'name': value['name'],  # Node name
                   'FIT%': value['FIT%'],  # FIT% score
                   'operator': value['operator'],  # Operator
                   'children': [edge[0] for edge in tree.edges() if edge[1] == key]}  # Children
             for key, value in zip(
            [node[0] for node in tree.nodes(data=True)],  # Node keys from graphml xml tag
            [json.loads(node[1]['label']) for node in tree.nodes(data=True)])}  # Node data from graphml labels

    # Construct fault tree of form [(node id, node operator, [node parents]), ...]
    fault_tree = [
        (nodes[node]['name'], nodes[node]['operator'],
         [nodes[edge[0]]['name'] for edge in tree.edges() if edge[1] == node])
        for node in nodes if nodes[node]['operator'] != 'None']

    if not argument.no_mocus:
        # Calculate the smallest sets of nodes that, by failing, will bring the system down.
        print("Minimum Cut Sets:", *cutsets.mocus(fault_tree), sep='\n')

    # Calculate FIT% for non-leaf-nodes
    while any([nodes[node]['FIT%'] == 'None' for node in nodes]):
        for node in nodes:
            if nodes[node]['FIT%'] == 'None' and all(
                    [nodes[child]['FIT%'] != 'None' for child in nodes[node]['children']]):
                nodes[node]['FIT%'] = node_probability(nodes[node]['operator'],
                                                       [nodes[child]['FIT%'] for child in nodes[node]['children']])
    if argument.top_fit_only:
        for node in nodes:
            if nodes[node]['name'] == "TOP":
                print("System FIT%: ", nodes[node]['FIT%'])
    else:
        print("\nNode FIT% scores:", *[nodes[node]['name'] + ' - ' + nodes[node]['FIT%'] for node in nodes], sep='\n')


if __name__ == "__main__":
    main()
