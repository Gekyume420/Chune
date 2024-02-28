import csv

# Define the data you want to write to the CSV file
data = [
    ["Month", "Revenue", "Expenses"],
    ["January", 10000, 8000],
    ["February", 15000, 9000],
    ["March", 12000, 7000]
]

# Specify the full path for the new CSV file
filename = r'C:\Users\16198\Documents\PYTHON\end_of_month_report.csv'

# Open the file in write mode ('w') and create a csv.writer object
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)

    # Write the data to the CSV file
    writer.writerows(data)

print(f"CSV file 'end_of_month_report.csv' has been created at {filename}")