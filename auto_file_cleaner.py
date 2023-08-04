import os
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

img_extensions = [".jpg", ".jpeg", ".png", ".tiff"]
video_extensions = [".mp4", ".webm", ".mov"]
audio_extensions = [".mp3", ".wav"]

source_dir = "\Users\ephou\Desktop"
img_dir = "\Users\ephou\Pictures"
video_dir = "\Users\ephou\Videos"
audio_dir = "\Users\ephou\Music"

def type_of_file(filename):
        for extension in img_extensions:
            if filename.endswith(extension):
                return "image"
        for extension in video_extensions:
            if filename.endswith(extension):
                return "video"
        for extension in audio_extensions:
            if filename.endswith(extension):
                return "audio"

def move(dest, entry, name):
    file_exists = os.path.exists(dest + "/" + name)
    if file_exists:
        unique_name = makeUnique(name)
        os.rename(entry, unique_name)
    shutil.move(entry, dest)


class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                dest = source_dir
                if type_of_file(name) == "image":
                    dest = img_dir
                    move(dest, entry, name)
                elif type_of_file(name) == "video":
                    dest = video_dir
                    move(dest, entry, name)
                elif type_of_file(name) == "audio":
                    dest = audio_dir
                    move(dest, entry, name)






if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()