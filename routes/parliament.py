from flask import Blueprint, render_template
from models import db, ParliamentMember
from collections import namedtuple
from sqlalchemy import func

parliament_bp = Blueprint('parliament', __name__)

Knesset_member = namedtuple("Knesset_member", ["name", "additional_role", "party", "is_coalition", "image"])  

# set a knesset_member namedtuple to each seat in strutcture
def create_parlament(knesset_members, structure):
    seats = []

    i = 0
    for row_structure in structure:
        row = []
        for cell_type in row_structure:
            if cell_type == "seat":
                try:
                    row.append(knesset_members[i])
                    i += 1
                except:
                    row.append({'name':''})
                    print('ERROR')
            else:
                row.append("space")
        seats.append(row)
    
    return seats

def divide_array(arr):
    n = len(arr)
    
    # Ensure the array length matches the required distribution
    if n != 120:
        raise ValueError("This function is designed to split arrays of length 120.")
    
    # Manually define the section sizes
    sizes = [41, 38, 41]
    
    # Calculate indices for slicing
    start1 = 0
    start2 = sizes[0]  # 41
    start3 = sizes[0] + sizes[1]  # 41 + 39 = 80
    
    # Split the array
    part1 = arr[start1:start2]
    part2 = arr[start2:start3]
    part3 = arr[start3:]
    
    return part1, part2, part3
    
@parliament_bp.route('/parlament')
def parlament():
    # get all knesset members from the DB ordered by coalition and party
    km_info = (
        db.session.query(ParliamentMember)
        .filter(ParliamentMember.is_km == True)  # Filter to include only where is_km is True
        .order_by(ParliamentMember.is_coalition.desc(), ParliamentMember.party)
        .all()
    )

    # create arra of dicts for the knesset members info
    knesset_members = []
    for member in km_info:
        data = {
            'name': member.name,
            'additional_role': member.additional_role,
            'party':member.party,
            'is_coalition':member.is_coalition,
            'image':member.image
        }
        knesset_members.append(data)

    first_section, second_section, third_section = divide_array(knesset_members)
    
    # Query to get the count of members in each party
    party_counts = db.session.query(
        ParliamentMember.party,
        func.count(ParliamentMember.id)  # Assuming 'id' is the primary key of each member
    ).filter(ParliamentMember.is_km == True).group_by(ParliamentMember.party).order_by(ParliamentMember.is_coalition.desc()).all()

    party_dict = {}

    for party, count in party_counts:
        party_dict[party] = count
    

    
    # set the parlament structure
    parlament_structure = [
        ["space", "space", "space", "seat", "seat", "seat", "seat", "seat", "seat", "seat", "seat", "seat", "seat", "seat", "seat", "seat", "space", "space", "space"],
        ["seat", "space", "space", "space", "seat", "seat", "seat", "seat", "seat", "seat", "seat", "seat", "seat", "seat", "seat", "space", "space", "space", "seat"],
        ["seat", "seat", "space", "space", "space", "seat", "seat", "seat", "seat", "seat", "seat", "seat", "seat", "seat", "space", "space", "space", "seat", "seat"],
        ["seat", "seat", "seat", "space", "space", "space", "seat", "seat", "seat", "seat", "seat", "seat", "seat", "space", "space", "space", "seat", "seat", "seat"],
        ["seat", "seat", "seat", "seat", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "seat", "seat", "seat", "seat"],
        ["seat", "seat", "seat", "seat", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "seat", "seat", "seat", "seat"],
        ["seat", "seat", "seat", "seat", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "seat", "seat", "seat", "seat"],
        ["seat", "seat", "seat", "seat", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "seat", "seat", "seat", "seat"],
        ["seat", "seat", "seat", "seat", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "seat", "seat", "seat", "seat"],
        ["seat", "seat", "seat", "seat", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "seat", "seat", "seat", "seat"],
        ["seat", "seat", "seat", "seat", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "seat", "seat", "seat", "seat"],
        ["seat", "seat", "seat", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "seat", "seat", "seat"],
        ["seat", "seat", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "seat", "seat"],
        ["seat", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "space", "seat"],
    ]

    # Split the parliament structure into left, center, and right sections
    left_section = []
    center_section = []
    right_section = []
    for row in parlament_structure:
        # Using slicing to divide each row into left, center, and right parts
        left_section.append(row[:4])     # First 4 columns
        center_section.append(row[4:15]) # Columns 4 to 15 (center)
        right_section.append(row[15:])   # Last 4 columns
        
    # set a knesset member namedtuple to each seat in structure 
    left_seats = create_parlament(list(reversed(first_section)),left_section)
    center_seats = create_parlament(second_section,center_section)
    right_seats = create_parlament(third_section,right_section)
    
    i=0
    for row in right_seats:
        for seat in row:
            if seat != 'space':
                #print(str(i) + seat['name'])
                i += 1
    return render_template('parliament.html', party_dict = party_dict, left_section = left_seats, center_section = center_seats, right_section= right_seats )