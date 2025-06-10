from flask import Blueprint, render_template

election_bp = Blueprint('election', __name__)

@election_bp.route('/election')
def election():
    return render_template('election_screen.html') 