import os
import re
from tika import parser


def extract_information(pdf_path):
    raw_text = parser.from_file(pdf_path)
    raw_list = raw_text['content'].splitlines()
    text = " ".join(raw_list)
    return text

if __name__ == '__main__':
    PAPERS_PATH = "/Users/weiqiuyou/Documents/UMass/2019Fall/COMPSCI692A/project/sci-paper-kb/papers"
    DEV_PATH = "/Users/weiqiuyou/Documents/UMass/2019Fall/COMPSCI692A/project/data/datasets_papers/dev_id.txt"
    in_candidates = 0
    all_count = 0
    found_count = 0
    with open(DEV_PATH, 'rt') as test_file:
        for line in test_file.readlines():
            line_list = line.strip().split('\t')
            dataset = line_list[1]
            paper_id = line_list[4]
            try:
                text = extract_information(os.path.join(PAPERS_PATH, paper_id + '.pdf'))

                # Find all capitalized words in front of the word "dataset" or "datasets"
                candidates1 = re.findall(r'\b\(?[A-Z]+[A-Za-z0-9-]*\)?', text)
                # candidates2 = re.findall(r'\bdataset[s]?[,.]? \b\(?[A-Z]+[A-Za-z0-9-]*\)?', text)
                candidates_set = set([candidate.split()[0].replace('(', '').replace(')', '') for candidate in candidates1])
                # candidates_set.update(set([candidate.split()[1].replace('(', '').replace(')', '') for candidate in candidates2]))

                # Find all the capitalized words connected with existing candidates using "and"
                # new_candidates_list = []
                # for candidate in candidates_set:
                #     new_candidate1 = [x.split()[-1].replace('(', '').replace(')', '').replace(',', '') for x in re.findall((r'%s \band \b\(?[A-Z]+[A-Za-z0-9-]*\)?' % candidate), text)]
                #     new_candidate2 = [x.split()[0].replace('(', '').replace(')', '').replace(',', '') for x in re.findall((r'\b\(?[A-Z]+[A-Za-z0-9-]*\)? \band %s' % candidate), text)]
                #     new_candidate3 = [y.replace(',', '') for x in re.findall((r'[\b\(?[A-Z]+[A-Za-z0-9-]*, ]?\b%s[, \b[A-Z]+[A-Za-z0-9-]*\)?]?' % candidate), text) for y in x.split()]
                #
                #     # if len(new_candidate3) > 0:
                #     #     print("new_candidate3", new_candidate3)
                #     #     print("new_candidate3", paper_id)
                #     new_candidates_list.extend(new_candidate1 + new_candidate2 + new_candidate3)
                # candidates_set.update(set(new_candidates_list))


                # if dataset in candidates_set:
                for candidate in candidates_set:
                    all_count += 1
                    if candidate in dataset or dataset in candidate:
                        in_candidates += 1
                else:
                    print(paper_id)
                    print("candidates_set", candidates_set)
                    print("dataset", dataset)
                if len(candidates_set) > 0:
                    found_count += 1
            except:
                continue
    print("Recall:", float(in_candidates)/all_count)
    print("Recall2:", float(in_candidates) / found_count)