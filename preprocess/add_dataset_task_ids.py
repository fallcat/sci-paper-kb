for split in ['train', 'dev', 'test']:
    with open('../data/datasets_papers.txt', 'rt') as input_file:
        with open('../data/dataset_ids.txt', 'rt') as dataset_file:
            with open('../data/task_ids.txt', 'rt') as task_file:
                with open('../data/datasets_papers_all_id.txt', 'wt') as output_file:
                    datasets_list = [line.strip().split('\t')[1] for line in dataset_file.readlines()]
                    tasks_list = [line.strip().split('\t')[1] for line in task_file.readlines()]
                    for line in input_file.readlines():
                        line_list = line.strip().split('\t')
                        output_file.write('{0}\t{1:04d}\t{2}\t{3:04d}\t{4}\t{5}\t{6}\n'.format(line_list[0],
                                                                                              tasks_list.index(line_list[0]) + 1,
                                                                                              line_list[1],
                                                                                              datasets_list.index(line_list[1]) + 1,
                                                                                              line_list[2],
                                                                                              line_list[3],
                                                                                              line_list[4]))