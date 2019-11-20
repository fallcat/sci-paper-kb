import networkx as nx
import pprint
import numpy as np

split = [0.6, 0.2, 0.2]
total_lines = 5123
split_lines = [total_lines*x for x in split]
split_list = [[], [], []]
split_names = ['train', 'dev', 'test']

with open('../data/all_data.txt', 'rt') as file:
    G = nx.Graph()
    for line in file.readlines():
        line_list = line.strip().split('\t')
        G.add_edge('D'+line_list[3], 'P'+line_list[6])
    print([len(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)])

    connected_components_list = list(sorted(nx.connected_components(G), key=len, reverse=True))

with open('../data/all_data.txt', 'rt') as file:
    subgraphs_indices = []
    connected_components_dict = {}
    connected_components_dict2 = {}

    lines = []

    for line_idx, line in enumerate(file.readlines()):
        line_list = line.strip().split('\t')
        lines.append(line)
        for i, c in enumerate(connected_components_list):
            # print("D" + line_list[3])
            if "D" + line_list[3] in c:
                subgraphs_indices.append(i)
                if i not in connected_components_dict:
                    connected_components_dict[i] = 1
                    connected_components_dict2[i] = [line_idx]
                else:
                    connected_components_dict[i] += 1
                    connected_components_dict2[i].append(line_idx)

    connected_components_dict_list = [connected_components_dict[i] for i in sorted(connected_components_dict)]
    connected_components_dict2_list = [connected_components_dict2[i] for i in sorted(connected_components_dict2)]
    # print("connected_components_dict_list", connected_components_dict_list)
    # print("connected_components_dict2_list", connected_components_dict2_list)

    for i, c in enumerate(connected_components_dict2_list):
        split_to_put = np.argmax([x - len(y) for x, y in zip(split_lines, split_list)])
        # print("split_to_put", split_to_put)
        # print("split_list[int(split_to_put)]", split_list[int(split_to_put)])
        # print(c)
        split_list[int(split_to_put)] = split_list[int(split_to_put)] + c

    print([len(x) for x in split_list])
    # pp = pprint.PrettyPrinter()
    # pp.pprint(connected_components_dict)

    for i, c in enumerate(split_list):
        with open('../data/datasets_papers622/' + split_names[i] + '622_id_new.txt', 'wt') as output_file:
            for line in np.array(lines)[np.array(c)]:
                output_file.write(line)