import requests
import os
import json
from datetime import datetime, timedelta

# Replace with your own Bearer Token
BEARER_TOKEN = ''

# Define the filename where the JSON data will be saved
filename = 'knesschat-backend\list_tweets.json'

# Function to create headers for the request
def create_headers(bearer_token):
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'User-Agent': 'v2ListTweetsPython'
    }
    return headers

# Function to make the request
def get_list_tweets(list_id, params):
    url = f'https://api.x.com/2/lists/{list_id}/tweets'
    headers = create_headers(BEARER_TOKEN)
    params = {}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        print(f"Got tweets successfuly from twitter")
    else:
        raise Exception(f"Request returned an error: {response.status_code} {response.text}")
    return response.json()

# Replace with your List ID
LIST_ID = '1869748855257862583'


params = {
    "max_results": 5,  # Number of tweets you want to retrieve per request (maximum is 100)
    "tweet.fields": "id,text,created_at",  # Specify which fields to retrieve
}
# Get and print the current time
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime('%H:%M:%S %Y-%m-%d')

print(f"Script started at: {formatted_datetime}")

# Fetch the list tweets
json_response = get_list_tweets(LIST_ID, params)

# Extract new tweets from the response
new_tweets = json_response.get('data', [])

# Load existing data if file exists
if os.path.exists(filename):
    with open(filename, 'r') as json_file:
        try:
            existing_data = json.load(json_file)
        except json.JSONDecodeError:
            existing_data = []
else:
    existing_data = []

print(existing_data)
# Extract existing tweet IDs for comparison
existing_tweet_ids = {tweet['id'] for tweet in existing_data}

# Filter out tweets that are already in the existing data
unique_new_tweets = [tweet for tweet in new_tweets if tweet['id'] not in existing_tweet_ids]

# Append unique new tweets to existing data
existing_data.extend(unique_new_tweets)

# Save updated data back to the file
with open(filename, 'w') as json_file:
    json.dump(existing_data, json_file, indent=4)

print(f"Added {len(unique_new_tweets)} new tweets to {filename}")

# Calculate the time 15 minutes from now
future_datetime = current_datetime + timedelta(minutes=15)
formatted_future_datetime = future_datetime.strftime('%H:%M:%S %Y-%m-%d')

print(f"Next run can be at: {formatted_future_datetime}")