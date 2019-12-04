import os
import re
from tika import parser
import pickle
from tqdm import tqdm

# Data Format: task, task_id, dataset, dataset_id, paper_name, paper_link, paper_id

oneside_window = 5  # whole window will be oneside_window * 2 + 1


def extract_information(pdf_path):
    raw_text = parser.from_file(pdf_path)
    raw_list = raw_text['content'].splitlines()
    text = " ".join(raw_list)
    return text

if __name__ == '__main__':
    PAPERS_PATH = "/Users/weiqiuyou/Documents/UMass/2019Fall/COMPSCI692A/project/sci-paper-kb/papers"
    TRAIN_PATH = "/Users/weiqiuyou/Documents/UMass/2019Fall/COMPSCI692A/project/sci-paper-kb/data/datasets_papers811/test.txt"

    non_exist_papers = []

    with open(TRAIN_PATH, 'rt') as train_file:
        sentence_pairs = []
        failed_dataset = []
        for line in tqdm(train_file.readlines()):
            line_list = line.strip().split('\t')
            dataset = line_list[2]
            paper_id = line_list[6]
            try:
                text = extract_information(os.path.join(PAPERS_PATH, paper_id + '.pdf'))
            except:
                non_exist_papers.append(paper_id)
                continue
            # text_list = text.strip().split(' ')
            dataset_variants = []
            dataset_variants.append(dataset)
            dataset_variants.append(dataset.upper())
            dataset_variants.append(dataset.lower())
            dataset_variants.extend(dataset.split())
            dataset_variants.extend(dataset.split('-'))
            dataset_variants.extend([x.strip() for x in dataset.split('/')])
            dataset_variants.extend([x.strip() for x in re.split('\(|\)', dataset)])
            dataset_variants.append(re.sub("\d+", "", dataset))
            if dataset.isupper():
                dataset_variants.append("".join([c + r"\S+ " for c in dataset])[:-1])
            dataset_variants = list(set(dataset_variants))

            # Find all windows that contain the dataset name
            all_sentences = []
            for dataset_variant in dataset_variants:
                regex1 = r'(\b(\S+ ){0,%d}\(*%s\)*\d*\,*( \S+){0,%d}\b)' % (oneside_window, dataset_variant, oneside_window)
                # regex2 = r'(\b\(*%s\)*( \S+){%d}\b)' % (dataset_variant, oneside_window)
                # print("regex1", regex1)
                # print("regex2", regex2)
                # print("paper_id", paper_id)
                try:
                    sentences = re.findall(regex1, text)
                except:
                    print("regex1", regex1)
                # sentences = re.findall(regex2, text)
                # print(sentences)
                all_sentences.extend([(s[0], dataset_variant, dataset) for s in sentences])

            # print("all", all_sentences)
            if len(all_sentences) == 0:
                print(paper_id, dataset)

                failed_dataset.append((paper_id, dataset))
                with open("/Users/weiqiuyou/Documents/UMass/2019Fall/COMPSCI692A/project/sci-paper-kb/experiments/" + paper_id + ".txt",
                            'wt') as file1:
                        file1.write(text)
            else:
                sentence_pairs.extend(all_sentences)

        data = {"sentences": sentence_pairs, "failed_dataset": failed_dataset}
        with open('/Users/weiqiuyou/Documents/UMass/2019Fall/COMPSCI692A/project/sci-paper-kb/data/datasets_papers811/test.pairs.txt', 'wt') as output_file:
            for pair in sentence_pairs:
                output_file.write("%s\t%s\t%s\n" % (pair[0], pair[1], pair[2]))

        with open('/Users/weiqiuyou/Documents/UMass/2019Fall/COMPSCI692A/project/sci-paper-kb/data/datasets_papers811/test.failed.txt', 'wt') as output_file:
            for failed in failed_dataset:
                output_file.write("%s\t%s\n" % (failed[0], failed[1]))
            # except:
            #     print("fail")
            #     continue
    # print("Recall:", float(in_candidates)/all_count)
    # print("Recall2:", float(in_candidates) / found_count)
    print("Non-exist papers:", non_exist_papers)