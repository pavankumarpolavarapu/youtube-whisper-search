import os
import whisper

model = whisper.load_model("base")


def transcribe_single_video(video_file_path: str,
                            transcribe_file_path: str) -> int:
    global model
    try:
        print(f"transcribing {video_file_path}")
        if not os.path.isfile(transcribe_file_path):
            result = model.transcribe(video_file_path)

            with open(transcribe_file_path, 'w') as f:
                for segment in result["segments"]:
                    line = f"{segment['start']}:{segment['end']}\
                    {segment['text']}\n"
                    f.write(line)
        else:
            print(f"video already transcribed")

    except Exception as e:
        print("An exception has occurred")
        raise

    return 0


def main(*args: str) -> int:
    videos_folder = f"{os.getcwd()}/videos"
    transcribe_folder = f"{os.getcwd()}/transcribed"
    files_in_dir = os.listdir(videos_folder)

    for file in files_in_dir:
        video_file_path = os.path.join(videos_folder, file)
        videoId, _, _ = file.partition(".")
        transcribe_file_path = \
            os.path.join(transcribe_folder, f"{videoId}.txt")

        transcribe_single_video(video_file_path, transcribe_file_path)


if __name__ == '__main__':
    SystemExit(main())
