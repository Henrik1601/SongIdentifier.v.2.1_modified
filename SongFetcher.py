import streamlit as st
import requests
from urllib.parse import urlencode

# YouTube Data API endpoint
SEARCH_ENDPOINT = 'https://www.googleapis.com/youtube/v3/search'
VIDEO_ENDPOINT = 'https://www.googleapis.com/youtube/v3/videos'

# YouTube Data API key
API_KEY = '<API_KEY>'

# Function to search for songs on YouTube based on lyrics
def search_songs_by_lyrics(lyrics):
    params = {
        'part': 'snippet',
        'q': lyrics,
        'type': 'video',
        'maxResults': 5,
        'key': API_KEY
    }

    url = SEARCH_ENDPOINT + '?' + urlencode(params)

    response = requests.get(url)
    data = response.json()

    songs = []
    for item in data['items']:
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        view_count = get_view_count(video_id)
        songs.append({'title': title, 'video_id': video_id, 'view_count': view_count})

    # Sort the songs based on view count in descending order
    songs = sorted(songs, key=lambda x: x['view_count'], reverse=True)

    return songs

# Function to get the view count of a YouTube video
def get_view_count(video_id):
    params = {
        'part': 'statistics',
        'id': video_id,
        'key': API_KEY
    }

    url = VIDEO_ENDPOINT + '?' + urlencode(params)

    response = requests.get(url)
    data = response.json()

    view_count = int(data['items'][0]['statistics']['viewCount'])

    return view_count

# Streamlit web interface
def main():
    st.title('Lyrics to Songs')

    # Get user input for the lyrics
    lyrics = st.text_input('Enter a single line of lyrics')

    # Search for songs on YouTube based on lyrics
    if lyrics:
        matching_songs = search_songs_by_lyrics(lyrics)

        # Display the details of matching songs
        if len(matching_songs) > 0:
            st.subheader('Matching songs:')
            for song in matching_songs:
                st.write('Song:', song['title'])
                st.write('View Count:', song['view_count'])
                st.video(f'https://www.youtube.com/watch?v={song["video_id"]}')
                st.write('---')
        else:
            st.write('No matching songs found.')

if __name__ == '__main__':
    main()
