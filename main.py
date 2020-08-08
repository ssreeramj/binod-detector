import json
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

API_KEY = os.getenv('YOUTUBE_API_KEY')
VIDEO_ID = 'sW12dNPz_7c'

# get list of comments from a response object
def get_comments(response):
    comments = []
    items = response.get('items')
    for objects in items:
        comment_text = objects.get('snippet').get('topLevelComment').get('snippet').get('textDisplay')
        comments.append(comment_text)

    return comments

all_comments = []
youtube = build('youtube', 'v3', developerKey=API_KEY)

request = youtube.commentThreads().list(
    part='snippet',
    videoId=VIDEO_ID,
    maxResults=100,
    textFormat='plainText',
)
response = request.execute()
all_comments.extend(get_comments(response))

next_page_token = response.get('nextPageToken', 0)

while next_page_token:
    next_request = youtube.commentThreads().list_next(
        request, response
    )

    next_response = next_request.execute()
    all_comments.extend(get_comments(next_response))

    next_page_token = next_response.get('nextPageToken', 0)
    request, response = next_request, next_response


with open('comments.txt', 'w') as f:
    json.dump(all_comments, f, indent=2)
