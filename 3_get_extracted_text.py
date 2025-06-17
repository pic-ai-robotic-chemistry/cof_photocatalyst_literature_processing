import csv
import sys
def extract_relevant(input_csv, output_txt):
    with open(input_csv, 'r') as csv_file, open(output_txt, 'w') as txt_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row[1].strip().lower() == "relevant":
                txt_file.write(row[0] + '\n')
input_file = sys.argv[1]
output_file = sys.argv[2]
# Replace with your actual filenames
extract_relevant(input_file, output_file)
