# Jellysports

A simple repo to create a m3u playlist for sports livestreams

## Local Setup
``` shell
git clone https://github.com/SolarWolf-Code/jellysports.git
cd jellysports
pip3 install -r requirements.txt
python3 main.py
```
## How to use on Jellyfin
1. Go to the dashboard
2. Click on `Live TV`
3. Click on `+` next to Tuner Devices
4. Under `Tunner Type` select `M3U Tuner`
5. Paste `https://raw.githubusercontent.com/SolarWolf-Code/jellysports/main/playlist.m3u` into `File or URL`
6. Click `Save`
7. Go back Home and click on `Live TV`
