import os
import shutil
import sys
import pandas as pd


def read_file(file_name):
    data = pd.read_csv(file_name, sep="\t")
    data = data.loc[data['Hierarchy Level'] == 1]
    metrics = ['Front-End Bound', 'Bad Speculation', 'Back-End Bound', 'Retiring', 'Clockticks', 'Instructions Retired']
    data = data.loc[data['Metric Name'].isin(metrics)]
    return data


def save_file(service_name, data, output_dir, file_to_write):
    clock_ticks = float(data.loc[data['Metric Name'] == 'Clockticks']['Metric Value'].values[0])
    instructions = float(data.loc[data['Metric Name'] == 'Instructions Retired']['Metric Value'].values[0])
    frontend_bound = float(data.loc[data['Metric Name'] == 'Front-End Bound']['Metric Value'].values[0])
    bad_speculation = float(data.loc[data['Metric Name'] == 'Bad Speculation']['Metric Value'].values[0])
    backend_bound = float(data.loc[data['Metric Name'] == 'Back-End Bound']['Metric Value'].values[0])
    retiring = float(data.loc[data['Metric Name'] == 'Retiring']['Metric Value'].values[0])
    ipc_value = instructions / clock_ticks

    data = {
        'Service Name': [service_name],
        'Front-End Bound': [frontend_bound],
        'Bad Speculation': [bad_speculation],
        'Back-End Bound': [backend_bound],
        'Retiring': [retiring],
        'IPC': [ipc_value]
    }

    df = pd.DataFrame(data)
    df.to_csv(output_dir + file_to_write, mode='a', index=False, header=False)


def append_results(dir_path, file_to_write, file_to_read, output_dir):
    data = read_file(dir_path + '/' + file_to_read)
    save_file(file_to_read.split('.')[0], data, output_dir, file_to_write)


def generate_output(dir_path, file_to_write):
    output_dir = dir_path + '/result/'
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir, ignore_errors=True)

    os.mkdir(output_dir)

    header = {
        'Service Name': [],
        'Front-End Bound': [],
        'Bad Speculation': [],
        'Back-End Bound': [],
        'Retiring': [],
        'IPC': []
    }

    df = pd.DataFrame(header)
    df.to_csv(output_dir + file_to_write, mode='a', index=False)

    for filename in os.listdir(dir_path):
        if '.csv' in filename:
            append_results(dir_path, file_to_write, filename, output_dir)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        generate_output(sys.argv[1], sys.argv[2])
    else:
        print('Not enough args. EXAMPLE: python <dir_to_search> <output_file>')
