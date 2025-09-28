import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
import os
from prettytable import PrettyTable
#version 1.2.0



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

    table=PrettyTable()
    table.field_names=["Index","Title","Artist"]
    for i in range(len(songs)):
        table.add_row([i+1,songs[i][0],songs[i][1]])

    print(table)


    cont=input("Continue with the downloading? [Y/n]\n==>")
    if cont.lower()=='y':
        return songs
    else:
        print("Returning to main menu...")
        Main()

def Playlist_Downloader(Songs):
    try:
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
    except :
        print("Inputed link is not supported, make sure its a public playlist only")



def Main():
    if os.path.isfile("credentials.txt"):
        try:
            choice=int(input("[1] Download the playlist\n[2] Re-enter the credentials\n[0] Exit\n==>"))
            if choice == 1:
                link=input("Paste the link of the playlist (MUST BE A PUBLIC PLAYLIST):\n==>")
                Songs=spotify_playlist(link);    
                Playlist_Downloader(Songs);
            elif choice ==2:
                with open("credentials.txt","w") as f:
                    id=input("Enter your Spotify Client ID:\n==>")
                    f.writelines(str(id)+"\n")
                    s_id=input("Enter your client secret ID:\n==>")
                    f.writelines(str(s_id)+"\n")
                Main()
            elif choice==0:
                print("Exiting...")
            else:
                print("Please enter a valid option")
                Main()
        except:
            Main()

            

        
    else:
        with open("credentials.txt","w") as f:
            id=input("Enter your Spotify Client ID:\n==>")
            f.writelines(str(id)+"\n")
            s_id=input("Enter your client secret ID:\n==>")
            f.writelines(str(s_id)+"\n")
        Main()

Main()