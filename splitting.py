import csv
from deep_translator import GoogleTranslator
import unicodedata
import re

def remove_arabic_chars(input_file, output_file):
    with open(input_file, encoding='utf-8') as file_in, \
            open(output_file, 'w', newline='', encoding='utf-8') as file_out:
        reader = csv.reader(file_in)
        writer = csv.writer(file_out)
        for row in reader:
            new_row = []
            for cell in row:
                cell = re.sub(r'[\u0600-\u06FF]+', '', cell)  # remove Arabic characters
                new_row.append(cell)
            writer.writerow(new_row)

def translate_csv(file_path, output_path):
    with open(file_path, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        with open(output_path, mode='w', newline='', encoding='utf-8') as output_file:
            csv_writer = csv.writer(output_file)
            for row in csv_reader:
                translated_row = []
                for cell in row:
                    if cell:
                        cell = GoogleTranslator(source='auto', target='en').translate(cell)
                    translated_row.append(cell)
                csv_writer.writerow(translated_row)

#write a function the removes emojis from csv file
def remove_emojis(input_file, output_file):
    with open(input_file, encoding='utf-8') as file_in, \
            open(output_file, 'w', newline='', encoding='utf-8') as file_out:
        reader = csv.reader(file_in)
        writer = csv.writer(file_out)
        for row in reader:
            new_row = []
            for cell in row:
                cell = re.sub(r'[^\w\s,]', '', cell)  # remove emojis
                new_row.append(cell)
            writer.writerow(new_row)

import os
import pandas as pd
def split_csv_by_lines(input_file, lines_per_file):
    counter=0
    # Read the input CSV file into a pandas dataframe
    df = pd.read_csv(input_file)

    # Get the total number of rows in the dataframe
    total_rows = df.shape[0]

    # Calculate the number of output files needed based on the number of lines per file
    num_output_files = (total_rows // lines_per_file) + 1

    # Loop through each output file and save a portion of the input data to it
    for i in range(num_output_files):
        # Calculate the start and end row indices for the current output file
        start_row = i * lines_per_file
        end_row = min((i + 1) * lines_per_file, total_rows)

        # Get the portion of the dataframe for the current output file
        output_data = df.iloc[start_row:end_row]

        # Construct the output file path for the current output file
        output_file = os.path.splitext(input_file)[0] + f"_part_{i+1}.csv"
        counter=counter+1

        # Write the output data to the output file
        output_data.to_csv(output_file, index=False)
    return counter
    

c=split_csv_by_lines("csvfile.csv", 200)

for i in range(1,c):
    translate_csv(f"csvfile_part_{i}.csv", f"output_part_{i}.csv")
    remove_arabic_chars(f"output_part_{i}.csv",f"output_part_{i}_non_arabic.csv")
    remove_emojis(f"output_part_{i}_non_arabic.csv",f"output_part_{i}_non_arabic_emojis.csv")
    os.remove(f"csvfile_part_{i}.csv")
    os.remove(f"output_part_{i}.csv")
    os.remove(f"output_part_{i}_non_arabic.csv")

dataframes = []

for i in range(1,c):
    filename = f"output_part_{i}_non_arabic_emojis.csv"
    df = pd.read_csv(filename, index_col=None, header=0)
    dataframes.append(df)

merged_df = pd.concat(dataframes, axis=0, ignore_index=True)

merged_df.to_csv("merged_non_arabic_emojis.csv", index=False)