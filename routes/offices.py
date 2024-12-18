from flask import Blueprint, render_template
from datetime import datetime
from collections import namedtuple
from models import db, ParliamentMember, Index, IndexData, Office, MinisterHistory
import random
import json

offices_bp = Blueprint('offices', __name__)


Cell = namedtuple("cell", ["cell_type", "size", "alert", "name","info","source","icon","chart_type","labels","values"]) # SET the Cell coloumns 
Minister_term = namedtuple("Minister_term", ["name", "start_date", "image", "party"])  

# Helper to create KPI and policy cells
def create_cells(indexes_info, structure):
    kpi_indexes = [info for info in indexes_info if info['is_kpi']]
    policy_indexes = [info for info in indexes_info if not info['is_kpi']]
    
    cells = []
    kpi_idx, policy_idx = 0, 0
    for row_structure in structure:
        row = []
        for cell_type in row_structure:
            if cell_type == "kpi" and kpi_idx < len(kpi_indexes):
                row.append(create_cell(cell_type, kpi_indexes[kpi_idx]))
                kpi_idx += 1
            elif cell_type == "policy" and policy_idx < len(policy_indexes):
                row.append(create_cell(cell_type, policy_indexes[policy_idx]))
                policy_idx += 1
            else:
                row.append(create_cell(cell_type))
        cells.append(row)
    return cells

# Fetch indexes and data for a specific office
def fetch_indexes(office_id):
    indexes = db.session.query(Index).filter_by(office_id=office_id).order_by(Index.is_kpi.desc()).all()
    indexes_info = []
    for index in indexes:
        index_data = db.session.query(IndexData).filter_by(index_id=index.id).all()
        labels = parse_dates([row.label for row in index_data])  # Convert dates once
        values = [float(str(row.value).replace(',', '').replace('%', '')) for row in index_data]

        indexes_info.append({
            'name': index.name,
            'info': index.info,
            'source': index.source,
            'icon': index.icon,
            'is_kpi': index.is_kpi,
            'alert': index.alert,
            'chart_type': index.chart_type,
            'labels': json.dumps(labels),
            'values': values
        })
    return indexes_info

# Helper function to create a Cell with index values or default values
def create_cell(cell_type, info=None):
    default_data = { # default cell data for empty cells
        'alert': False,
        'name': '',
        'info': 'info',
        'source': '',
        'icon': '',
        'chart_type': 'line',
        'labels': [],
        'values': ""
    }
    
    # insert data if info exists
    data = info if info else default_data 
    # get random size for the cells based of their type
    size = (
        random.choice(['large', 'medium']) if cell_type == "kpi" 
        else random.choice(['medium', 'small']) if cell_type == "policy" 
        else 'small'
    )
    # set the icon to "" if index doesn't have icon in db
    icon = ("" if data['icon'] == None
    else data['icon'])
    
    values = ("" if data['values'] == None
        else data['values'])
    
    return Cell(
        cell_type=cell_type,
        size=size,
        alert=data['alert'],
        name=data['name'],
        info=data['info'],
        source=data['source'],
        icon=icon,
        chart_type=data['chart_type'],
        labels=data['labels'],
        values=values
    )

# setting the labels dates to json for the graphs
def parse_dates(labels):
    
    # Parse dates based on format
    parsed_labels = []
    for date in labels:
        parsed_labels.append(parse_date(date))

    # Filter out None values if any parsing failed
    parsed_labels = [date for date in parsed_labels if date is not None]
    return parsed_labels
    
def parse_date(date):
    try:
        # Try to parse as "DD.MM.YYYY"
        parsed_date = datetime.strptime(date, "%d.%m.%Y").strftime("%Y-%m")
    except ValueError:
        try:
            # If it fails, try to parse as "YYYY"
            parsed_date = datetime.strptime(date, "%Y").strftime("%Y")
        except ValueError:
            # Handle any other unexpected format here if needed
            parsed_date = None
    return parsed_date

# Create list of ministers_history for specific office
def ministers_history_timeline(ministers_list):
    terms_list = []
    
    for minister in ministers_list:
        term = Minister_term(name=minister.name,
                      start_date=parse_date(minister.start_date),
                      image=minister.image,
                      party=minister.party)
        terms_list.append(term)
    
    # Convert namedtuples to dictionaries
    dict_data = [t._asdict() for t in terms_list]

    # Convert to JSON and pass to the template
    json_data = json.dumps(dict_data)  
    return json_data

@offices_bp.route('/offices')
def offices():
    all_offices = db.session.query(Office).limit(4).all()

    # Fetch index info for each office
    first_office_indexes_info = fetch_indexes(1)
    second_office_indexes_info = fetch_indexes(2)
    third_office_indexes_info = fetch_indexes(3)
    forth_office_indexes_info = fetch_indexes(4)
    
    # Cell structures
    upper_left_structure = [
        ["space", "kpi", "kpi", "space"],
        ["kpi", "kpi", "kpi", "policy"],
        ["kpi", "kpi", "policy", "policy"],
        ["space", "policy", "policy", "main_bubble"]
    ]
    upper_right_structure = [
        ["space", "kpi", "kpi", "space"],
        ["policy", "kpi", "kpi", "kpi"],
        ["policy", "policy", "kpi", "kpi"],
        ["main_bubble", "policy", "policy", "space"]
    ]
    bottom_left_structure = [
        ["space", "policy", "policy", "main_bubble"],
        ["kpi", "kpi", "policy", "policy"],
        ["kpi", "kpi", "kpi", "policy"],
        ["space", "kpi", "kpi", "space"]
    ]
    bottom_right_structure = [
        ["main_bubble", "policy", "policy", "space"],
        ["policy", "policy", "kpi", "kpi"],
        ["policy", "kpi", "kpi", "kpi"],
        ["space", "kpi", "kpi", "space"]
    ]
    
    # Create the office's cells
    first_office_cells = create_cells(first_office_indexes_info, upper_left_structure)
    second_office_cells = create_cells(second_office_indexes_info, upper_right_structure)
    third_office_cells = create_cells(third_office_indexes_info, bottom_left_structure)
    forth_office_cells = create_cells(forth_office_indexes_info, bottom_right_structure)
   
   # save the first 4 offices from the database and their ministers data in a list
    offices_list = []
    for office in all_offices:
        minister = db.session.query(ParliamentMember).filter_by(id=office.minister_id).first() 
        
        ministers_history = db.session.query(MinisterHistory).filter_by(office_id=office.id).all() 
        term_history = ministers_history_timeline(ministers_history)
        
        office_data = {
            'name':office.name,
            'info': office.info,
            'minister_name': minister.name,
            'minister_image': minister.image,  
            'minister_party': minister.party,
            'minister_role': minister.additional_role,
            'ministers_history' : term_history,
        }
        offices_list.append(office_data)

    
    # send the page offices and indexes data
    return render_template('offices-screen/offices.html',  offices=offices_list,first_office_cells=first_office_cells, second_office_cells=second_office_cells, third_office_cells=third_office_cells, forth_office_cells=forth_office_cells)
