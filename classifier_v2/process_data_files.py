import os
import pandas as pd
import csv

src_folder = "classifier_v2/data"
src_num = "2"

def split(filehandler, delimiter=',', row_limit=60, ignored_start=30, num_files=10,
    output_name_template='output_%s.csv', output_path='classifier_v2/data/all_data', keep_headers=True):
    """
    Splits a CSV file into multiple pieces.
    
    A quick bastardization of the Python CSV library.

    Arguments:

        `row_limit`: The number of rows you want in each output file. 10,000 by default.
        `ignored_start` : The number of rows you want to skip before starting a new output file. 30 by default.
        `num_files` : The number of files you want. 10 by default.
        `output_name_template`: A %s-style template for the numbered output files.
        `output_path`: Where to stick the output files.
        `keep_headers`: Whether or not to print the headers in each output file.

    Example usage:
    
        >> from toolbox import csv_splitter;
        >> csv_splitter.split(open('/home/ben/input.csv', 'r'));
    
    """
    reader = csv.reader(filehandler, delimiter=delimiter)
    current_piece = 1
    current_out_path = os.path.join(
         output_path,
         output_name_template % current_piece
    )
    current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
    current_limit = row_limit
    if keep_headers:
        headers = next(reader)
        current_out_writer.writerow(headers)

    # get rid of first ignored_start lines
    for _ in range(ignored_start):
        next(reader)

    for i, row in enumerate(reader):

        if i + 1 > current_limit:

            current_piece += 1

            if current_piece > num_files:
                break

            current_limit = row_limit * current_piece
            current_out_path = os.path.join(
               output_path,
               output_name_template  % current_piece
            )
            current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
            if keep_headers:
                current_out_writer.writerow(headers)
        current_out_writer.writerow(row)

if __name__ == '__main__':

    for state in ["active", "meditate", "neutral"]:
        read_file = pd.read_excel(os.path.join(src_folder, src_num, state + ".xlsx"))
        read_file.to_csv(os.path.join(src_folder, src_num, state + ".csv"), index=False)
        
        split(open(f'{src_folder}/{src_num}/{state}.csv', 'r'), output_name_template=f'{state}_{src_num}_' + '%s.csv')