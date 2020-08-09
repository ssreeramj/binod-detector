import json
import os
import pandas as pd 
import plotly.express as px
import texthero as hero


# get list of comments from a response object
def get_comments(response):
    comments = []
    items = response.get('items')
    for objects in items:
        comment_text = objects.get('snippet').get('topLevelComment').get('snippet').get('textDisplay')
        comments.append(comment_text)

    return comments

# get all comments
def get_all_comments(youtube, video_id, count=20):
    all_comments = []

    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
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

    return all_comments

# with open('comments.txt', 'w') as f:
#     json.dump(all_comments, f, indent=2)

# data preprocessing
def get_wordcloud(all_comments):
    df = pd.DataFrame(all_comments, columns=['text'])
    df['clean_text'] = hero.clean(df['text'])

    figure = hero.visualization.wordcloud(df['clean_text'], return_figure=True)
    # figure.savefig('plot.png')
    return figure, df


def get_pie_plot(df):
    top_words = hero.visualization.top_words(df['clean_text'])

    df['is_binod'] = df['clean_text'].apply(lambda x: 'binod' in x)

    values = list(df['is_binod'].value_counts())

    if len(values) != 2:
        most_common_word = hero.visualization.top_words(df['clean_text']).keys()[0]
        df['is_common_word'] = df['clean_text'].apply(lambda x: most_common_word in x)

        values = list(df['is_common_word'].value_counts())
        names = ['Others', str.capitalize(most_common_word)]
    else:
        names = ['Others', 'Binod']

    pie_fig = px.pie(values=values, names=names)

    return pie_fig




