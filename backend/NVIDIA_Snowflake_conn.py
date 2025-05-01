import snowflake.connector
import os
import pandas as pd

# Snowflake connection details
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_STAGE = os.getenv("SNOWFLAKE_STAGE")

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    account=SNOWFLAKE_ACCOUNT,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA
)

cursor = conn.cursor()
print("✅ Connected to Snowflake!")

# Use the correctly formatted CSV file
csv_file_path = "nvidia_pivoted_cleaned_data.csv"

# Upload CSV to Snowflake Stage
upload_query = f"PUT file://{csv_file_path} @{SNOWFLAKE_STAGE} AUTO_COMPRESS=TRUE"

try:
    cursor.execute(upload_query)
    print("✅ Fixed CSV file successfully uploaded to Snowflake stage!")
except Exception as e:
    print(f"❌ Error uploading file: {e}")

# Close the connection
cursor.close()
conn.close()
