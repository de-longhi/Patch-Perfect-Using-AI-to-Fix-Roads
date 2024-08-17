import csv
import re

def sort_csv(input_file, output_file):
    # Read the data from the input CSV file
    with open(input_file, mode='r') as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Read the header row
        rows = list(reader)    # Read the rest of the rows

    # Define a function to extract the numeric part from the filename
    def extract_number(filename):
        match = re.search(r'mask_p(\d+)\.jpg', filename)
        if match:
            return int(match.group(1))
        return 0  # Default to 0 if no match is found

    # Sort rows by the extracted number
    sorted_rows = sorted(rows, key=lambda x: extract_number(x[0]))

    # Write the sorted data to the output CSV file
    with open(output_file, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)  # Write the header row
        writer.writerows(sorted_rows)  # Write the sorted rows

# Set your input and output file paths
input_csv = 'image_classes.csv'
output_csv = 'sorted_output.csv'

# Call the function to sort the CSV file
sort_csv(input_csv, output_csv)
