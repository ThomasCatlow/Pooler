import os, requests, time, shutil

# Define beatmap mirror | If you replace this, please include "/" at the end.
mirror = "https://kitsu.moe/d/"

# Generate Download.txt
txtCheck = os.path.join(os.getcwd(), "download.txt")
if not os.path.exists(txtCheck):
    with open("./download.txt", "w"): pass

def getBeatmaps():

    try:   
        # Get list of beatmap IDs
        mapsets = []
        with open("download.txt", "r") as f:
            lines = [line.strip() for line in f.read().splitlines()]
            mapsets.extend(lines)

        # Check directory exists
        newDir = os.getcwd() + "\\Maps\\"
        if not os.path.exists(newDir):
            os.makedirs(newDir)

        # Assign file directory
        for mapset in mapsets:
            dl_path = newDir + f"{mapset}.osz"
    
            # Download beatmaps
            r = requests.get(mirror + mapset)
            with open(dl_path, "wb") as stream:
                stream.write(r.content)
            print("Downloading Mapset ID: " + str(mapset))
    except Exception as e:
        print("Something went wrong: " + e)



# Main function

print("""
Welcome to Pooler! The automatic mappool downloader.
Please make sure that you have included all of the correct mapset IDs in the download.txt file.

1 | Start map download
2 | Quit
""")

selection = int(input("Please make a selection: "))

match(selection):
    case 1:
        getBeatmaps()
    case 2:
        print("Thank you for using Pooler. Have a great day! :)")
        time.wait(2)
        os.exit(1)
    case _:
        print("That wasn't a correct selection, please try again.")
