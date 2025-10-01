import yt_dlp
from prettytable import PrettyTable
import requests
import time
import base64
import pyotp
from urllib.parse import urlparse, parse_qs
from random import randrange
from prettytable import PrettyTable
#Version 2.0.0

def get_random_user_agent():
    return f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{randrange(11, 15)}_{randrange(4, 9)}) " \
           f"AppleWebKit/{randrange(530, 537)}.{randrange(30, 37)} (KHTML, like Gecko) " \
           f"Chrome/{randrange(80, 105)}.0.{randrange(3000, 4500)}.{randrange(60, 125)} " \
           f"Safari/{randrange(530, 537)}.{randrange(30, 36)}"

def parse_uri(uri):
    u = urlparse(uri)
    parts = []
    if u.scheme == "spotify":
        parts = uri.split(":")
    else:
        parts = u.path.split("/")
    if len(parts) >= 3 and parts[1] == "playlist":
        return {"type": "playlist", "id": parts[2]}
    raise Exception("Only playlist URLs supported here.")

def generate_totp():
    url = "https://raw.githubusercontent.com/Thereallo1026/spotify-secrets/refs/heads/main/secrets/secretBytes.json"
    resp = requests.get(url, timeout=10)
    secrets_list = resp.json()
    latest_entry = max(secrets_list, key=lambda x: x["version"])
    secret_cipher = latest_entry["secret"]

    processed = [byte ^ ((i % 33) + 9) for i, byte in enumerate(secret_cipher)]
    processed_str = "".join(map(str, processed))
    utf8_bytes = processed_str.encode('utf-8')
    secret_bytes = bytes.fromhex(utf8_bytes.hex())
    b32_secret = base64.b32encode(secret_bytes).decode('utf-8')
    totp = pyotp.TOTP(b32_secret)

    headers = {"User-Agent": get_random_user_agent()}
    resp = requests.get("https://open.spotify.com/api/server-time", headers=headers, timeout=10)
    server_time = resp.json()["serverTime"]
    return totp, server_time, latest_entry["version"]

def get_access_token():
    totp, server_time, ver = generate_totp()
    otp_code = totp.at(int(server_time))
    timestamp_ms = int(time.time() * 1000)

    params = {
        'reason': 'init',
        'productType': 'web-player',
        'totp': otp_code,
        'totpServerTime': server_time,
        'totpVer': str(ver),
        'sTime': server_time,
        'cTime': timestamp_ms,
    }
    headers = {"User-Agent": get_random_user_agent()}
    resp = requests.get("https://open.spotify.com/api/token", headers=headers, params=params, timeout=10)
    return resp.json()["accessToken"]

def get_playlist_tracks(playlist_url):
    info = parse_uri(playlist_url)
    if info["type"] != "playlist":
        raise Exception("Not a playlist URL")

    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}", "User-Agent": get_random_user_agent()}

    tracks = []
    url = f"https://api.spotify.com/v1/playlists/{info['id']}/tracks?limit=100"
    while url:
        resp = requests.get(url, headers=headers, timeout=10).json()
        for item in resp.get("items", []):
            track = item.get("track")
            if not track:
                continue
            name = track.get("name", "")
            artists = track.get("artists", [])
            first_artist = artists[0]["name"] if artists else ""
            tracks.append((name, first_artist))
        url = resp.get("next")

    table=PrettyTable()
    table.field_names=["Index","Title","Artist"]
    for i in range(len(tracks)):
        table.add_row([i+1,tracks[i][0],tracks[i][1]])

    print(table)
    
    cont=input("Continue with the downloading? [Y/n]\n==>")
    if cont.lower()=='y':
        return tracks
    else:
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
    choice=int(input("----- SPOTIFY PLAYLIST DOWNLOADER -----\n[1] Download the playlist\n[0] Exit\n==>"))
    if choice == 1:
        link=input("Paste the link of the playlist (MUST BE A PUBLIC PLAYLIST):\n==>")
        Songs=get_playlist_tracks(link);    
        Playlist_Downloader(Songs);
    elif choice==0:
        print("Exiting...")
    else:
        print("Please enter a valid option")
        Main()
    

Main()
