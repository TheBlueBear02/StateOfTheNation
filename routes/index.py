from flask import Blueprint, render_template, request
from datetime import datetime
from pyluach import dates
from models import Tweet, ParliamentMember, db

index_bp = Blueprint('index', __name__)

def get_date():
    return datetime.today().strftime('%d.%m.%Y')

def get_hebrew_date():
    today = dates.HebrewDate.today()
    return today.hebrew_date_string()

# This function is used to get the knesset members and their tweet count 
def get_knesset_members():
    all_kms = db.session.query(ParliamentMember).all()
    km_list = []
    
    for km in all_kms:
        tweet_count = db.session.query(Tweet).filter(Tweet.twitter_id == km.twitter_id).count()
        
        km_data = {
            'id': km.id,
            'name': km.name,
            'party': km.party,
            'is_coalition': km.is_coalition,
            'image': km.image,
            'additional_role': km.additional_role,
            'twitter_id': km.twitter_id,
            'tweet_count': tweet_count
        }
        km_list.append(km_data)

    # Sort the km_list by tweet_count in descending order
    km_list = sorted(km_list, key=lambda x: x['tweet_count'], reverse=True)
    return km_list

# This function is used to get the tweets of a specific knesset member
@index_bp.route('/get_km_tweets', methods=['POST'])
def get_km_tweets():
    twitter_id = request.json.get('twitter_id')
    km_tweets = db.session.query(Tweet).filter(Tweet.twitter_id == twitter_id)
    km_data = db.session.query(ParliamentMember).filter(ParliamentMember.twitter_id == twitter_id).first()
    km_tweets_list = []
    for tweet in km_tweets:
        tweet_data = {
            'id': tweet.id,
            'text': tweet.text,
            'date': tweet.date,
            'time': tweet.time,
            'topic': tweet.topic,
            'image': tweet.image,
            'name': km_data.name,
            'party': km_data.party,
            'is_coalition': km_data.is_coalition,
            'minister_image': km_data.image,
            'additional_role': km_data.additional_role,
        }
        km_tweets_list.append(tweet_data)
    return list(reversed(km_tweets_list))

@index_bp.route('/get_all_tweets', methods=['POST'])
def get_all_tweets():
    all_tweets = db.session.query(Tweet).all()
    all_kms = db.session.query(ParliamentMember).all()
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
    return list(reversed(tweets_list))
@index_bp.route('/')
def index():
    # Knesschat backend
    tweets_list = get_all_tweets()
    km_data = get_knesset_members() 
    return render_template('index.html', today_date=get_date(), hebrew_date=get_hebrew_date(), km_data=km_data)
