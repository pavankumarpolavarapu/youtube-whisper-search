from __future__ import annotations

import argparse
import os
from collections.abc import Sequence
from pathlib import Path

import googleapiclient.discovery
import googleapiclient.errors
import yt_dlp
from dotenv import load_dotenv

from logger import MyLogger

scopes = ['https://www.googleapis.com/auth/youtube.readonly']


def download_multiple_youtube_videos(
    playlist: str,
    playlist_videos: list[list[str]],
) -> list[str]:
    downloaded_video_paths = []
    try:
        for item in playlist_videos:
            file_path = f"{os.getcwd()}/videos/{playlist}/{item[0]}.mp4"
            Path(os.path.dirname(file_path)).mkdir(parents=True, exist_ok=True)
            if not os.path.isfile(file_path):
                try:
                    if (download_single_youtube_video(item[1], file_path)):
                        downloaded_video_paths.append(file_path)
                except yt_dlp.DownloadError:
                    print(f"Error while downloading {item[1]}")
    except Exception:
        print('An exception occurred while downloading videos')
        raise

    return downloaded_video_paths


def download_single_youtube_video(url: str, file_path: str) -> str:
    """Save a YouTube video URL to mp3.

    Args:
        url (str): A YouTube video URL.

    Returns:
        str: The filename of the mp3 file.
    """

    options = {
        'format': 'mp4/bestvideo*+bestaudio/best',
        'outtmpl': file_path,
        'logger': MyLogger(),
    }

    try:
        with yt_dlp.YoutubeDL(options) as downloader:
            downloader.download(['' + url + ''])
    except Exception:
        raise

    return file_path


def get_google_api_client(
    api_service_name: str,
    api_version: str,
    developer_key: str | None,
) -> object:
    service = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=developer_key,
    )

    return service


def get_youtube_playlist_videos(
    service: object,
    playlist: str,
    page_token: str | None,
    playlist_videos: list[list[str]],
) -> list[list[str]]:
    # type: ignore
    request = service.playlistItems().list(
        part='snippet,contentDetails',
        maxResults=50,
        playlistId=playlist,
        pageToken=page_token,
    )

    response = request.execute()

    for item in response['items']:
        videoId: str = item['contentDetails']['videoId']
        youtube_url = f"https://youtube.com/watch?v={videoId}"

        playlist_videos.append([videoId, youtube_url])

    if 'nextPageToken' in response.keys():
        playlist_videos = \
            get_youtube_playlist_videos(
                service, playlist,
                response['nextPageToken'],
                playlist_videos,
            )

    return playlist_videos


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('playlist_id')
    load_dotenv()
    developer_key = os.getenv('developer_key')
    args = parser.parse_args(argv)

    api_service_name = 'youtube'
    api_version = 'v3'

    service = \
        get_google_api_client(api_service_name, api_version, developer_key)

    if (service):
        playlist_videos = \
            get_youtube_playlist_videos(service, args.playlist_id, None, [])

    if (playlist_videos):
        downloaded_video_paths = \
            download_multiple_youtube_videos(args.playlist_id, playlist_videos)

    for video_path in downloaded_video_paths:
        print(video_path)

    return 0


if __name__ == '__main__':
    exit(main())
