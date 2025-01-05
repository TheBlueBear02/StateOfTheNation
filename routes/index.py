from flask import Blueprint, render_template
from datetime import datetime
from pyluach import dates
from models import Tweet, ParliamentMember, db

index_bp = Blueprint('index', __name__)

def get_date():
    return datetime.today().strftime('%d.%m.%Y')

def get_hebrew_date():
    today = dates.HebrewDate.today()
    return today.hebrew_date_string()

@index_bp.route('/')
def index():
    # Knesschat backend
   # Query the database for all tweets and kms
    all_tweets = db.session.query(Tweet).all()
    all_kms = db.session.query(ParliamentMember).all()
    # create list of dicts that contains the feed's tweets
    name = ""
    party = ""
    is_coalition = False
    image = ""
    additional_role = ""
    tweets_list = []
    for tweet in all_tweets:
        for member in all_kms:
            try:
                if int(member.twitter_id) == int(tweet.twitter_id):
                    name = member.name
                    party = member.party
                    is_coalition = member.is_coalition
                    image = member.image
                    additional_role = member.additional_role
                    break
            except:
                #print("knesset member not found")
                print()
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
        tweets_list.append(tweet_data)
    return render_template('index.html', today_date=get_date(), hebrew_date=get_hebrew_date(), tweets=list(reversed(tweets_list)), all_kms=all_kms)
