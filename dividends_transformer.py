def transform(file_path):
    # Open both input and output files
    with open(file_path, "r") as input_file, open("dividends.csv", "w") as output_file:
        for line in input_file:
            # Write T4 lines to the output file
            if "-T4," in line:
                output_file.write(line)


transform("valeurs_trimestrielles.csv")
