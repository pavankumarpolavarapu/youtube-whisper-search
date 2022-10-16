import os
import argparse
from typing import Optional, Sequence

def link(uri, label=None) -> str:
    if label is None:
        label = uri
    parameters = ''

    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'

    return escape_mask.format(parameters, uri, label)

def search_file(file_path: str, file_name: str, search_phrase: str) -> None:

    video_id, _, _ = file_name.partition(".")
    youtube_url = link(f"https://youtube.com/watch?v={video_id}")

    print(f"Searching in {youtube_url}")

    with open(file_path, 'r') as f:
        searchlines = f.readlines()
    for i, line in enumerate(searchlines):
        if search_phrase in line: 
            for l in searchlines[i:i+3]: print (l),
            print


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('search_phrase')

    args = parser.parse_args(argv)

    transcribe_folder = f'{os.getcwd()}/transcribed'
    files_in_dir = os.listdir(transcribe_folder)

    for file in files_in_dir:
        search_file(os.path.join(transcribe_folder, file), file, args.search_phrase)




if __name__ == '__main__':
    SystemExit(main())

