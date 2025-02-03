import pandas as pd
import os
from typing import List
import re


def read_excel_files() -> List[pd.DataFrame]:
    # Get all xlsx files in current directory
    xlsx_files = [f for f in os.listdir(".") if f.lower().endswith(".xlsx")]
    if not xlsx_files:
        print("No Excel files found in current directory")
        return
    try:
        return [pd.read_excel(file) for file in xlsx_files]
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return []


def search_keywords_in_excel(
    keywords, units, excel_files: List[pd.DataFrame], exclude_keywords: List[str] = []
):
    # Create a list to store all matching rows
    all_matches = []

    for df in excel_files:
        # Escape special regex characters in keywords
        escaped_keywords = [re.escape(keyword) for keyword in keywords]
        keyword_filter = df.iloc[:, 9].str.contains(
            "|".join(escaped_keywords), case=False, na=False
        )
        # Use exact matching for units
        unit_filter = df.iloc[:, 10].isin(units)

        # Add exclude filter if exclude_keywords is not empty
        if exclude_keywords:
            escaped_exclude = [re.escape(keyword) for keyword in exclude_keywords]
            exclude_filter = ~df.iloc[:, 9].str.contains(
                "|".join(escaped_exclude), case=False, na=False
            )
            # Combine all filters with AND operation
            filter_condition = keyword_filter & unit_filter & exclude_filter
        else:
            # Use original filters if no exclude keywords
            filter_condition = keyword_filter & unit_filter

        # Get matching rows
        matching_rows = df[filter_condition]

        if not matching_rows.empty:
            all_matches.append(matching_rows)

    if all_matches:
        # Combine all matching rows and save to CSV
        result_df = pd.concat(all_matches, ignore_index=True)

        # Count occurrences of each country
        country_counts = result_df.iloc[:, 1].value_counts()
        # Keep only countries that appear for all keywords
        valid_countries = country_counts[country_counts >= len(keywords)].index
        # Filter the dataframe to keep only valid countries
        result_df = result_df[result_df.iloc[:, 1].isin(valid_countries)]
        return result_df

    else:
        print("No matches found for the given keywords")


# put all results into a single csv (ameco_data.csv)
def results_to_csv(result_df: pd.DataFrame | List[pd.DataFrame], filename: str):
    """
    Saves a DataFrame or combines multiple dataframes and saves them to a CSV file.

    Args:
        result_df: A pandas DataFrame or list of pandas DataFrames to be saved
        filename: Name of the output CSV file
    """
    # Check if input is None or empty list
    if result_df is None or (isinstance(result_df, list) and len(result_df) == 0):
        print("No data to save")
        return

    # Handle single DataFrame
    if isinstance(result_df, pd.DataFrame):
        combined_df = result_df
    else:
        # Combine multiple dataframes
        combined_df = pd.concat(result_df, ignore_index=True)

    # Replace 'Germany ("linked")' with 'Germany' in the country column (index 7)
    combined_df.iloc[:, 7] = combined_df.iloc[:, 7].replace(
        'Germany ("linked")', "Germany"
    )

    # Save to CSV
    combined_df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


if __name__ == "__main__":
    excel_files = read_excel_files()

    results = search_keywords_in_excel(
        [
            "Compensation of employees: total economy",
            "Taxes linked to imports and production minus subsidies: total economy",
            "Consumption of fixed capital at current prices: total economy",
            "Net operating surplus: total economy :- Adjusted for imputed compensation of self-employed",
            "Gross operating surplus: total economy",
            "Gross operating surplus: total economy :- Adjusted for imputed compensation of self-employed",
            "Net primary income from the rest of the world",
        ],
        ["Mrd ECU/EUR"],
        excel_files,
    )
    results2 = search_keywords_in_excel(
        [
            "Population: 0 to 14 years",
            "Population: 15 to 64 years",
            "Population: 65 years and over",
            "Total population",
            "Employment, persons: total economy",
            "Total unemployment :- Member States: definition EUROSTAT",
        ],
        ["1000 persons"],
        excel_files,
        ["Total population (National accounts)"],
    )
    results3 = search_keywords_in_excel(
        [
            "Private final consumption expenditure at current prices",
            "Individual consumption of general government at current prices",
            "Collective consumption of general government at current prices",
            "Gross capital formation at current prices: total economy",
            "Consumption of fixed capital at current prices: total economy",
            "Net exports of goods and services at current prices",
        ],
        ["Mrd ECU/EUR"],
        excel_files,
    )
    results4 = search_keywords_in_excel(
        [
            "Subsidies: general government :- ESA 2010",
            "Social benefits other than social transfers in kind: general government :- ESA 2010 ",
            "Social transfers in kind supplied to households via market producers: general government :- ESA 2010 ",
            "Interest: general government :- ESA 2010 ",
            "Compensation of employees: general government :- ESA 2010 ",
            "Intermediate consumption: general government :- ESA 2010 ",
            "Other current expenditure: general government :- ESA 2010 ",
            "Gross fixed capital formation: general government :- ESA 2010 ",
            "Other capital expenditure, including capital transfers: general government :- ESA 2010 ",
        ],
        ["(Percentage of GDP at current prices (excessive deficit procedure)) "],
        excel_files,
    )
    results5 = search_keywords_in_excel(
        [
            "Average annual working hours per worker",
            "Price deflator private final consumption expenditure",
            "Gross domestic product at current prices",
        ],
        ["Hours", "ECU/EUR: 2015 = 100", "Mrd ECU/EUR"],
        excel_files,
    )
    results6 = search_keywords_in_excel(
        [
            "Employment, persons: agriculture, forestry and fishery products",
            "Employment, persons: industry excluding building and construction",
            "Employment, persons: building and construction",
            "Employment, persons: services",
        ],
        ["1000 persons"],
        excel_files,
    )
    results7 = search_keywords_in_excel(
        [
            "Price deflator gross value added: agriculture, forestry and fishery products",
            "Price deflator gross value added: industry excluding building and construction",
            "Price deflator gross value added: building and construction",
            "Price deflator gross value added: services",
            "Gross Value Added at current prices: agriculture, forestry and fishery products",
            "Gross value added at current prices: industry excluding building and construction",
            "Gross value added at current prices: building and construction",
            "Gross value added at current prices: services",
        ],
        ["Mrd ECU/EUR", "ECU/EUR: 2015 = 100"],
        excel_files,
    )
    results8 = search_keywords_in_excel(
        [
            "Exports of goods at current prices",
            "Price deflator exports of goods",
            "Exports of services at current prices",
            "Price deflator exports of services",
            "Imports of goods at current prices",
            "Price deflator imports of goods",
            "Imports of services at current prices",
            "Price deflator imports of services",
            "Price deflator gross domestic product",
        ],
        ["Mrd ECU/EUR", "ECU/EUR: 2015 = 100"],
        excel_files,
        [
            "Net exports of services at current prices (National accounts) ",
            "Net exports of goods at current prices (National accounts) ",
            "Price deflator exports of goods and services ",
            "Price deflator imports of goods and services ",
        ],
    )
    results_to_csv(
        [results, results2, results3, results4, results5, results6, results7, results8],
        "ameco_data.csv",
    )
