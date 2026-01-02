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
        print(f"An exception has occurred: {e}")
        return 1

    return 0


def main(*args: str) -> int:
    videos_folder = f"{os.getcwd()}/videos"
    transcribe_folder = f"{os.getcwd()}/transcribed"
    valid_extensions = ('.mp4', '.webm', '.mkv', '.avi', '.mov', '.flv')
    for root, dirs, files in os.walk(videos_folder):
        for file in files:
            if not file.lower().endswith(valid_extensions):
                continue
            video_file_path = os.path.join(root, file)
            rel_path = os.path.relpath(root, videos_folder)

            if rel_path == ".":
                target_dir = transcribe_folder
            else:
                target_dir = os.path.join(transcribe_folder, rel_path)

            os.makedirs(target_dir, exist_ok=True)

            file_name_without_ext = os.path.splitext(file)[0]
            transcribe_file_path = os.path.join(target_dir, f"{file_name_without_ext}.txt")

            transcribe_single_video(video_file_path, transcribe_file_path)


if __name__ == '__main__':
    SystemExit(main())
