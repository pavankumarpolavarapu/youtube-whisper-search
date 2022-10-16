# youtube_whisper_search

Implementing keyword search on youtube video playlists using whisper


# How to use

create .env file with developer_key=[key], you can get one from [Google Developer](https://developers.google.com/maps/documentation/javascript/get-api-key)

```
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
source .env
python get_playlist_videos.py [playlist_id]
python get_videos_transcribed.py
python search.py [search_phrase]
```

ripgrep is another useful tool, you can execute

```
rg [search_phrase]
```
