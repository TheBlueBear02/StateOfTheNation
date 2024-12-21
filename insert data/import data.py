import csv
import sys
#sys.path.append('E:\\Development Projects\\SN')
sys.path.append('D:\\Projects\\stateofthenation')

import json
from app import db, create_app
from models import ParliamentMember,Tweet,IndexData,Index

app = create_app()

# add data from csv file to index_data table
def save_csv_to_db():
    with open("D:\\Projects\\SN - DATA\\המשרד לביטחון לאומי - מדדים - מספר תיקים שנפתחו.csv", newline='',encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        # Query the max id and increment
        max_id = db.session.query(db.func.max(IndexData.id)).scalar()
        new_id = (max_id or 0) + 1  # Handle None case if table is empty
        index_id = "19"
        date = ""
        value = None
        for row in csv_reader:
            # Create an instance of YourModel
            new_record = IndexData(
                id=new_id,
                index_id = index_id,
                label=row['labels'],  
                value=row['values']

            )
            # Add the record to the session if not saved yet
            db.session.add(new_record)
            new_id += 1
            
        # Commit all changes to the database
        db.session.commit()

# add knesset members from json file to the kms table
def add_km():
    # Read the JSON data
    with open(r'D:\Projects\StateOfTheNation\DB\KnessetMembers.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    i=0
    # Iterate through each entry in the JSON and add it to the database
    for entry in data['Members']:
        new_message = ParliamentMember(
            id=i,
            name=entry['name'],
            party=entry['party'],
            additional_role=entry['additional_role'],
            is_coalition=entry['is_coalition'],
            is_km=True,
            image=entry['image'],
            twitter_id=entry['Id']
        )
        db.session.add(new_message)
        i += 1
    # Commit the changes to the database
    db.session.commit()
    return 'Data added successfully'


def add_index():
    # Read the JSON data
    with open(r'D:\Projects\StateOfTheNation\sn - db backup 16.11.24\indexes.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    for entry in data:
        new_index = Index(
            id=entry['id'],
            name=entry['name'],
            info=entry['info'],
            office_id=entry['office_id'],
            is_kpi=entry['is_kpi'],
            alert=False,
            icon=entry['icon'],
            chart_type=entry['chart_type']
            
           
        )
        db.session.add(new_index)
    
    # Commit the changes to the database
    db.session.commit()
    return 'Data added successfully'

# add tweets from json file to the tweet's table
@app.route('/add_data', methods=['POST'])
def add_tweet():
    # Read the JSON data
    with open(r"D:\Projects\StateOfTheNation\DB\Tweets.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Iterate through each entry in the JSON and add it to the database
    for entry in data:
        new_message = Tweet(
            id=entry['Id'],
            twitter_id=entry['UserId'],
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
        save_csv_to_db()
        #add_index()
        print("Data Saved")