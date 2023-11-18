import requests
import re
import threading

def stream_ended(url: str, all_urls: dict[str, list[str]], category: str) -> None:
    #EXT-X-ENDLIST
    req = requests.get(url)
    if req.status_code == 200:
        if "#EXT-X-ENDLIST" in req.text:
            all_urls[category].remove(url)
        else:
            print(f"[{category.upper()}] Found vaild stream: {url}")

def get_stream_links(base_url: str, category: str, all_urls: dict[str, list[str]]) -> None:
    # Get all the links
    urls: list[str] = []
    count = 1
    while True:
        url = base_url + f"{category}{count}.m3u8"
        req = requests.get(url)
        if req.status_code == 200:
            urls.append(url)
            count += 1
        else:
            break

    all_urls[category] = urls

def create_playlist(all_urls: dict[str, list[str]]) -> None:
    # create m3u8 playlist
    with open("playlist.m3u", "w") as f:
        f.write("#EXTM3U\n\n")
        for category in all_urls:
            for url in all_urls[category]:
                title = url.split("stream_")[1].split(".m3u8")[0].upper()
                title, number = re.match(r'([A-Za-z]+)(\d+)', title).groups()
                title = title + ' ' + str(int(number)).zfill(2)

                if category == "nba":
                    # https://cdn-icons-png.flaticon.com/512/217/217076.png
                    f.write(f"#EXTINF:-1 tvg-logo=\"https://cdn-icons-png.flaticon.com/512/217/217076.png\" group-title=\"Sports\",{title}\n")
                elif category == "nfl":
                    # https://cdn-icons-png.flaticon.com/512/2972/2972028.png
                    f.write(f"#EXTINF:-1 tvg-logo=\"https://cdn-icons-png.flaticon.com/512/2972/2972028.png\" group-title=\"Sports\",{title}\n")
                elif category == "nhl":
                    # https://cdn-icons-png.flaticon.com/512/2633/2633847.png
                    f.write(f"#EXTINF:-1 tvg-logo=\"https://cdn-icons-png.flaticon.com/512/2633/2633847.png\" group-title=\"Sports\",{title}\n")
                elif category == "box":
                    # https://cdn-icons-png.flaticon.com/512/2503/2503381.png
                    f.write(f"#EXTINF:-1 tvg-logo=\"https://cdn-icons-png.flaticon.com/512/2503/2503381.pngg\" group-title=\"Sports\",{title}\n")
                elif category == "ufc":
                    # https://cdn-icons-png.flaticon.com/512/928/928633.png
                    f.write(f"#EXTINF:-1 tvg-logo=\"https://cdn-icons-png.flaticon.com/512/928/928633.png\" group-title=\"Sports\",{title}\n")

                f.write(f"{url}\n\n")


def main():
    base_url = "https://sports.freesportstime.com/live/stream_"
    print(f"Attempting to get all stream links with base url {base_url}")
    all_urls: dict[str, list[str]] = {}

    threads: list[threading.Thread] = []
    categories: list[str] = ["nfl", "nba", "nhl", "box", "ufc"]
    print(f"Categories tracked: {categories}")
    for category in categories:
        t = threading.Thread(target=get_stream_links, args=(base_url, category, all_urls))
        threads.append(t)
    
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # double check threads and remove ended streams
    threads: list[threading.Thread] = []

    for category in all_urls:
        for url in all_urls[category]:
            t = threading.Thread(target=stream_ended, args=(url,all_urls,category))
            threads.append(t)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("Creating playlist.m3u")
    create_playlist(all_urls)





if __name__ == "__main__":
    main()  

        
