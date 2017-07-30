# TODO:
#   - Failsafes
#   - Action Menu Integration
#   - Logging
#   - Path specification
#   - Optional Name Conventions
#   - Commenting
#   - Optimizations

# Import the Shotgun software API
import shotgun_api3
# Import PrettyPrint
from pprint import pprint

# Server details and authentication
SERVER_URL = "https://noobxgenesis.shotgunstudio.com"
SCRIPT_NAME = "Pull Playlist"
API_KEY = "4de7568c48239687deadba1478377889f312f87d13784701606a433a5752bc30"

if __name__ == "__main__":
    # Assign all commands via script based authentication to sg variable
    sg = shotgun_api3.Shotgun(SERVER_URL, SCRIPT_NAME, API_KEY)

    # Specify playlist
    #   - Possibly handle by ID rather than name
    playlistName = raw_input("Enter Playlist Name: ")

    # Create List of Versions within PlaylistName
    versions = sg.find("Version", [["playlists", "name_is", playlistName]])
    
    # Get Count of Versions within playlistName to prepare for Iteration Loop
    vCount = len(versions)
    # LOG
    pprint("Number of Versions in " + playlistName + ": " + str(vCount))

    # Define path to save downloaded images
    #path = raw_input("Enter filepath to download images to: ")

    # Loop through each Version within playlistName
    for x in range(0, vCount):
        # LOG
        pprint(versions[x]["id"])
        # Simplify ID collection by assigning it to a variable
        versionID = versions[x]["id"]
        # Grab the version and it's details pertaining to the Attachment for download
        #   - Need to look deeper into how this works fully and what limits I can push
        versionToDownload = sg.find_one("Version", [["id", "is", versionID]], ['sg_uploaded_movie'])
        # LOG
        pprint(versionToDownload)
        # Path and Filename to save the file to
        #   - Currently static path, need to make this path assignable by the user
        #   - Currently name is set to the name on Shotgun, may need more flexability in naming conventions
        local_file_path = "C:\Users\Jesse\Desktop\Python Testing\Shotgun\Playlist Download\%s" % versionToDownload["sg_uploaded_movie"]["name"]

        # The actual download and save function
        sg.download_attachment(versionToDownload['sg_uploaded_movie'], file_path=local_file_path)
