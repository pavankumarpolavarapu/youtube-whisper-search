import os
import yt_dlp 

from pathlib import Path
from typing import Optional, Sequence
import whisper

import argparse
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def download_multiple_youtube_videos(playlist_videos: list[str, str]) -> list[str]:
    downloaded_video_paths = []
    try:
        for item in playlist_videos:
            file_path = f"{os.getcwd()}/videos/{item[0]}.mp4"
            if not os.path.isfile(file_path):
                if(download_single_youtube_video(item[1], file_path)):
                    downloaded_video_paths.append(file_path)
    except Exception as e:
        print("An exception occurred while downloading videos")
        raise

    return downloaded_video_paths

def download_single_youtube_video(url: str,file_path: str) -> str:
    """Save a YouTube video URL to mp3.

    Args:
        url (str): A YouTube video URL.

    Returns:
        str: The filename of the mp3 file.
    """

    options = {
        'format': 'mp4',
        'outtmpl': file_path 
    }

    try:
        with yt_dlp.YoutubeDL(options) as downloader:
            downloader.download(["" + url + ""])
    except Exception as e:
        raise
    
    return file_path

def get_google_api_client(api_service_name: str, api_version: str, developer_key: str) -> object:
    service = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=developer_key)

    return service
    

def get_youtube_playlist_videos(service, playlist: str, page_token: str|None, playlist_videos: list[str, str]) -> list[str, str]:

    request = service.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=50,
        playlistId=playlist,
        pageToken=page_token
    )

    response = request.execute()
    
    for item in response["items"]:
        videoId = item["contentDetails"]["videoId"]
        youtube_url = f"https://youtube.com/watch?v={videoId}"
        
        playlist_videos.append([videoId, youtube_url])

    if 'nextPageToken' in response.keys():
        playlist_videos = get_youtube_playlist_videos(service, playlist, response['nextPageToken'], playlist_videos)

    return playlist_videos

def transcribe_single_video(video_file_path: Path, transcript_file_path: Path) -> int:

    try:
        result = model.transcribe(video_file_path)

        if not os.path.isfile(transcript_file_path):
            transcribe_video(video, videoId)

            with open(transcript_file_path, 'w') as f:
                for segment in result["segments"]:
                    line = f"{segment['start']}:{segment['end']} {segment['text']}\n"
                    f.write(line)
    except Exception as e:
        print("An exception has occurred", e.value)
        return 1

    return 0

def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('playlist_id')
    developer_key = os.getenv('developer_key')
    args = parser.parse_args(argv)

    model = whisper.load_model("base")
    
    api_service_name = "youtube"
    api_version = "v3"

    service = get_google_api_client(api_service_name, api_version, developer_key)

    if(service):
        playlist_videos = get_youtube_playlist_videos(service, args.playlist_id, None, [])
   
    if(playlist_videos):
        downloaded_video_paths = download_multiple_youtube_videos(playlist_videos)
    
    for video_path in downloaded_video_paths:
        print(video_path)

if __name__ == "__main__":
    exit(main())
