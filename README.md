# YouTube Whisper Search

Implementing keyword search on YouTube video playlists using OpenAI's Whisper transcriptions.

## Features
-   **Download Playlist Data:** Fetch video IDs and titles from a YouTube playlist.
-   **Download Videos:** Download audio/video from the playlist for processing.
-   **Transcribe:** Use OpenAI's Whisper model to convert audio to text.
-   **Search:** Perform keyword searches across all transcribed videos with timestamped links.

## Prerequisites
-   **Python:** 3.12+
-   **[uv](https://github.com/astral-sh/uv):** For fast and modern dependency management.
-   **FFmpeg:** Required by `whisper` and `yt-dlp` for media processing.
-   **YouTube Data API Key:** Get one from the [Google Developers Console](https://console.cloud.google.com/).

## Setup
1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd youtube-whisper-search
    ```

2.  **Configure environment variables:**
    Create a `.env` file in the root directory:
    ```text
    developer_key=YOUR_GOOGLE_API_KEY
    ```

3.  **Install dependencies:**
    Using `uv`, this will automatically create a virtual environment and install all required packages:
    ```bash
    uv sync
    ```

## Usage

### 1. Download Playlist Videos
Fetch and download videos from a specific YouTube playlist.
```bash
uv run python get_playlist_videos.py --playlist_id [PLAYLIST_ID]
```
*Options:*
- `--list_videos`: Only list the video URLs without downloading.
- `--no_download`: Skip downloading the video files.

### 2. Transcribe Videos
Convert all downloaded videos in the `videos/` folder into text transcripts.
```bash
uv run python get_videos_transcribed.py
```
*Note: This will use the "base" Whisper model by default. Transcripts are saved in the `transcribed/` folder.*

### 3. Search Transcripts
Search for keywords or phrases across all generated transcripts.
```bash
uv run python search.py "your search phrase"
```
*The output will include clickable YouTube links with the correct video ID and the context of the match.*

### Alternative Search (Using ripgrep)
If you have `ripgrep` installed, you can search the text files directly:
```bash
rg "search phrase" transcribed/ -g "*.txt"
```

## Development
-   **Update dependencies:** `uv lock --upgrade && uv sync`
-   **Add new dependency:** `uv add <package>`
-   **Remove dependency:** `uv remove <package>`
