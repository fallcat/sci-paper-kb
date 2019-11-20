with open('../data/datasets_papers_all_id.txt', 'rt') as input_file:
    with open('../data/datasets_papers_all_id_new.txt', 'wt') as output_file:
        for line in input_file.readlines():
            line_list = line.strip().split('\t')
            if line_list[-1] not in ['0599', '0280']:
                output_file.write(line)