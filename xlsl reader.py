import pandas as pd
import os


def find_deflator_rows():
    # Get all xlsx files in current directory
    xlsx_files = [f for f in os.listdir(".") if f.endswith((".XLSX", ".xlsx"))]

    if not xlsx_files:
        print("No Excel files found in current directory")
        return

    # Set to store unique file-title pairs
    seen_pairs = set()

    for file in xlsx_files:
        try:
            # Read the Excel file
            df = pd.read_excel(file)

            # Check if 'TITLE' column exists
            if "TITLE" not in df.columns:
                print(f"Warning: File {file} does not contain a 'TITLE' column")
                continue

            # Filter rows where TITLE contains 'deflator' (case insensitive)
            deflator_rows = df[
                df["TITLE"].str.contains("Financial", case=False, na=False)
            ]

            if not deflator_rows.empty:
                # Only print the TITLE column values
                for title in deflator_rows["TITLE"]:
                    # Create a tuple of file and title
                    pair = (file, title)
                    # Only print if we haven't seen this pair before
                    if pair not in seen_pairs:
                        print(f"File: {file} - Title: {title}")
                        seen_pairs.add(pair)

        except Exception as e:
            print(f"Error reading file {file}: {str(e)}")


def export_all_titles_to_csv():
    # Get all xlsx files in current directory
    xlsx_files = [f for f in os.listdir(".") if f.endswith((".XLSX", ".xlsx"))]

    if not xlsx_files:
        print("No Excel files found in current directory")
        return

    # Create a list to store all titles and their source files
    all_titles = []

    for file in xlsx_files:
        try:
            # Read the Excel file
            df = pd.read_excel(file)

            # Check if 'TITLE' column exists
            if "TITLE" not in df.columns:
                print(f"Warning: File {file} does not contain a 'TITLE' column")
                continue

            # Get all titles from the file
            titles = df["TITLE"].dropna()  # Remove any NA values

            # Add each title with its source file to the list
            for title in titles:
                all_titles.append({"File": file, "Title": title})

        except Exception as e:
            print(f"Error reading file {file}: {str(e)}")

    # Create a DataFrame from all collected titles
    titles_df = pd.DataFrame(all_titles)

    # Export to CSV
    try:
        titles_df.to_csv("titles_list.csv", index=False)
        print(f"Successfully exported {len(all_titles)} titles to titles_list.csv")
    except Exception as e:
        print(f"Error writing to CSV: {str(e)}")


if __name__ == "__main__":
    export_all_titles_to_csv()
