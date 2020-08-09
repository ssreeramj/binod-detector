import json
import os
import pandas as pd 
import texthero as hero

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

API_KEY = os.getenv('YOUTUBE_API_KEY')
VIDEO_ID = 'CbNYxFIQ5jI'

# get list of comments from a response object
def get_comments(response):
    comments = []
    items = response.get('items')
    for objects in items:
        comment_text = objects.get('snippet').get('topLevelComment').get('snippet').get('textDisplay')
        comments.append(comment_text)

    return comments

# getting comments from api
count = 10
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

while next_page_token and count:
    next_request = youtube.commentThreads().list_next(
        request, response
    )

    next_response = next_request.execute()
    all_comments.extend(get_comments(next_response))

    next_page_token = next_response.get('nextPageToken', 0)
    request, response = next_request, next_response
    count -= 1

with open('comments.txt', 'w') as f:
    json.dump(all_comments, f, indent=2)

# data preprocessing
# df = pd.DataFrame(all_comments, columns=['text'])
# df['clean_text'] = hero.clean(df['text'])

# # print(df.head())
# figure = hero.visualization.wordcloud(df['clean_text'], return_figure=True)
# figure.savefig('plot.png')


