import subprocess
import sys
import pandas as pd

output_labels = ''

# Parse fastq.files.group.tsv file specifying file groups to mageck's format
if sys.argv[1] and sys.argv[1].endswith('fastq.files.group.tsv'):
    files = pd.read_csv(sys.argv[1], sep='\t')

    groups = {}
    for group in set(files['Group name']):
        groups[group] = []

    for i in range(files.shape[0]):
        group = files.ix[i, 1]
        filepath = files.ix[i, 0]

        groups[group].append(filepath)

    output_labels = '--sample-label '
    output_paths = '--fastq '
    for label, path_list in groups.items():
        counter = 1
        for filepath in path_list:
            output_labels += '{}.{},'.format(label, counter)
            output_paths += '{},'.format(filepath)
        output_paths = output_paths[:-1]
        output_paths += ' '

    output_labels = output_labels[:-1]
    output_paths = output_paths[:-1]
else:
    # Count table
    count_filepath = '-k ' + sys.argv[1]


if output_labels != '':
    required_input = output_paths + ' ' + output_labels
else:
    required_input = count_filepath

# Let mageck handle the rest of the arguments
all_args = ' '.join(sys.argv[2:])
mageck_cmd = ' '.join(['mageck count', required_input, all_args])
subprocess.call(mageck_cmd, shell=True)
