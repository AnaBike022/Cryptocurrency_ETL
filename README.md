# Bitcoin Crypto-Database Pipeline 

# Project Overview

This project is an automated ETL (Extract, Transform, Load) data pipeline that transitions from simple file storage to a managed PostgreSQL Relational Database system. The pipeline extracts live Bitcoin network data, transforms it for analysis, and loads it into a database (thus DBeaver/PostgreSQL) while ensuring data integrity.

# Technical Features

Automated Extraction: It fetches live BTC data directly from a remote CSV source and includes error handling (try/except) for network and database operations.

# Data Transformation
The transformation phase of the pipeline extracts the core metrics—time, price, volatility, and realized cap—while standardizing timestamps, cleaning missing price data, and applying logic to categorize market status as "Stable" or "High Volatility" based on a 0.05 threshold.