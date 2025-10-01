# Spotify Playlist to MP3 files

Reads names of the songs in your public Spotify Playlist and downloads them using yt_dlp

## Prerequisites 

**The user must have FFmpeg in their system**  .

```bash
#windows,open powershell and type the command given below
winget install ffmpeg

#macOS
brew install ffmpeg

#linux ubuntu (use your respective package manager)
sudo apt install ffmpeg
```



## Setting up the script

1.  create a virual python env using terminal. This creates a folder (virtual environmet) called spotify .
```bash
python -m venv spotify
```
3. Move both Main.py and requirements.txt into it

## Running the script

1. Activate the virtual. **You need to do this each time you want to run the code**.
```bash
# for windows

spotify\Scripts\activate

# for linux/macOS
source spotify/bin/activate
```
2. Change directory into spotify folder and download required python packages, **you only need to do this once**.
```bash
pip install -r requirements.txt
```
3. Run the Main.py to get started.The songs will be downloaded into a folder named Downloads within the spotify folder automatically.

4. Deactivate the v_env once you are done.
```bash
deactivate
```



