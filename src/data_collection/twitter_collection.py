import csv

# Define the absolute path to the CSV file
csv_file = 'C:\\Users\\Chris\\Documents\\GitHub\\marketTracker\\Bitcoin_tweets_test.csv'

# Open the CSV file and read its contents using csv.reader
with open(csv_file, 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
