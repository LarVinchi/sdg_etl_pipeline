# sdg_etl_pipeline
AICA Data Engineering ETL pipeline Project

# SDG ETL Pipeline

This project extracts SDG (Sustainable Development Goals) data from the UNDP API, cleans and transforms it, merges it with a country reference dataset, and saves the cleaned data as a CSV file. Optional analysis is included to explore the data.

## Project Overview

The ETL pipeline consists of the following stages:

1. **Extract**: Fetch JSON data from the UNDP SDG Index API.
2. **Transform**: 
   - Normalize the top recipients data from JSON.
   - Merge with a country reference CSV.
   - Clean the dataset by removing incomplete rows and renaming columns.
3. **Load**: Save the transformed dataset as a CSV file.
4. **Optional Analysis**: Basic insights like top countries by recipient budget and number of countries per region.

## Project Structure

- `extract_transform_load.py` : Python ETL script
- `sdg_index_data.json` : Raw JSON data from the API
- `sdg_recipients_cleaned.csv` : Transformed CSV dataset
- `all_countries.csv` : Country reference dataset
- `README.md` : Project documentation

## How to Run

1. Ensure Python installed.
2. Install dependencies (if not already):

pip install pandas requests
