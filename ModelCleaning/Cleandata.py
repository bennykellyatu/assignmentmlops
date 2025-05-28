import os
import pandas as pd

# Load CSV file
df = pd.read_csv('ice-cream-temp.csv')

# Show original data
print("Original Data:")
print(df.head())

# Strip whitespace from column names
df.columns = df.columns.str.strip()

# Remove leading/trailing whitespace from string values
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

# Convert string columns to lowercase
df = df.map(lambda x: x.lower() if isinstance(x, str) else x)

# Convert values to numeric 
df = df.map(lambda x: pd.to_numeric(x, errors='coerce') if not pd.isna(x) else x) 

# Drop rows with any missing values
df.dropna(inplace=True)

# Drop duplicate rows
df.drop_duplicates(inplace=True)

# Save cleaned data to current directory (ModelCleaning)
output_path = 'cleaned_icecreamdata.csv'
df.to_csv(output_path, index=False)

print(f"Cleaned data saved to: {os.path.abspath(output_path)}")
print("Cleaned Data:")
print(df.head())