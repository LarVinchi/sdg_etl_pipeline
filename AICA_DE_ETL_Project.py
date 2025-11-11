# %% [Imports]
import requests
import pandas as pd
import json

# %% [Stage 1: Extract JSON Data from API]
def extract_sdg_data(api_url: str, save_path: str) -> dict:
    """
    Fetch SDG data from API and save as JSON locally.
    Returns the data as a Python dict.
    """
    response = requests.get(api_url)
    response.raise_for_status()  # Raise error if request fails
    data = response.json()
    
    # Save JSON file
    with open(save_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
    print(f"JSON file saved at {save_path}")
    return data


# %% [Stage 2: Transform SDG Recipients Data]
def transform_sdg_data(data: dict, country_csv_path: str) -> pd.DataFrame:
    """
    Normalize top recipients from JSON, merge with country reference, and clean data.
    Returns cleaned DataFrame.
    """
    # Normalize recipients
    df_recipients = pd.json_normalize(
        data,
        record_path=['top_recipients'],
        meta=["sdg_code", "sdg_name"],
        meta_prefix="parent_"
    )

    # Rename columns
    df_recipients.rename(columns={
        "name": "country_name",
        "iso3": "iso3",
        "total_budget": "recipient_budget",
        "total_expense": "recipient_expense",
        "parent_sdg_code": "sdg_code",
        "parent_sdg_name": "sdg_name"
    }, inplace=True)

    # Load country reference and merge
    countries = pd.read_csv(country_csv_path)
    countries.rename(columns={"country": "country_name"}, inplace=True)
    
    merged = pd.merge(df_recipients, countries, on="iso3", how="left")
    
    # Filter rows with valid capital, region, and continents
    filtered = merged.dropna(subset=['capital', 'region', 'continents'])
    
    # Drop old country_name_x and rename country_name_y
    cleaned = filtered.drop(columns=['country_name_x']).rename(columns={'country_name_y': 'country'})
    
    print("Data transformation complete")
    return cleaned


# %% [Stage 3: Load Transformed Data]
def load_to_csv(cleaned: pd.DataFrame, csv_save_path: str):
    """
    Save cleaned DataFrame as CSV.
    """
    cleaned.to_csv(csv_save_path, index=False)
    print(f"Cleaned data saved to CSV at {save_path}")


# %% [Optional: Basic Analysis]
def analyze_data(cleaned: pd.DataFrame):
    """
    Perform basic analysis on the SDG recipients dataset.
    """
    print("=== Top 10 Countries by Total Recipient Budget ===")
    print(cleaned.groupby('country')['recipient_budget'].sum().sort_values(ascending=False).head(10))
    
    print("\n=== Number of Countries per Region ===")
    print(cleaned['region'].value_counts())


# %% [Main ETL Pipeline]
if __name__ == "__main__":
    api_url = 'https://api.open.undp.org/api/sdg-index.json'
    save_path = r"C:\Users\NOC1\Desktop\sl\Python\Data_Engineering\sdg_index_data.json"
    country_csv_path = "all_countries.csv"
    csv_save_path = r"C:\Users\NOC1\Desktop\sl\Python\Data_Engineering\sdg_recipients_cleaned.csv"

    # Extract
    raw_data = extract_sdg_data(api_url, save_path)
    
    # Transform
    cleaned = transform_sdg_data(raw_data, country_csv_path)
    
    # Load
    load_to_csv(cleaned, csv_save_path)
    
    # Optional Analysis
    analyze_data(cleaned)
