import re
from tqdm import tqdm

with open('/Users/weiqiuyou/Documents/UMass/2019Fall/COMPSCI692A/project/sci-paper-kb/data/datasets_papers811/test.pairs.txt', 'rt') as input_file:
    with open('/Users/weiqiuyou/Documents/UMass/2019Fall/COMPSCI692A/project/sci-paper-kb/data/datasets_papers811/test.columns.txt', 'wt') as output_file:
        wholes = {}
        exceptions1 = 0
        exceptions2 = 0
        no_exception = 0
        for line in tqdm(input_file.readlines()):
            line_list = line.strip().split('\t')
            sentence = line_list[0]
            try:
                dataset_variant = line_list[1]
                dataset = line_list[2]
            except:
                print(line_list)
                exceptions1 += 1
                continue
            if dataset_variant == "".join([c + r"\S+ " for c in dataset])[:-1]:
                whole = True
            else:
                whole = False
            if dataset in wholes and dataset_variant in wholes[dataset]:
                wholes[dataset][dataset_variant] += 1
            else:
                wholes[dataset] = {dataset_variant: 1}
            try:
                # print("sentence:", sentence)
                # print("dataset", dataset)
                # print("dataset var", dataset_variant)
                result1 = re.search(dataset_variant, sentence)
                result2 = re.search(dataset, sentence)
                if result2 is not None and result2.start() < result1.start() and result2.end() > result1.end():
                    result_final = result2
                else:
                    result_final = result1
                sentence_list = sentence.split()
                idx = 0
                start = -1
                end = -1
                l = []
                for i, w in enumerate(sentence_list):
                    if start == -1:
                        # print("start == -1", result_final.start(), idx, len(w))
                        if result_final.start() >= idx and result_final.start() < idx + len(w) + 1:
                            start = i
                            l.append("B-DAT")
                            if result_final.end() < idx + len(w) + 1:
                                end = i
                        else:
                            l.append("O")
                    elif end == -1:
                        l.append("I-DAT")
                        # print("end == -1", result_final.end(), idx, len(w))
                        if result_final.end() < idx + len(w) + 1:
                            end = i
                        #
                        # elif result_final.end() > idx + len(w) + 1:
                        #     l.append("O")
                        # else:
                        #     l.append("I-DAT")
                    else:
                        # print("else")
                        l.append("O")
                    idx += len(w) + 1
                output_file.write("\n".join([x + " " + y for x, y in zip(sentence_list, l)]) + "\n\n")
                no_exception += 1
                # if no_exception == 4:
                #     break
            except:
                print("unbalanced parenthesis", line_list)
                exceptions2 += 1
                continue
        print("exceptions1", exceptions1)
        print("exceptions2", exceptions2)
        print("no exception:", no_exception)