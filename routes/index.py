from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from datetime import datetime
from pyluach import dates
from models import db, Tweet, ParliamentMember, Index, Office, IndexData
import random
import csv
import io
from sqlalchemy import exists

index_bp = Blueprint('index', __name__)

def get_date():
    return datetime.today().strftime('%d.%m.%Y')

def get_hebrew_date():
    today = dates.HebrewDate.today()
    return today.hebrew_date_string()

def is_mobile():
    """Check if the request comes from a mobile device."""
    user_agent = request.headers.get("User-Agent", "").lower()
    mobile_keywords = ["mobi", "android", "iphone", "ipad"]
    return any(keyword in user_agent for keyword in mobile_keywords)

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
            'tweet_count': tweet_count,
            'twitter_feed_id' : km.twitter_feed_id
        }
        km_list.append(km_data)
    # Sort the km_list by tweet_count in descending order
    #km_list = sorted(km_list, key=lambda x: x['tweet_count'], reverse=True)
    random.shuffle(km_list)


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

@index_bp.route('/add_index', methods=['POST'])
def add_index():
    try:
        index_name = request.form.get('index_name')
        is_kpi = request.form.get('kpi_policy') == "true"
        news_feed_id = request.form.get('news_feed_id')
        index_info = request.form.get('index_info')
        alert = request.form.get('alert') == "true"
        is_shown = request.form.get('is_shown') == "true"
        icon_url = request.form.get('icon_url')
        chart_type = request.form.get('chart_type')
        office_id = request.form.get('office_id')
        source = request.form.get('source')

        if not index_name or not office_id or not chart_type:
            return jsonify({"success": False, "error": "Index Name, Office, and Chart Type are required!"})

        new_index = Index(
            name=index_name,
            info=index_info,
            icon=icon_url,
            is_kpi=is_kpi,
            office_id=office_id,
            news_feed_id=news_feed_id,
            alert=alert,
            is_shown=is_shown,
            chart_type=chart_type,
            source=source
        )

        db.session.add(new_index)
        db.session.commit()

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})




@index_bp.route("/upload_csv", methods=["POST"])
def upload_csv():
    try:
        office_id = request.form.get("office_id")
        index_id = request.form.get("index_id")
        file = request.files.get("csv_file")

        if not file or not office_id or not index_id:
            return jsonify({"error": "Missing required parameters"}), 400

        try:
            index_id = int(index_id)  # Ensure index_id is an integer
        except ValueError:
            return jsonify({"error": "Invalid index_id"}), 400

        print(f"Received file for office_id={office_id}, index_id={index_id}")

        # Read file content
        file_content = file.read().decode("utf-8")
        file_stream = io.StringIO(file_content)
        csv_reader = csv.reader(file_stream)
        next(csv_reader, None)  # Skip header row if present

        new_rows = []
        invalid_rows = []

        # Ensure database has the latest committed data
        db.session.commit()

        for row in csv_reader:
            if len(row) < 2:
                print(f"Skipping row due to insufficient columns: {row}")
                continue

            date_str, value = row[0].strip(), row[1].strip()

            try:
                date_obj = datetime.strptime(date_str, "%d.%m.%Y").strftime("%d.%m.%Y").strip()
            except ValueError:
                invalid_rows.append(date_str)
                continue

            # Check if the row exists in the DB using LIKE for better matching
            row_exists = db.session.query(
                exists().where(
                    (IndexData.index_id == index_id) &
                    (IndexData.label.like(f"%{date_obj}%"))  # Flexible match
                )
            ).scalar()

            if row_exists:
                print(f"Date {date_obj} already exists in DB, skipping.")
            else:
                print(f"Date {date_obj} not found in DB, adding to new rows.")
                new_rows.append(IndexData(index_id=index_id, label=date_obj, value=value))

        if invalid_rows:
            print(f"Skipped invalid dates: {invalid_rows}")

        if new_rows:
            #db.session.bulk_save_objects(new_rows)
            #db.session.commit()
            print(f"Inserted {len(new_rows)} new records.")
            return jsonify({"message": f"Inserted {len(new_rows)} new records"}), 200
        else:
            return jsonify({"message": "No new records to insert"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500




# Define the admin password (store securely in production)
ADMIN_PASSWORD = "pass"

@index_bp.route("/get_offices", methods=["GET"])
def get_offices():
    return jsonify([{"id": o.id, "name": o.name} for o in Office.query.all()])


@index_bp.route("/get_indexes/<int:office_id>", methods=["GET"])
def get_indexes(office_id):
    indexes = db.session.query(Index).filter_by(office_id=office_id).all()
    return jsonify([{"id": index.id, "name": index.name} for index in indexes])


@index_bp.route("/admin", methods=["GET", "POST"])
def admin():
    if "admin_logged_in" in session:
        indexes = db.session.query(Index).all()
        return render_template("admin-screen/admin_screen.html", indexes=indexes)  

    if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("index.admin"))

        return render_template("admin-screen/admin_login.html", error="Incorrect password")

    return render_template("admin-screen/admin_login.html")

@index_bp.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("index.admin"))  # Redirects back to the admin login page


@index_bp.route("/knesschat")
def knesschat():
    km_data = get_knesset_members() 
    return render_template("knesschat-screen.html")  # Ensure this template exists

@index_bp.route('/')
def index():
    # Knesschat backend
    km_data = get_knesset_members() 
    if is_mobile():
        return render_template("mobile.html")  # Render mobile version
    return render_template('index.html', today_date=get_date(), hebrew_date=get_hebrew_date(), km_data=km_data)  # Render desktop version

