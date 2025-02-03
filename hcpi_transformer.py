def transform(file_path, years, output_csv=None):
    coicop_descriptions = {
        "CP01": "Food and non-alcoholic beverages",
        "CP02": "Alcoholic beverages and tobacco",
        "CP03": "Clothing and footwear",
        "CP04": "Housing, water, electricity, gas and other fuels",
        "CP05": "Household furnishings/equipment/maintenance",
        "CP06": "Health",
        "CP07": "Transport",
        "CP08": "Communication",
        "CP09": "Recreation and culture",
        "CP10": "Education",
        "CP11": "Restaurants and hotels",
        "CP12": "Miscellaneous goods and services",
    }

    # Add list to store results if output_csv is specified
    results = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            import csv

            delimiter = "," if file_path.lower().endswith(".csv") else "\t"
            reader = csv.reader(file, delimiter=delimiter)

            # Get header row and find indices
            header = next(reader)
            try:
                geo_index = header.index("geo")
                coicop_index = header.index("coicop")
                year_indices = {
                    year: header.index(f"{year} ") for year in years
                }  # Note the space after year
            except ValueError:
                print(
                    f"Error: One or more years not found in file. Available years may be missing."
                )
                return

            # Calculate total width needed for years columns
            year_column_width = 12 * len(years)

            # Print header
            print("\n+" + "-" * 60 + "+" + "-" * year_column_width + "+")
            years_header = "".join(f" | {year:>10}" for year in years)
            print(f"| {'Category and Description':<58}{years_header} |")
            print("+" + "=" * 60 + "+" + ("=" * 12) * len(years) + "+")

            # Read and process rows
            sums = {year: 0 for year in years}
            for row in reader:
                if (
                    row
                    and row[geo_index] == "FR"
                    and "CP" in row[coicop_index]
                    and "CP00" not in row[coicop_index]
                    and len(row[coicop_index]) == 4
                ):
                    coicop_code = row[coicop_index].strip()
                    category_num = coicop_code[2:]
                    description = coicop_descriptions.get(coicop_code, coicop_code)
                    formatted_description = f"{category_num}. {description}"

                    # Get values for all years
                    values = []
                    for year in years:
                        value = row[year_indices[year]].strip()
                        values.append(value)
                        if value != ":" and value.strip():
                            try:
                                sums[year] += float(value)
                            except ValueError:
                                pass

                    # Print row with all years
                    values_str = "".join(f" | {val:>10}" for val in values)
                    print(f"| {formatted_description:<58}{values_str} |")
                    print("+" + "-" * 60 + "+" + ("-" * 12) * len(years) + "+")

                    # Store results if output_csv specified
                    if output_csv:
                        result_row = {
                            "category": coicop_code,
                            "description": description,
                        }
                        for year, value in zip(years, values):
                            result_row[str(year)] = value
                        results.append(result_row)

            # Print sums for all years
            print("\nSums:")
            for year in years:
                print(f"{year}: {sums[year]:.2f}")

            # Write results to CSV if output path specified
            if output_csv and results:
                import pandas as pd

                df = pd.DataFrame(results)
                df.to_csv(output_csv, index=False)
                print(f"\nResults written to {output_csv}")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
    except Exception as e:
        print(f"Error reading file: {str(e)}")


def transform_category(file_path, category, years, output_csv=None):
    # Validate category format
    if not category.startswith("CP") or len(category) != 4:
        print("Error: Category must be in format 'CPxx' (e.g., 'CP12')")
        return

    # Add list to store results if output_csv is specified
    results = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            import csv

            delimiter = "," if file_path.lower().endswith(".csv") else "\t"
            reader = csv.reader(file, delimiter=delimiter)

            # Get header row and find indices
            header = next(reader)
            try:
                geo_index = header.index("geo")
                coicop_index = header.index("coicop")
                year_indices = {year: header.index(f"{year} ") for year in years}
            except ValueError:
                print(
                    f"Error: One or more years not found in file. Available years may be missing."
                )
                return

            # Calculate total width needed for years columns
            year_column_width = 12 * len(years)

            # Print header
            print(f"\nBreakdown for category {category}:")
            print("+" + "-" * 60 + "+" + "-" * year_column_width + "+")
            years_header = "".join(f" | {year:>10}" for year in years)
            print(f"| {'Subcategory':<58}{years_header} |")
            print("+" + "=" * 60 + "+" + ("=" * 12) * len(years) + "+")

            # Read and process rows
            sums = {year: 0 for year in years}
            for row in reader:
                if (
                    row
                    and row[geo_index] == "FR"
                    and row[coicop_index].startswith(category)
                    and len(row[coicop_index]) == 5
                ):
                    coicop_code = row[coicop_index].strip()
                    subcategory = f"{coicop_code[2:4]}.{coicop_code[4]}"

                    # Get values for all years
                    values = []
                    for year in years:
                        value = row[year_indices[year]].strip()
                        values.append(value)
                        if value != ":" and value.strip():
                            try:
                                sums[year] += float(value)
                            except ValueError:
                                pass

                    # Print row with all years
                    values_str = "".join(f" | {val:>10}" for val in values)
                    print(f"| {subcategory:<58}{values_str} |")
                    print("+" + "-" * 60 + "+" + ("-" * 12) * len(years) + "+")

                    # Store results if output_csv specified
                    if output_csv:
                        result_row = {
                            "subcategory": coicop_code,
                            "description": subcategory,
                        }
                        for year, value in zip(years, values):
                            result_row[str(year)] = value
                        results.append(result_row)

            # Print sums for all years
            print("\nSums:")
            for year in years:
                print(f"{year}: {sums[year]:.2f}")

            # Write results to CSV if output path specified
            if output_csv and results:
                import pandas as pd

                df = pd.DataFrame(results)
                df.to_csv(output_csv, index=False)
                print(f"\nResults written to {output_csv}")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
    except Exception as e:
        print(f"Error reading file: {str(e)}")


def convert_to_tsv(input_file, output_file=None):
    if output_file is None:
        # If no output file specified, create name by replacing .csv with .tsv
        output_file = input_file.replace(".csv", ".tsv")

    try:
        with open(input_file, "r", encoding="utf-8") as infile:
            content = infile.read()
            # Replace commas with tabs
            converted_content = content.replace(",", "\t")

        with open(output_file, "w", encoding="utf-8") as outfile:
            outfile.write(converted_content)

        print(f"Successfully converted {input_file} to {output_file}")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
    except Exception as e:
        print(f"Error processing file: {str(e)}")


# Example usage:
# transform("estat_prc_hicp_aind.tsv", range(1996, 2023), "hcpi_indexes.csv")
transform_category(
    "estat_prc_hicp_inw.tsv",
    "CP12",
    range(1996, 2024),
    "hcpi_miscellaneous_weights.csv",
)
# convert_to_tsv("estat_prc_hicp_aind.tsv")
