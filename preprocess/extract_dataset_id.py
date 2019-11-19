datasets = []
tasks = []

for split in ['train', 'dev', 'test']:
    with open('../data/datasets_papers/' + split + '_id.txt', 'rt') as input_file:
        for line in input_file.readlines():
            line_list = line.strip().split('\t')
            task = line_list[0]
            dataset = line_list[1]
            if dataset not in datasets:
                datasets.append(dataset)
            if task not in tasks:
                tasks.append(task)

with open('../data/dataset_ids.txt', 'wt') as output_file1:
    for i, dataset in enumerate(datasets):
        output_file1.write('{0:04d}\t{1}\n'.format(i + 1, dataset))

with open('../data/task_ids.txt', 'wt') as output_file2:
    for i, task in enumerate(tasks):
        output_file2.write('{0:04d}\t{1}\n'.format(i + 1, task))