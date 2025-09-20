import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
import os
#version 1.1.0



def spotify_playlist(link):
    with open("credentials.txt") as f:
        client_id = f.readline().strip()
        client_secret = f.readline().strip()
        
    

    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    playlist_link = link.strip()
    if not playlist_link.startswith("https://open.spotify.com/playlist/"):
        print("Error: Invalid Spotify playlist URL.")
        return None
    try:
        playlist_id = playlist_link.split("/")[-1].split("?")[0]
    except IndexError:
        print("Error: Invalid playlist URL.")
        return None

    songs = []
    limit = 100
    offset = 0

    while True:
        results = sp.playlist_items(playlist_id, limit=limit, offset=offset)
        items = results['items']

        if not items:
            break

        for item in items:
            track = item['track']
            if track:  
                songs.append((track['name'],track['artists'][0]['name']))

        offset += limit


    return songs

def Playlist_Downloader(Songs):
    for index,song in enumerate(Songs):
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,  
            'outtmpl': 'Downloads/%(title)s.%(ext)s',  
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',  
            }]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch1:{song[0]} {song[1]} lyrics"])





def Main():
    if os.path.isfile("credentials.txt"):
        
        choice=int(input("[1] Download the playlist\n[2] Re-enter the credentials\n==>"))
        if choice == 1:
            link=input("Paste the link of the playlist (MUST BE A PUBLIC PLAYLIST):\n==>")
            Songs=spotify_playlist(link);    
            Playlist_Downloader(Songs);
        elif choice ==2:
            with open("credentials.txt","w") as f:
                id=input("Enter your Spotify Client ID:\n==>")
                f.write(id)
                s_id=input("Enter your client secret ID:\n==>")
                f.write(s_id)
            Main()
        
        else:
            print("Please enter a valid option")
            Main()

        
    else:
        with open("credentials.txt","w") as f:
            id=input("Enter your Spotify Client ID:\n==>")
            f.write(id)
            s_id=input("Enter your client secret ID:\n==>")
            f.write(s_id)
        Main()

Main()