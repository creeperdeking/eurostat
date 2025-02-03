def filter_france_data(input_csv_name, output_csv_name="france_expenditure.csv"):
    import pandas as pd

    # Read the CSV file
    df = pd.read_csv(input_csv_name)

    # Filter for France only
    france_df = df[df["Entity"] == "France"]

    # Save to new CSV file
    france_df.to_csv(output_csv_name, index=False)

    return france_df


filter_france_data("government-expenditure-vs-gdp.csv")
