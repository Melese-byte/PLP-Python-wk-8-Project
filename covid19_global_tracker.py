import pandas as pd
import matplotlib.pyplot as plt
import os

# ===================== CONFIG =====================
DATA_FILE = "owid-covid-data.csv"  # Place CSV in the same folder as this script
COUNTRIES = ["Kenya", "United States", "India"]  # Edit countries of interest
# ==================================================

def load_data(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"CSV file not found: {filepath}. "
                                "Download it from Our World in Data (owid-covid-data.csv).")
    df = pd.read_csv(filepath)
    return df

def clean_data(df, countries):
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    # Filter countries of interest
    df = df[df['location'].isin(countries)]
    # Fill missing values forward/backward
    df = df.fillna(method='ffill').fillna(method='bfill')
    return df

def exploratory_analysis(df):
    # Preview data
    print("Data Preview:")
    print(df.head(), "\n")
    print("Summary Statistics:")
    print(df.describe(include='all'), "\n")
    print("Missing values:")
    print(df.isnull().sum(), "\n")

def plot_cases_over_time(df):
    plt.figure(figsize=(10,6))
    for country in df['location'].unique():
        subset = df[df['location'] == country]
        plt.plot(subset['date'], subset['total_cases'], label=country)
    plt.title("Total COVID-19 Cases Over Time")
    plt.xlabel("Date")
    plt.ylabel("Total Cases")
    plt.legend()
    plt.show()

def plot_deaths_over_time(df):
    plt.figure(figsize=(10,6))
    for country in df['location'].unique():
        subset = df[df['location'] == country]
        plt.plot(subset['date'], subset['total_deaths'], label=country)
    plt.title("Total COVID-19 Deaths Over Time")
    plt.xlabel("Date")
    plt.ylabel("Total Deaths")
    plt.legend()
    plt.show()

def plot_vaccinations(df):
    plt.figure(figsize=(10,6))
    for country in df['location'].unique():
        subset = df[df['location'] == country]
        if 'people_fully_vaccinated_per_hundred' in subset.columns:
            plt.plot(subset['date'], subset['people_fully_vaccinated_per_hundred'], label=country)
    plt.title("Vaccination Progress (Fully Vaccinated % of Population)")
    plt.xlabel("Date")
    plt.ylabel("% Fully Vaccinated")
    plt.legend()
    plt.show()

def top_countries_by_cases(df, top_n=10):
    latest_date = df['date'].max()
    latest_df = df[df['date'] == latest_date]
    top_countries = latest_df.sort_values('total_cases', ascending=False).head(top_n)
    plt.figure(figsize=(10,6))
    plt.bar(top_countries['location'], top_countries['total_cases'])
    plt.title(f"Top {top_n} Countries by Total Cases (as of {latest_date.date()})")
    plt.xticks(rotation=45)
    plt.ylabel("Total Cases")
    plt.show()

def main():
    print("Loading data...")
    df = load_data(DATA_FILE)
    print("Cleaning data...")
    df = clean_data(df, COUNTRIES)
    print("Running exploratory analysis...")
    exploratory_analysis(df)
    
    print("Generating plots...")
    plot_cases_over_time(df)
    plot_deaths_over_time(df)
    plot_vaccinations(df)
    top_countries_by_cases(df)

    print("\nAnalysis complete. Add your narrative insights here.")

if __name__ == "__main__":
    main()
