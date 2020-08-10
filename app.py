import os
import re
import streamlit as st

from main import get_all_comments, get_wordcloud, get_pie_plot

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

API_KEY = os.getenv('YOUTUBE_API_KEY')

youtube = build('youtube', 'v3', developerKey=API_KEY)

if __name__ == '__main__':
    st.title('Binod Detector:rocket:')

    st.header("Unless you are living under a rock, you must have come across \
        the word 'BINOD' on social media. This simple webapp helps you visualize \
        comment section of a youtube video and gives us the percentage of comments \
        having the word in it.")

    url = st.text_input(label='Enter the url of a youtube video.')
    pattern = re.compile('^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+')

    if re.match(pattern, url):
        try:
            video_id = url.split('?')[1].split('=')[1]
            if '&' in video_id:
                video_id = video_id.split('&')[0]

            with st.spinner('Scraping comments...'):
                comments_list = get_all_comments(youtube, video_id)

            st.balloons()
            word_cloud, df = get_wordcloud(comments_list)

            pie_plot = get_pie_plot(df)

            st.subheader('Lets have a look at some random comments of the youtube video')
            st.info('Hover on the text to see the full text')
            st.dataframe(df.loc[:, 'text'].sample(20))

            st.subheader('Here we can see the visualization of common words that \
                are there in the comments.')
            st.write(word_cloud)

            st.subheader("Now we see the distribution of comments which have 'BINOD' \
                in them.")
            st.warning('If the comment section does not have binod, then the distribution \
                would show the most common word')
            st.write(pie_plot)
        except Exception as e:
            # st.subheader(e)
            st.subheader('Could not get the video id, please paste the correct URL')

    else:
        st.subheader('Please enter a valid URL of a youtube video')

