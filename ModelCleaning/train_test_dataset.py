import os
from pandas import read_csv
from joblib import dump
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Define the path to the cleaned data CSV file
csv_file_path = 'cleaned_icecreamdata.csv'

# Check if the file exists (for debugging)
if os.path.exists(csv_file_path):
    print(f"File found: {os.path.abspath(csv_file_path)}")
else:
    print(f"File not found at: {os.path.abspath(csv_file_path)}")
    # List files in current directory for debugging
    print("Files in current directory:")
    for file in os.listdir('.'):
        print(f"  {file}")

# Read the cleaned data CSV file
df = read_csv(csv_file_path)

# Proceed with your training logic
print(df.head()) 

X= df["Temperature"].values.reshape(-1,1)
y= df["Ice Cream Profits"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

mind = LinearRegression()
mind.fit(X_train,  y_train)

dump(mind, "TemperatureProfitsModel.pkl")

print("Model training completed successfully!")
print(f"Model saved to: {os.path.abspath('TemperatureProfitsModel.pkl')}")