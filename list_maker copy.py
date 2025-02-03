import numpy as np
import csv


def interpolate_csv_values(input_file, output_file):
    """
    Read a single-column CSV file and create a new CSV with interpolated values,
    generating 12 values between each original value.

    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file
    """
    # Read the original values
    values = []
    with open(input_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0].strip():  # Check if row exists and is not empty
                try:
                    values.append(float(row[0]))
                except ValueError:
                    continue  # Skip non-numeric values

    # Create interpolated values
    interpolated_values = []
    for i in range(len(values) - 1):
        # Create 12 points between each pair of values
        start_val = values[i]
        end_val = values[i + 1]
        intermediate_vals = np.linspace(start_val, end_val, 13)[
            :-1
        ]  # Remove last point to avoid duplication
        interpolated_values.extend(intermediate_vals)

    # Add the last value
    interpolated_values.append(values[-1])

    # Write to output CSV
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        for value in reversed(interpolated_values):
            writer.writerow([value])

    print(f"Successfully created interpolated values in {output_file}")


def reverse_csv_values(input_file, output_file):
    """
    Read a single-column CSV file and create a new CSV with reversed values.

    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file
    """
    # Read the values
    values = []
    with open(input_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0].strip():  # Check if row exists and is not empty
                try:
                    values.append(float(row[0]))
                except ValueError:
                    continue  # Skip non-numeric values

    # Write reversed values to output CSV
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        for value in reversed(values):
            writer.writerow([value])

    print(f"Successfully created reversed values in {output_file}")


def reverse_csv_columns(input_file, output_file):
    """
    Read a CSV file and create a new CSV with columns in reverse order.

    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file
    """
    # Read all rows
    rows = []
    with open(input_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:  # Check if row is not empty
                rows.append(row)

    # Write reversed columns to output CSV
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row[::-1])  # Reverse the order of columns

    print(f"Successfully created column-reversed CSV in {output_file}")


# Example usage
# interpolate_csv_values("list.csv", "list_interpolated.csv")
# reverse_csv_values("list.csv", "list_reversed.csv")
reverse_csv_columns("table.csv", "table_columns_reversed.csv")
