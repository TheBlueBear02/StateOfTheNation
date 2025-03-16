from flask import Blueprint, render_template, request, jsonify
import json
import random

# Create Blueprint
game_bp = Blueprint('game', __name__)

# Load Knesset members data from JSON file
def load_knesset_data():
    with open("static/json/knesset_members.json", "r", encoding="utf-8") as file:
        return json.load(file)

data = load_knesset_data()

@game_bp.route("/guessthekm")
def game():
    return render_template("game.html")

@game_bp.route("/api/question", methods=["POST"])
def get_question():
    difficulty = request.json.get("difficulty", "קל")
    
    # Filter members by difficulty
    members_by_difficulty = [level['members'] for level in data if level['difficulty'] == difficulty]
    
    if not members_by_difficulty:
        return jsonify({"error": "No members found for the specified difficulty"}), 404

    # Flatten the list of members
    members = members_by_difficulty[0]  # Get the first (and only) list of members for the selected difficulty

    # Select a random Knesset member
    member = random.choice(members)
    
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
    correct_answer = request.json.get("correct_name", "")
    
    is_correct = user_input == correct_answer
    return jsonify({"correct": is_correct})

