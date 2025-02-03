import pandas as pd
import numpy as np


def interpolate_gini_coefficients(filename):
    # Read the CSV file
    df = pd.read_csv(filename)

    # Create a complete range of years for each country
    countries = df["Entity"].unique()
    interpolated_data = []

    for country in countries:
        country_data = df[df["Entity"] == country].copy()

        # Get min year and set max year to 2022
        min_year = country_data["Year"].min()
        max_year = 2022  # Changed to fixed value of 2022

        # Create a template DataFrame with all years
        full_years = pd.DataFrame(
            {
                "Year": range(min_year, max_year + 1),
                "Entity": country,
                "Code": country_data["Code"].iloc[0],
            }
        )

        # Merge with existing data
        merged = full_years.merge(
            country_data, on=["Year", "Entity", "Code"], how="left"
        )

        # Interpolate the Gini coefficient and forward fill any remaining NaN values
        merged["Average annual working hours per worker"] = (
            merged["Average annual working hours per worker"]
            .interpolate(method="linear")
            .ffill()
        )

        interpolated_data.append(merged)

    # Combine all interpolated data
    result = pd.concat(interpolated_data, ignore_index=True)

    # Sort by country and year
    result = result.sort_values(["Entity", "Year"])

    # Write to new CSV file
    output_filename = filename.replace(".csv", "_interpolated.csv")
    result.to_csv(output_filename, index=False)

    return output_filename


def transform_gini_coefficients(filename):
    # Read the interpolated Gini data
    df = pd.read_csv(filename)

    # Pivot the data to get years as columns
    pivoted = df.pivot(
        index=["Entity", "Code"],
        columns="Year",
        values="Average annual working hours per worker",
    ).reset_index()

    # Create the AMECO-style metadata columns
    ameco_columns = {
        "SERIES": "",
        "CNTRY": pivoted["Code"],
        "TRN": "",
        "AGG": "",
        "UNIT": "",
        "REF": "",
        "CODE": "",
        "COUNTRY": pivoted["Entity"],
        "SUB-CHAPTER": "",
        "TITLE": "Average annual working hours per worker",
        "UNIT.1": "Hours",
    }

    # Create new dataframe with AMECO format
    result = pd.DataFrame(ameco_columns)

    # Add the year columns from the pivoted data
    year_columns = pivoted.drop(["Entity", "Code"], axis=1)
    result = pd.concat([result, year_columns], axis=1)

    # Save to Excel instead of CSV
    result.to_excel("WorkingHours.xlsx", index=False)

    return "WorkingHours.xlsx"


interpolate_gini_coefficients("annual-working-hours-per-worker.csv")
transform_gini_coefficients("annual-working-hours-per-worker_interpolated.csv")
