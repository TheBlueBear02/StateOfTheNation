from flask import Blueprint, render_template
from datetime import datetime
from pyluach import dates
from models import db, KnessetMembers, Tweets, Offices, Indexes, Indexes_Data  # Import models
from collections import namedtuple
import json
import random

# Create a Blueprint for the routes
routes = Blueprint('routes', __name__)


def get_date(): # return today's date
    return datetime.today().strftime('%d.%m.%Y')
def get_hebrew_date(): # return hebrew date
    today = dates.HebrewDate.today()
    return today.hebrew_date_string()



@routes.route('/')
def index():
    # Query the database for all tweets and kms
    all_tweets = db.session.query(Tweets).all()
    all_kms = db.session.query(KnessetMembers).all()
    
    # create list of dicts that contains the feed's tweets
    name = ""
    party = ""
    is_coalition = False
    image = ""
    additional_role = ""
    tweets = []
    for tweet in all_tweets:
        for member in all_kms:
            if member.km_id == tweet.km_id:
                name = member.name
                party = member.party
                is_coalition = member.is_coalition
                image = member.image
                additional_role = member.additional_role
                break
        tweet_data = {
            'id':tweet.id,
            'text': tweet.text,
            'date': tweet.date,
            'time': tweet.time,
            'topic': tweet.topic,  
            'name': name,
            'party': party,
            'is_coalition': is_coalition,
            'minister_image': image,
            'additional_role': additional_role,
            'image': tweet.image
        }
        tweets.append(tweet_data)
    return render_template('index.html', today_date=get_date(), hebrew_date=get_hebrew_date(), tweets=list(reversed(tweets)))

Cell = namedtuple("cell", ["cell_type", "size", "alert", "name","info","icon","chart_type","labels","values"]) # SET the Cell coloumns 

# Helper function to create a Cell with default values
def create_cell(cell_type, info=None):
    default_data = {
        'alert': False,
        'name': 'name',
        'info': 'info',
        'icon': '',
        'chart_type': 'line',
        'labels': [],
        'values': []
    }
    
    data = info if info else default_data
    size = (
        random.choice(['large', 'medium']) if cell_type == "kpi" 
        else random.choice(['medium', 'small']) if cell_type == "policy" 
        else 'small'
    )
    print(data['icon'])
    return Cell(
        cell_type=cell_type,
        size=size,
        alert=data['alert'],
        name=data['name'],
        info=data['info'],
        icon=data['icon'],
        chart_type=data['chart_type'],
        labels=data['labels'],
        values=data['values']
    )

# setting the labels dates to json for the graphs
def parse_dates(labels):
    # Parse dates based on format
    parsed_labels = []
    for date in labels:
        try:
            # Try to parse as "DD.MM.YYYY"
            parsed_date = datetime.strptime(date, "%d.%m.%Y").strftime("%Y-%m-%d")
        except ValueError:
            try:
                # If it fails, try to parse as "YYYY"
                parsed_date = datetime.strptime(date, "%Y").strftime("%Y")
            except ValueError:
                # Handle any other unexpected format here if needed
                parsed_date = None
        parsed_labels.append(parsed_date)

    # Filter out None values if any parsing failed
    parsed_labels = [date for date in parsed_labels if date is not None]
    result = json.dumps(parsed_labels)  # Convert list to JSON string


    return result

@routes.route('/offices')
def offices():
    all_offices = db.session.query(Offices).all()
    all_kms = db.session.query(KnessetMembers).all()
    # save the first 4 offices from the database and their ministers data in a list
    offices_list = []
    number_of_offices = 4
    i=0

    first_office_indexes = db.session.query(Indexes).filter_by(office_id='3').order_by(Indexes.is_kpi.desc()).all()
    second_office_indexes = db.session.query(Indexes).filter_by(office_id='2').all()
    third_office_indexes = db.session.query(Indexes).filter_by(office_id='3').all()
    forth_office_indexes = db.session.query(Indexes).filter_by(office_id='4').all()

    first_office_indexes_info = []
    for index in first_office_indexes:
        index_data = db.session.query(Indexes_Data).filter_by(index_id=index.id).all()
        
        labels = []
        values = []
        for row in index_data:
            labels.append(row.label)
            values.append(row.value)
        
        # Convert each date to "YYYY-MM-DD" format
        labels = parse_dates(labels)
        
        index_info = {
            'name':index.name,
            'info':index.info,
            'icon':index.icon,
            'is_kpi':index.is_kpi,
            'alert':index.alert,
            'chart_type':index.chart_type,
            'labels': labels,
            'values': values
        }
        first_office_indexes_info.append(index_info)

    # Separate KPI and policy indexes from first_office_indexes_info
    kpi_indexes = [info for info in first_office_indexes_info if info['is_kpi']]
    policy_indexes = [info for info in first_office_indexes_info if not info['is_kpi']]

    # Create the cells list with assigned KPI and policy information
    second_office_cells = []
    kpi_idx, policy_idx = 0, 0

    # Define row structures and fill cells
    for row_structure in [
        ["space", "kpi", "kpi", "space"],
        ["policy", "kpi", "kpi", "kpi"],
        ["policy", "policy", "kpi", "kpi"],
        ["main_bubble", "policy", "policy", "space"]
    ]:
        row = []
        for cell_type in row_structure:
            if cell_type == "kpi" and kpi_idx < len(kpi_indexes):
                # Create a KPI cell with specific info
                row.append(create_cell(cell_type, kpi_indexes[kpi_idx]))
                kpi_idx += 1
            elif cell_type == "policy" and policy_idx < len(policy_indexes):
                # Create a policy cell with specific info
                row.append(create_cell(cell_type, policy_indexes[policy_idx]))
                policy_idx += 1
            else:
                # Create a default or placeholder cell
                row.append(create_cell(cell_type))
        
        second_office_cells.append(row)

    # 4 office's data
    for office in all_offices:
        if i == number_of_offices:
            break
        minister = db.session.query(KnessetMembers).filter_by(km_id=office.minister_id).first()
            
        office_data = {
            'name':office.name,
            'info': office.info,
            'minister_name': minister.name,
            'minister_image': minister.image,  
            'minister_party': minister.party,
            'minister_role': minister.additional_role,
        }
        offices_list.append(office_data)
        i += 1

    
    return render_template('offices.html', offices=offices_list, first_office_indexes=first_office_indexes_info, second_office_cells=second_office_cells)

@routes.route('/demography')
def demography():
    graphs_data = {}
    # population size
    size_data = db.session.query(Indexes_Data).filter_by(index_id=12).all()

    size_labels = []
    size_values = []
    for row in size_data:
        size_labels.append(row.label)
        size_values.append(row.value)
    size_values = [int(str(val).replace(",", "")) for val in size_values]

    # religion chart
    religion_data = db.session.query(Indexes_Data).filter_by(index_id=13).all()
    religion_labels = []
    religion_values = []
    for row in religion_data:
        religion_labels.append(row.label)
        religion_values.append(row.value)
    religion_values = [int(str(val).replace(",", "")) for val in religion_values]

    return render_template('demography.html', size_labels=size_labels, size_values=size_values, religion_labels=religion_labels, religion_values=religion_values)


@routes.route('/economy')
def economy():
   
    # Main Graph data
    main_labels = []
    main_values = []
    temp_values = []
    
    debt_per_year = db.session.query(Indexes_Data).filter_by(index_id=5).all()
    income_per_year = db.session.query(Indexes_Data).filter_by(index_id=6).all()
    expenses_per_year = db.session.query(Indexes_Data).filter_by(index_id=7).all()
    interest_per_year = db.session.query(Indexes_Data).filter_by(index_id=8).all()
    gdp_per_year = db.session.query(Indexes_Data).filter_by(index_id=9).all()

    indexes = []
    indexes.append(debt_per_year)
    indexes.append(income_per_year)
    indexes.append(expenses_per_year)
    indexes.append(interest_per_year)
    indexes.append(gdp_per_year)


    for row in income_per_year:
        main_labels.append(row.label)

    for index in indexes: 
        for row in index:  
            temp_values.append(row.value)
        main_values.append(temp_values)
        temp_values = []
    

    last_year_expenses = db.session.query(Indexes_Data).filter_by(index_id=10).all()
    expenses_lables = []
    expenses_values = []
  
    for row in last_year_expenses:
        expenses_lables.append(row.label)
        expenses_values.append(row.value)
    
    last_year_income = db.session.query(Indexes_Data).filter_by(index_id=11).all()
    income_lables = []
    income_values = []

    for row in last_year_income:
        income_lables.append(row.label)
        income_values.append(row.value)

    return render_template('economy.html', main_lables=main_labels, main_values=main_values, expenses_lables=expenses_lables, expenses_values=expenses_values,income_lables=income_lables,income_values=income_values)
