from flask import Blueprint, render_template, request, jsonify
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


def get_tweets_data(tweets):
    tweets_list = []
    for tweet in tweets:
        km_data = db.session.query(ParliamentMember).filter(ParliamentMember.twitter_id == tweet.twitter_id).first()
        if km_data is None:
            # Skip this tweet if no matching ParliamentMember is found
            continue
        tweet_data = {
            'id': tweet.id,
            'text': tweet.text,
            'date': tweet.date,
            'time': tweet.time,
            'topic': tweet.topic,
            'name': km_data.name,
            'party': km_data.party,
            'is_coalition': km_data.is_coalition,
            'minister_image': km_data.image,
            'additional_role': km_data.additional_role,
            'image': tweet.image
        }
        tweets_list.append(tweet_data)
    return jsonify(list(reversed(tweets_list)))
# This function is used to get the tweets of a specific knesset member
@index_bp.route('/get_km_tweets', methods=['POST'])
def get_km_tweets():
    twitter_id = request.json.get('twitter_id')
    km_tweets = db.session.query(Tweet).filter(Tweet.twitter_id == twitter_id)
    
    return get_tweets_data(km_tweets)

@index_bp.route('/get_all_tweets', methods=['POST'])
def get_all_tweets():
    all_tweets = db.session.query(Tweet).all()

    return get_tweets_data(all_tweets)

@index_bp.route('/get_tweets_by_topic', methods=['POST'])
def get_filtered_tweets():
    topic = request.json.get('topic')
    if not topic:
        return jsonify({'error': 'Missing topic'}), 400

    all_tweets = db.session.query(Tweet).filter(Tweet.topic == topic)
    
    return get_tweets_data(all_tweets)

@index_bp.route('/')
def index():
    # Knesschat backend
    tweets_list = get_all_tweets()
    km_data = get_knesset_members() 
    return render_template('index.html', today_date=get_date(), hebrew_date=get_hebrew_date(), km_data=km_data)
