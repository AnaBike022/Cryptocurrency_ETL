import pandas as pd 
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


load_dotenv()


def extract_data(file_path):
    data = pd.read_csv(file_path)
    return data

def transform_data(data):
    data['time'] = pd.to_datetime(data['time'])
    
    return data

def load_data(data):
   user = os.getenv("user")
   password = os.getenv("password")
   host = os.getenv("host")
   port = int(os.getenv("port", 5432))
   database = os.getenv("database")
   table_name = os.getenv("table")
   schema = os.getenv("schema")
   
   engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')
   data.to_sql(table_name, engine, schema=schema, if_exists='append', index=False)
    

if __name__ == "__main__":
    
    file_path = "https://raw.githubusercontent.com/coinmetrics/data/master/csv/btc.csv"
    data = extract_data(file_path)
    head = data.head(5)
    print(head)
    col = data.columns
    print(col)
    
    transformed_data = transform_data(data)
    load_data(transformed_data)