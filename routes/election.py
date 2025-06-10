from flask import Blueprint, render_template
from models import db, Poll, PollResult
from sqlalchemy import func
from datetime import datetime, timedelta
import math
import json
import os

election_bp = Blueprint('election', __name__)

@election_bp.route('/election')
def election():
    # Get the last 5 polls
    latest_polls = Poll.query.order_by(Poll.date.desc()).limit(5).all()
    
    # Get all unique party names from the last 5 polls
    party_names = db.session.query(PollResult.party_name)\
        .join(Poll)\
        .filter(Poll.id.in_([poll.id for poll in latest_polls]))\
        .distinct()\
        .all()
    party_names = [party[0] for party in party_names]
    
    # Calculate average seats for each party
    party_averages = {}
    for party in party_names:
        avg_seats = db.session.query(func.avg(PollResult.seats))\
            .join(Poll)\
            .filter(Poll.id.in_([poll.id for poll in latest_polls]))\
            .filter(PollResult.party_name == party)\
            .scalar()
        party_averages[party] = round(avg_seats, 1) if avg_seats else 0
    
    # Calculate total of all averages
    total_seats = sum(party_averages.values())
    
    # Calculate scaling factor to make total 120
    scaling_factor = 120 / total_seats if total_seats > 0 else 0
    
    # Apply scaling factor and calculate decimal seats
    decimal_seats = {
        party: seats * scaling_factor
        for party, seats in party_averages.items()
    }
    
    # Calculate integer seats and remainders
    integer_seats = {party: math.floor(seats) for party, seats in decimal_seats.items()}
    remainders = {
        party: seats - math.floor(seats)
        for party, seats in decimal_seats.items()
    }
    
    # Calculate how many seats we need to distribute
    total_integer_seats = sum(integer_seats.values())
    seats_to_distribute = 120 - total_integer_seats
    
    # Sort parties by remainder and distribute remaining seats
    sorted_remainders = sorted(remainders.items(), key=lambda x: x[1], reverse=True)
    for party, _ in sorted_remainders[:seats_to_distribute]:
        integer_seats[party] += 1
    
    # Filter out parties with fewer than 4 seats
    filtered_integer_seats = {party: seats for party, seats in integer_seats.items() if seats >= 4}
    
    # If any parties were removed, recalculate scaling for the remaining parties
    if len(filtered_integer_seats) < len(integer_seats):
        filtered_total = sum(filtered_integer_seats.values())
        scaling_factor = 120 / filtered_total if filtered_total > 0 else 0
        # Recalculate decimal seats for filtered parties
        decimal_seats = {
            party: party_averages[party] * scaling_factor
            for party in filtered_integer_seats.keys()
        }
        integer_seats = {party: math.floor(seats) for party, seats in decimal_seats.items()}
        remainders = {
            party: seats - math.floor(seats)
            for party, seats in decimal_seats.items()
        }
        total_integer_seats = sum(integer_seats.values())
        seats_to_distribute = 120 - total_integer_seats
        sorted_remainders = sorted(remainders.items(), key=lambda x: x[1], reverse=True)
        for party, _ in sorted_remainders[:seats_to_distribute]:
            integer_seats[party] += 1
        # Final filter (shouldn't be needed, but for safety)
        filtered_integer_seats = {party: seats for party, seats in integer_seats.items() if seats >= 4}
    
    # Sort parties by final seat count
    sorted_parties = sorted(filtered_integer_seats.items(), key=lambda x: x[1], reverse=True)

    # Prepare lists for chart
    party_labels = [party for party, seats in sorted_parties]
    party_seats = [seats for party, seats in sorted_parties]

    # Load party blocks JSON
    blocks_path = os.path.join(os.path.dirname(__file__), '../static/json/party_blocks.json')
    with open(blocks_path, encoding='utf-8') as f:
        party_blocks = json.load(f)

    # Map each party to its block color
    party_to_color = {}
    for block in party_blocks.values():
        color = block.get('color', '#1e88e5')
        for party in block['parties']:
            party_to_color[normalize_party_name(party)] = color
    # Create a list of colors for the chart, matching the order of party_labels
    party_colors = [party_to_color.get(normalize_party_name(party), '#1e88e5') for party in party_labels]

    return render_template('election_screen.html', 
                         polls=latest_polls,
                         party_averages=sorted_parties,
                         party_labels=party_labels,
                         party_seats=party_seats,
                         party_colors=party_colors)

def normalize_party_name(name):
    return name.replace('"', '').replace("'", '').replace('-', '').replace('״', '').replace('׳', '').replace(' ', '') 