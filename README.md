
# Bitcoin Crypto-Database Pipeline

## Project Overview

This project is an automated **ETL (Extract, Transform, Load)** data pipeline designed to transition data from simple file storage into a managed **PostgreSQL** Relational Database system. The pipeline extracts live Bitcoin network data, transforms it for analysis, and loads it into a database via DBeaver/PostgreSQL while maintaining strict data integrity.

## Technical Features

* **Automated Extraction:** Fetches live BTC data directly from a remote CSV source.
* **Resiliency:** Includes robust error handling (`try/except` blocks) to manage network interruptions and database connection issues.
* **Database Integration:** Seamlessly maps transformed data into a relational schema.


## Data Transformation

The transformation phase focuses on distilling raw data into actionable insights. The pipeline processes the following core metrics:

* **Standardization:** Timestamps are converted to a uniform format.
* **Data Cleaning:** Handles missing price data to ensure continuity.
* **Metric Extraction:** Isolates Time, Price, Volatility, and Realized Cap.
* **Categorization Logic:** Applies a volatility threshold to categorize market status:
* **Stable:** Volatility $\le 0.05$
* **High Volatility:** Volatility $> 0.05$

