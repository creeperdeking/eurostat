import pandas as pd
import numpy as np


def merge_retirement(filename1, filename2):
    # Read the CSV files
    df1 = pd.read_csv(filename1)
    df2 = pd.read_csv(filename2)

    # Rename columns to distinguish between men and women
    df1.columns = ["Entity", "Code", "Year", "Women_Retirement_Age"]
    df2.columns = ["Entity", "Code", "Year", "Men_Retirement_Age"]

    # Merge the dataframes on Entity, Code, and Year
    merged_df = pd.merge(df1, df2, on=["Entity", "Code", "Year"], how="outer")

    # Check for missing data
    missing_women = merged_df[merged_df["Women_Retirement_Age"].isna()]
    missing_men = merged_df[merged_df["Men_Retirement_Age"].isna()]

    # Print missing data information
    if not missing_women.empty:
        print("\nMissing women's retirement age data:")
        for _, row in missing_women.iterrows():
            print(f"Year: {row['Year']}, Country: {row['Entity']}, File: {filename1}")

    if not missing_men.empty:
        print("\nMissing men's retirement age data:")
        for _, row in missing_men.iterrows():
            print(f"Year: {row['Year']}, Country: {row['Entity']}, File: {filename2}")

    # Calculate the average retirement age
    merged_df["Average_Retirement_Age"] = (
        merged_df["Women_Retirement_Age"] + merged_df["Men_Retirement_Age"]
    ) / 2

    # Create final dataframe with required columns
    final_df = merged_df[["Entity", "Code", "Year", "Average_Retirement_Age"]]

    # Rename the average column to match the desired format
    final_df.columns = [
        "Entity",
        "Code",
        "Year",
        "Average effective age of retirement (OECD)",
    ]

    # Save to CSV
    final_df.to_csv("retirement.csv", index=False)


def fill_missing_data(filename):
    # Read the CSV file
    df = pd.read_csv(filename)

    # Convert Year to int to ensure proper sorting
    df["Year"] = df["Year"].astype(int)

    # Create full year range from 1960 to 2022
    full_years = pd.DataFrame({"Year": range(1960, 2023)})

    # Process each country separately
    entities = df["Entity"].unique()
    complete_data = []

    for entity in entities:
        entity_data = df[df["Entity"] == entity].copy()
        entity_code = entity_data["Code"].iloc[0]

        # Merge with full years to identify gaps
        entity_full = full_years.merge(entity_data, on="Year", how="left")

        # Forward extrapolation
        last_year = entity_data["Year"].max()
        if last_year < 2022:  # Do forward extrapolation if data ends before 2022
            # Get last 4 known years
            last_known = entity_data.nlargest(4, "Year")
            if len(last_known) >= 2:  # Need at least 2 points for regression
                X = last_known["Year"].values.reshape(-1, 1)
                y = last_known["Average effective age of retirement (OECD)"].values
                model = np.polyfit(X.flatten(), y, 1)

                # Predict forward
                future_years = range(int(last_year + 1), 2023)
                for year in future_years:
                    predicted_value = model[0] * year + model[1]
                    complete_data.append(
                        {
                            "Entity": entity,
                            "Code": entity_code,
                            "Year": year,
                            "Average effective age of retirement (OECD)": predicted_value,
                        }
                    )

        # Backward extrapolation
        first_year = entity_data["Year"].min()
        if (
            first_year > 1960
        ):  # Only do backward extrapolation if data starts after 1960
            # Get first 4 known years
            first_known = entity_data.nsmallest(4, "Year")
            if len(first_known) >= 2:  # Need at least 2 points for regression
                X = first_known["Year"].values.reshape(-1, 1)
                y = first_known["Average effective age of retirement (OECD)"].values
                model = np.polyfit(X.flatten(), y, 1)

                # Predict backward
                past_years = range(1960, int(first_year))
                for year in past_years:
                    predicted_value = model[0] * year + model[1]
                    complete_data.append(
                        {
                            "Entity": entity,
                            "Code": entity_code,
                            "Year": year,
                            "Average effective age of retirement (OECD)": predicted_value,
                        }
                    )

        # Add existing data
        complete_data.extend(entity_data.to_dict("records"))

    # Create final dataframe and sort
    final_df = pd.DataFrame(complete_data)
    final_df = final_df.sort_values(["Entity", "Year"])

    # Save to CSV
    final_df.to_csv("retirement_filled.csv", index=False)


merge_retirement(
    "average-effective-retirement-women.csv",
    "average-effective-retirement-men.csv",
)
fill_missing_data("retirement.csv")
