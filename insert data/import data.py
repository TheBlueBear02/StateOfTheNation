import csv
import sys
sys.path.append('E:\Development Projects\SN')
from models import KnessetMembers,Tweets,Offices,Indexes,Indexes_Data
import json
from app import app, db

# add data from csv file to index_data table
def save_csv_to_db():
    with open("E:\Development Projects\SN - DATA\המשרד לביטחון לאומי\נרצחים בפיגועים (2).csv", newline='',encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        index_id = "14"
        date = ""
        value = None
        for row in csv_reader:
            # Create an instance of YourModel
            new_record = Indexes_Data(
                index_id = index_id,
                label=row['label'],  # Map CSV fields to your model's columns
                value=row['value']

            )
            # Add the record to the session if not saved yet
            db.session.add(new_record)
            
        # Commit all changes to the database
        db.session.commit()

# add knesset members from json file to the kms table
def add_km():
    # Read the JSON data
    with open(r'E:\Development Projects\SN\DB\KnessetMembers.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Iterate through each entry in the JSON and add it to the database
    for entry in data['Members']:
        new_message = KnessetMembers(
            km_id=entry['Id'],
            party=entry['party'],
            is_coalition=entry['is_coalition'],
            image=entry['image'],
            additional_role=entry['additional_role'],
            name=entry['name']
        )
        db.session.add(new_message)
    
    # Commit the changes to the database
    db.session.commit()
    return 'Data added successfully'

# add tweets from json file to the tweet's table
@app.route('/add_data', methods=['POST'])
def add_tweet():
    # Read the JSON data
    with open(r"E:\Development Projects\SN\DB\Tweets.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Iterate through each entry in the JSON and add it to the database
    for entry in data:
        new_message = Tweets(
            id=entry['Id'],
            km_id=entry['UserId'],
            text=entry['Text'],
            date=entry['Date'],
            time=entry['Time'],
            topic=entry['Topic']
        )
        db.session.add(new_message)
    
    # Commit the changes to the database
    db.session.commit()
    return 'Data added successfully'


if __name__ == "__main__":
    with app.app_context():
        # save_csv_to_db()
        save_csv_to_db()
        print("Data Saved")