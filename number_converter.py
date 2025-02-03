def convert_decimals(input_file):
    """
    Convert decimal separators from comma to period and change delimiters from colon to comma
    in a colon-delimited CSV file.

    Args:
        input_file (str): Path to the input CSV file
    """
    # Generate output filename by adding '_converted' before the extension
    output_file = (
        input_file.rsplit(".", 1)[0] + "_converted." + input_file.rsplit(".", 1)[1]
    )

    try:
        # Read the input file and process line by line
        with open(input_file, "r", encoding="utf-8") as infile:
            with open(output_file, "w", encoding="utf-8") as outfile:
                for line in infile:
                    # First replace decimal commas with periods
                    converted_line = line.replace(",", ".")
                    # Then replace colons with commas
                    converted_line = converted_line.replace(":", ",")
                    outfile.write(converted_line)

        print(f"Successfully converted {input_file} to {output_file}")

    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Example usage
convert_decimals("oddnums.csv")
