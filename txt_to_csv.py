import csv


def txt_to_csv(input_file, output_file):
    with open(input_file, "r") as in_file, open(
        output_file, "w", newline=""
    ) as out_file:
        # Create a CSV writer object
        csv_writer = csv.writer(out_file)

        # Read each line from the input file
        for line in in_file:
            # Split the line into number and word
            number, word = line.strip().split(" ", 1)

            # Write the row to the CSV file
            csv_writer.writerow([number, word])
