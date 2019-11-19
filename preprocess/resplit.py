import networkx as nx

with open('../data/datasets_papers_all_id.txt', 'rt') as file:
    G = nx.Graph()
    for line in file.readlines():
        line_list = line.strip().split('\t')
        G.add_edge('D'+line_list[3], 'P'+line_list[6])
    print([len(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)])
    for c in nx.connected_components(G):
        print(c)