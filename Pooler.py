import os
import time

import requests
import sys

# Define beatmap mirror | If you replace this, please include "/" at the end.
mirror = "https://kitsu.moe/d/"

def check_download_txt():
    txt_path = os.path.join(os.getcwd(), "download.txt")
    return os.path.exists(txt_path)


def ensure_download_txt():
    # Create empty Download.txt if needed
    if not check_download_txt():
        create_download_txt()
        print("download.txt was missing and has been created.")


def create_download_txt():
    with open("./download.txt", "w"):
        pass


def get_beatmaps(mapset_texts):

    mapsets = []
    map_count = 0
    success_count = 0

    # No arguments and download.txt was not found
    if len(mapset_texts) == 0:
        print("No mapset information provided. Edit the provided download.txt file or pass/"
              "files as arguments")
        ensure_download_txt()
        sys.exit(2)

    # Get beatmap IDs
    for file in mapset_texts:
        print(f"Reading maps from {file}")
        try:
            with open(file, "r") as f:
                lines = [line.strip() for line in f.read().splitlines()]
                mapsets.extend(lines)
        except Exception as e:
            print(f"File '{file}' could not be opened.")
            #print(e)

    # Check output directory exists
    new_dir = os.getcwd() + "\\Maps\\"
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    # Assign file directory
    for mapset in mapsets:
        # Prevent ratelimit
        time.sleep(3)

        map_count += 1
        dl_path = new_dir + f"{mapset}.osz"
        # TODO - CHeck if the map already exists and skip download if so
        # Some maps could be in multiple lists

        print("Downloading Mapset ID: " + str(mapset))

        # Download beatmaps
        try:
            r = requests.get(mirror + mapset)
            # TODO - check response / see if ratelimited or beatmap not found and log it + no save
            with open(dl_path, "wb") as stream:
                stream.write(r.content)
            success_count += 1
        except Exception as e:
            print(e)

    print(f"Downloaded {success_count}/{map_count} mapsets.")


def interactive_input(mapset_list):
    print("""
           Welcome to Pooler! The automatic mappool downloader.
           Please make sure that you have included all of the correct mapset IDs in the download.txt file.
           """)

    while True:
        print("""Loaded map ID files: """, end='')

        for map in mapset_list:
            print(f"{map} ", end='')
        print('')

        print("""
                1 | Start map download
                2 | Quit
                """)

        selection = int(input("Please make a selection: "))

        if selection == 1:
            get_beatmaps(mapset_list)
        elif selection == 2:
            print("Thank you for using Pooler. Have a great day! :)")
            return
        else:
            print("Invalid selection, please try again.")

    # match(selection):
    #     case 1:
    #         getBeatmaps()
    #     case 2:
    #         print("Thank you for using Pooler. Have a great day! :)")
    #         time.wait(2)
    #         os.exit(1)
    #     case _:
    #         print("That wasn't a correct selection, please try again.")

if __name__ == "__main__":

    arg_count = len(sys.argv)
    args_processed = 1
    interactive = True
    custom_files = False
    mapset_list = []

    # TODO - make this arg parsing better

    # If we have args
    if (arg_count > 1):

        # Interactive mode flag
        if sys.argv[1] == "-ni":
            interactive = False
            args_processed += 1

        # Some args left, so assume they are input files
        if arg_count > args_processed:
            # Make map file list
            for i in range(args_processed, len(sys.argv)):
                mapset_list.append(sys.argv[i])


    if len(mapset_list) == 0:
        # Didn't specify any map file. Check for download.txt
        txt_exists = check_download_txt()
        if txt_exists:
            print("Found existing 'download.txt'")
            mapset_list.append("download.txt")


    # Switch behavior on if the program is interactive (-i flag)
    if interactive:
        interactive_input(mapset_list)
    else:
        get_beatmaps(mapset_list)

    sys.exit(1)

