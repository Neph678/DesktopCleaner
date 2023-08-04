from os import getlogin, scandir, rename
from os.path import exists, join, splitext
from shutil import move
import logging
import timeit


img_extensions = [".jpg", ".jpeg", ".png", ".tiff"]
video_extensions = [".mp4", ".mov"]
audio_extensions = [".mp3", ".wav"]

username = getlogin()

source_dir = "/Users/"+username+"/Desktop"
img_dir = "/Users/"+username+"/Pictures"
video_dir = "/Users/"+username+"/Videos"
audio_dir = "/Users/"+username+"/Music"


def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # If file exists then counter is added to end of the filename
    while exists(f"{dest}\{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name


def move_file(dest, file):
    if exists(f"{dest}\{file.name}"):
        oldName = join(dest, file.name)
        newName = join(dest, make_unique(dest, file.name))
        rename(oldName, newName)
        logger.info(
            f"\"{file.name}\" already exists at {dest}. Renaming file from \"{oldName}\" to \"{newName}\"")
    move(file, dest)
    logger.info(
        f"\"{file.name}\" has successfully moved to \"{dest}/{file.name}\"")


def check_image_files(file):
    for extension in img_extensions:
        if file.name.endswith(extension):
            move_file(img_dir, file)


def check_video_files(file):
    for extension in video_extensions:
        if file.name.endswith(".webm"):
            # moving webm extensions to their own folder
            move_file(video_dir + "/Webm", file)
        elif file.name.endswith(extension):
            move_file(video_dir, file)


def check_audio_files(file):
    for extension in audio_extensions:
        if file.name.endswith(extension):
            move_file(audio_dir, file)


def clean_directory(target_dir):
    with scandir(target_dir) as files:
        for file in files:
            check_image_files(file)
            check_video_files(file)
            check_audio_files(file)


if __name__ == "__main__":
    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    logger.info("Booting up program...")
    runtime = timeit.timeit(lambda: clean_directory(source_dir), number=1)
    logger.info(f"Finished in{runtime: .6f} seconds.")
    logger.info("Done!")
