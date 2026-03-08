import pandas as pd
import requests
from io import StringIO
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()

def extract_btc_data(url):
    try:
        # Fetching CSV data directly from the URL
        response = requests.get(url, timeout=10)
        response.raise_for_status() 
        
        # Load into a DataFrame
        data = pd.read_csv(StringIO(response.text))
        print("Extraction Successful")
        return data
    except Exception as e:
        print(f"Error during extraction: {e}")
        return None

# URL from technical specifications
BTC_URL = "https://raw.githubusercontent.com/coinmetrics/data/master/csv/btc.csv"
raw_df = extract_btc_data(BTC_URL)


def transform_btc_data(df):
    try:
        # Selection: Only keep what is available
        columns_to_keep = ['time', 'PriceUSD', 'ROI30d']
        df = df[columns_to_keep].copy()
        
        # Data Cleaning: Convert time to SQL-friendly Timestamp
        df['time'] = pd.to_datetime(df['time'])
        
        # Handle missing values in PriceUSD
        df = df.dropna(subset=['PriceUSD'])
        
        # Feature Engineering: Market_Status 
        # Using ROI30d as the threshold since VtyDayRet30d is missing
        df['market_status'] = df['ROI30d'].apply(
            lambda x: 'High Volatility' if abs(x) > 0.05 else 'Stable'
        )
        
        # Add a placeholder for realized_cap since it's missing from source
        df['realized_cap'] = 0.0
        
        # Rename to match Database Schema [cite: 25, 26, 27, 28, 29]
        df = df.rename(columns={
            'PriceUSD': 'price_usd',
            'ROI30d': 'volatility_30d'
        })
        
        # Reorder to match schema exactly
        df = df[['time', 'price_usd', 'volatility_30d', 'realized_cap', 'market_status']]
        
        print("Transformation Successful with adapted columns.")
        return df
        
    except KeyError as e:
        print(f"Critical Mapping Error: {e}")
        return None

transformed_df = transform_btc_data(raw_df)



# Update these with your local Postgres credentials
DATABASE_URL = "postgresql://postgres:password@localhost:5432/crypto_db"


# 3. SAFETY CHECK: This prevents the 'None' error by giving you a clear message
if DATABASE_URL is None:
    print("❌ ERROR: DATABASE_URL is not found. Check if your .env file is in the same folder as this script.")
else:
    try:
        # 4. Create the engine
        engine = create_engine(DATABASE_URL)
        print("✅ Connection string loaded successfully!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")


def load_to_postgres(df, connection_string):
    if df is None:
        print("No data available to load.")
        return
        
    try:
        engine = create_engine(connection_string)
        
        # Step 3 logic: Create table automatically and handle duplicates [cite: 22, 23]
        # Using 'append' adds new data; the Schema (Primary Key) handles the logic 
        df.to_sql('btc_metrics', engine, if_exists='append', index=False)
        
        print("Successfully loaded data into 'btc_metrics' table!")
    except Exception as e:
        print(f"Database Error: {e}")

# Run the load
load_to_postgres(transformed_df, DATABASE_URL)