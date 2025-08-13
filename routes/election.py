from flask import Blueprint, render_template
from models import db, Poll, PollResult
from sqlalchemy import func
from datetime import datetime, timedelta
import math
import json
import os

election_bp = Blueprint('election', __name__)

def normalize_party_name(name):
    return name.replace('"', '').replace("'", '').replace('-', '').replace('״', '').replace('׳', '').replace(' ', '') 

def get_poll_averages(latest_polls):
    party_names = db.session.query(PollResult.party_name)\
        .join(Poll)\
        .filter(Poll.id.in_([poll.id for poll in latest_polls]))\
        .distinct()\
        .all()
    party_names = [party[0] for party in party_names]
    party_averages = {}
    for party in party_names:
        avg_seats = db.session.query(func.avg(PollResult.seats))\
            .join(Poll)\
            .filter(Poll.id.in_([poll.id for poll in latest_polls]))\
            .filter(PollResult.party_name == party)\
            .scalar()
        party_averages[party] = round(avg_seats, 1) if avg_seats else 0
    return party_averages

def allocate_seats(party_averages):
    total_seats = sum(party_averages.values())
    scaling_factor = 120 / total_seats if total_seats > 0 else 0
    decimal_seats = {party: seats * scaling_factor for party, seats in party_averages.items()}
    integer_seats = {party: math.floor(seats) for party, seats in decimal_seats.items()}
    remainders = {party: seats - math.floor(seats) for party, seats in decimal_seats.items()}
    total_integer_seats = sum(integer_seats.values())
    seats_to_distribute = 120 - total_integer_seats
    sorted_remainders = sorted(remainders.items(), key=lambda x: x[1], reverse=True)
    for party, _ in sorted_remainders[:seats_to_distribute]:
        integer_seats[party] += 1
    filtered_integer_seats = {party: seats for party, seats in integer_seats.items() if seats >= 4}
    if len(filtered_integer_seats) < len(integer_seats):
        filtered_total = sum(filtered_integer_seats.values())
        scaling_factor = 120 / filtered_total if filtered_total > 0 else 0
        decimal_seats = {party: party_averages[party] * scaling_factor for party in filtered_integer_seats.keys()}
        integer_seats = {party: math.floor(seats) for party, seats in decimal_seats.items()}
        remainders = {party: seats - math.floor(seats) for party, seats in decimal_seats.items()}
        total_integer_seats = sum(integer_seats.values())
        seats_to_distribute = 120 - total_integer_seats
        sorted_remainders = sorted(remainders.items(), key=lambda x: x[1], reverse=True)
        for party, _ in sorted_remainders[:seats_to_distribute]:
            integer_seats[party] += 1
        filtered_integer_seats = {party: seats for party, seats in integer_seats.items() if seats >= 4}
    sorted_parties = sorted(filtered_integer_seats.items(), key=lambda x: x[1], reverse=True)
    return sorted_parties, filtered_integer_seats

def get_block_data(filtered_integer_seats, party_blocks):
    party_to_block = {}
    for block_key, block in party_blocks.items():
        for party in block['parties']:
            party_to_block[normalize_party_name(party)] = block_key
    block_totals = {block_key: 0 for block_key in party_blocks}
    for party, seats in filtered_integer_seats.items():
        block_key = party_to_block.get(normalize_party_name(party))
        if block_key:
            block_totals[block_key] += seats
    # Set the desired order of block keys
    block_order = ['opposition', 'arabs', 'coalition']
    block_labels = [party_blocks[key]['name'] for key in block_order]
    block_seats = [block_totals[key] for key in block_order]
    block_colors = [party_blocks[key]['color'] for key in block_order]
    return block_labels, block_seats, block_colors

def get_party_colors(party_blocks, party_labels):
    party_to_color = {}
    for block in party_blocks.values():
        color = block.get('color', '#1e88e5')
        for party in block['parties']:
            party_to_color[normalize_party_name(party)] = color
    party_colors = [party_to_color.get(normalize_party_name(party), '#1e88e5') for party in party_labels]
    return party_colors, party_to_color

def get_poll_history_data():
    all_polls = Poll.query.order_by(Poll.date.asc()).all()
    poll_dates = [poll.date.strftime('%d/%m/%Y') for poll in all_polls]
    # Get all unique parties from all PollResults in the DB
    all_party_names = [row[0] for row in db.session.query(PollResult.party_name).distinct().all()]
    # Use the same color logic as above
    blocks_path = os.path.join(os.path.dirname(__file__), '../static/json/party_blocks.json')
    with open(blocks_path, encoding='utf-8') as f:
        party_blocks = json.load(f)
    party_to_color = {}
    party_to_block = {}
    for block_key, block in party_blocks.items():
        color = block.get('color', '#1e88e5')
        for party in block['parties']:
            norm_name = normalize_party_name(party)
            party_to_color[norm_name] = color
            party_to_block[norm_name] = block_key

    # Group parties by block order, but include all parties
    block_order = ['coalition', 'arabs', 'opposition']
    parties_by_block = []
    for block in block_order:
        block_parties = [p for p in all_party_names if party_to_block.get(normalize_party_name(p)) == block]
        parties_by_block.extend(block_parties)
    # Add any parties not in the blocks (e.g., historical/defunct parties)
    other_parties = [p for p in all_party_names if p not in parties_by_block]
    all_party_names_ordered = parties_by_block + other_parties

    all_party_colors = [party_to_color.get(normalize_party_name(p), '#1e88e5') for p in all_party_names_ordered]

    # Build the data: for each party, a list of seat counts per poll (0 if not present)
    poll_party_seats = []
    for party in all_party_names_ordered:
        seats_per_poll = []
        for poll in all_polls:
            # Find the result for this party in this poll
            result = next((r for r in poll.results if r.party_name == party), None)
            seats_per_poll.append(result.seats if result else 0)
        poll_party_seats.append(seats_per_poll)

    return poll_dates, all_party_names_ordered, all_party_colors, poll_party_seats

@election_bp.route('/election')
def election():
    # Get the last 5 polls
    latest_polls = Poll.query.order_by(Poll.date.desc()).limit(5).all()
    party_averages = get_poll_averages(latest_polls)
    sorted_parties, filtered_integer_seats = allocate_seats(party_averages)
    party_labels = [party for party, seats in sorted_parties]
    party_seats = [seats for party, seats in sorted_parties]
    blocks_path = os.path.join(os.path.dirname(__file__), '../static/json/party_blocks.json')
    with open(blocks_path, encoding='utf-8') as f:
        party_blocks = json.load(f)
    party_colors, party_to_color = get_party_colors(party_blocks, party_labels)
    # Serialize party_to_color for JS
    party_to_color_json = party_to_color
    block_labels, block_seats, block_colors = get_block_data(filtered_integer_seats, party_blocks)
    poll_dates, all_party_names, all_party_colors, poll_party_seats = get_poll_history_data()

    # Serialize polls for JSON
    def poll_to_dict(poll):
        return {
            "id": poll.id,
            "date": poll.date.strftime('%d/%m/%Y'),
            "pollster": poll.pollster,
            "publisher": poll.publisher,
            "results": [
                {"party_name": r.party_name, "seats": r.seats} for r in poll.results
            ]
        }
    polls_json = [poll_to_dict(p) for p in latest_polls]

    return render_template('election_screen.html',
                         polls=latest_polls,
                         polls_json=polls_json,
                         party_averages=sorted_parties,
                         party_labels=party_labels,
                         party_seats=party_seats,
                         party_colors=party_colors,
                         party_to_color_json=party_to_color_json,
                         block_labels=block_labels,
                         block_seats=block_seats,
                         block_colors=block_colors,
                         poll_dates=poll_dates,
                         all_party_names=all_party_names,
                         all_party_colors=all_party_colors,
                         poll_party_seats=poll_party_seats)

