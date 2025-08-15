from flask import Blueprint, render_template
from models import db, ParliamentMember, NonParliamentMember
from collections import namedtuple
from sqlalchemy import func
from sqlalchemy import or_, not_


parliament_bp = Blueprint('parliament', __name__)


# set a knesset_member namedtuple to each seat in strutcture
def create_parlament(knesset_members, structure):
    # Knesset data
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
# devide the knesset memebers array into 3 sections for the structure
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
    # Knesset Data
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
    
    # final array for the front end
    knesset = [(left_seats, 'left'), (center_seats, 'center'), (right_seats, 'right')]

    # Government Data

    # get all government members data
    gm_info = (
    db.session.query(ParliamentMember)
    .filter(
        ParliamentMember.is_coalition != "",  # Check that is_coalition is not an empty string
        not_(ParliamentMember.additional_role.contains("יושב ראש")),  # Exclude rows where additional_role contains "יושב ראש"
        ParliamentMember.additional_role != ""  # Ensure additional_role is not empty
    )
    .order_by(ParliamentMember.party)
    .all()
    )

    # create array of dicts for the government members info
    government_members = []
    for member in gm_info:
        data = {
            'name': member.name,
            'additional_role': member.additional_role,
            'party':member.party,
            'image':member.image
        }
        government_members.append(data)

    government_sturcture = [
        ["space","space","space", "space","space", "space","space","space","space", "space"],
        ["space","seat","seat", "seat","seat", "seat","seat","seat","seat", "space"],
        ["seat","seat","seat", "seat","seat", "seat","seat","seat","seat", "seat"],
        ["seat","seat","space", "space","space", "space","space","space","seat", "seat"],
        ["seat","seat","space", "space","space", "space","space","space","seat", "seat"],
        ["seat","space","space", "space","space", "space","space","space","space", "space"],
        ["space","space","space", "space","space", "space","space","space","space", "space"],
        ["space","space","space", "space","space", "space","space","space","space", "space"],
        ["space","space","space", "space","space", "space","space","space","space", "space"],
        ["space","space","space", "space","space", "space","space","space","space", "space"],
        ["space","space","space", "space","space", "space","space","space","space", "space"],
    ]
    
    government_seats = create_parlament(government_members, government_sturcture)


    # Query to get the count of members in each party
    party_counts_government = (
    db.session.query(
        ParliamentMember.party,
        func.count(ParliamentMember.id).label("member_count")  # Alias for better readability
    )
    .filter(
        ParliamentMember.is_coalition.isnot(None),  # Ensure is_coalition is not NULL
        ParliamentMember.is_coalition != "",        # Ensure is_coalition is not an empty string
        ~ParliamentMember.additional_role.contains("יושב ראש"),  # Exclude rows with "יושב ראש" in additional_role
        ParliamentMember.additional_role.isnot(None),  # Ensure additional_role is not NULL
        ParliamentMember.additional_role != ""        # Ensure additional_role is not an empty string
    )
    .group_by(ParliamentMember.party)  # Group by party
    .order_by(ParliamentMember.party)  # Order by party
    .all()
)


    count_by_party_government = {}

    for party, count in party_counts_government:
        count_by_party_government[party] = count


    # Supreme Court Data

    # get all Supreme Court members data
    sc_info = (
    db.session.query(NonParliamentMember)
    .filter(
        NonParliamentMember.role.ilike("%בית המשפט העליון%")  # Case-insensitive match
    )
    .all()
    )

    # create array of dicts for the government members info
    supreme_court_members = []
    for member in sc_info:
        data = {
            'name': member.name,
            'role': member.role,
            'start_date': member.start_date,
            'finish_date': member.finish_date,
            'image':member.image,
            'appointed_by':member.appointed_by
        }
        supreme_court_members.append(data)

    supreme_court_sturcture = [
        ["space","space","space", "space","space", "space","space","space","space", "space","space","space"],
        ["space","space","space", "seat","seat", "seat","seat","seat","seat", "space","space","space"],
        ["space","space","seat", "space","space", "space","space","space","space", "seat","space","space"],
        ["space","seat","space", "space","space", "space","space","space","space", "space","seat","space"],
        ["seat","space","space", "space","space", "space","space","space","space", "space","space","seat"],
        ["space","space","space", "space","space", "space","space","space","space", "space","space","space"],
        ["space","space","space", "space","space", "space","space","space","space", "space","space","space"],
        ["space","space","space", "space","space", "space","space","space","space", "space","space","space"],
        ["space","space","space", "space","space", "space","space","space","space", "space","space","space" ],
        ["space","space","space", "space","space", "space","space","space","space", "space","space","space"],
        ["space","space","space", "space","space", "space","space","space","space", "space","space","space"],
        ["space","space","space", "space","space", "space","space","space","space", "space","space","space"],
        ["space","space","space", "space","space", "space","space","space","space", "space","space","space"],
        ["space","space","space", "space","space", "space","space","space","space", "space","space","space"],
        ["space","space","space", "space","space", "space","space","space","space", "space","space","space"],
        ["space","space","space", "space","space", "space","space","space","space", "space","space","space"],
        ["space","space","space", "space","space", "space","space","space","space", "space","space","space"],
        ["space","space","space", "space","space", "space","space","space","space", "space","space","space"],
        ["space","space","space", "space","space", "space","space","space","space", "space","space","space"],
        ["space","space","space", "space","space", "space","space","space","space", "space","space","space"],
        ["space","space","space", "space","space", "space","space","space","space", "space","space","space"],
       
     

    ]
    
    supreme_Court_seats = create_parlament(supreme_court_members, supreme_court_sturcture)

    
    return render_template('parliament.html', party_dict = party_dict, government_parties = count_by_party_government, parliament = knesset, government = government_seats, supreme_court = supreme_Court_seats)