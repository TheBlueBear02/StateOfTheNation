from flask import Blueprint, render_template, request, jsonify
import json
import random
import datetime

# Create Blueprint
game_bp = Blueprint('game', __name__)

# Load Knesset members data from JSON file
def load_knesset_data():
    with open("static/json/knesset_members.json", "r", encoding="utf-8") as file:
        return json.load(file)

data = load_knesset_data()

# Function to get the day's specific Knesset member for a given difficulty
def get_daily_knesset_member(difficulty):
    # Get current date for deterministic selection
    today = datetime.datetime.now().date()
    day_of_year = today.timetuple().tm_yday  # Get day of year (1-366)
    
    # Get members for the specified difficulty
    members_by_difficulty = [level['members'] for level in data if level['difficulty'] == difficulty]
    
    if not members_by_difficulty or not members_by_difficulty[0]:
        return None
    
    # Get members list for the specified difficulty
    members = members_by_difficulty[0]
    
    # Use day of year to deterministically select a member
    # Modulo ensures we always get a valid index
    daily_index = day_of_year % len(members)
    return members[daily_index]

@game_bp.route("/guessthekm")
def game():
    return render_template("game.html")

@game_bp.route("/api/question", methods=["POST"])
def get_question():
    difficulty = request.json.get("difficulty", "קל")
    
    # Get the daily Knesset member for the specified difficulty
    member = get_daily_knesset_member(difficulty)
    
    if not member:
        return jsonify({"error": "No members found for the specified difficulty"}), 404
    
    question = {
        "name_hidden": member["name"],
        "year_first": member.get("year_first", "לא ידוע"),
        "year_last": member.get("year_last", "לא ידוע"),
        "important_role": member.get("important_role", "לא ידוע"),
        "career_before": member.get("career_before", "לא ידוע"),
        "party": member.get("party", "לא ידוע"),
    }
    
    return jsonify(question)

@game_bp.route("/api/check", methods=["POST"])
def check_answer():
    user_input = request.json.get("answer", "").strip()
    difficulty = request.json.get("difficulty", "")
    
    # Get the correct answer based on today's date and difficulty
    daily_member = get_daily_knesset_member(difficulty)
    if not daily_member:
        return jsonify({"correct": False, "error": "Could not determine correct answer"}), 400
    
    correct_answer = daily_member["name"]
    
    is_correct = user_input == correct_answer
    return jsonify({"correct": is_correct})

