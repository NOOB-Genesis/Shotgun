#!/usr/bin/python
# TODO:
#   - Failsafes
#   - Action Menu Integration
#   - Logging (Shotgun Side)
#   - Path specification
#       - Currently gets default path of desktop and creates a general folder and playlist specific folder
#   - Optional Name Conventions
#       - Currently keeps names as they are in the playlist
#   - Optimizations

import os, sys
# Import the Shotgun software API
import shotgun_api3
# Import PrettyPrint
from pprint import pprint


# This is to get a default save location to the desktop
# Uncomment if on OSX
# desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
# Uncomment if on Windows
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 

# Server details and authentication
SERVER_URL = "https://noobxgenesis.shotgunstudio.com"
SCRIPT_NAME = "Pull Playlist"
API_KEY = "4de7568c48239687deadba1478377889f312f87d13784701606a433a5752bc30"

class Pull():

    # Assign all commands via script based authentication to sg variable
    sg = shotgun_api3.Shotgun(SERVER_URL, SCRIPT_NAME, API_KEY)

    # Specify playlist
    #   - Possibly handle by ID rather than name - this also means all concatenations will be off in both prints and paths
    playlist_name = raw_input("Enter Playlist Name: ")
    # Create List of Versions within playlist_name
    versions = sg.find("Version", [["playlists", "name_is", playlist_name]])

    # Get Count of Versions within playlist_name to prepare for Iteration Loop
    vCount = len(versions)
    # LOG
    pprint("Number of Versions in " + playlist_name + ": " + str(vCount))

    # Define path to save downloaded images
    #path = raw_input("Enter filepath to download images to: ")

    # Loop through each Version within playlistName
    for x in range(0, vCount):
        # LOG
        #pprint(versions[x]["id"])
        # Simplify ID collection by assigning it to a variable
        versionID = versions[x]["id"]
        # Grab the version and it's details pertaining to the Attachment for download
        #   - Need to look deeper into how this works fully and what limits I can push
        versionToDownload = sg.find_one("Version", [["id", "is", versionID]], ['sg_uploaded_movie'])
        # LOG
        #pprint(versionToDownload)
        
        # Path and Filename to save the file to
        # Checks to see if the desktop based path (folder structure) exists
        if os.path.exists(desktop + "\Downloaded Playlist\\" + playlist_name):
            # If the path exists, it creates the naming convention for the image to be downloaded and assigns it to a variable
            local_file_path = desktop + "\Downloaded Playlist\\" + playlist_name + "\%s" % versionToDownload["sg_uploaded_movie"]["name"]
        else:
            # If the path does not exist, it creates both a general folder for all playlists, and a playlist specific one
            os.makedirs(desktop + "\Downloaded Playlist\\" + playlist_name)
            # Then it creates the naming convention for the image to be downloaded and assigns it to a variable
            local_file_path = desktop + "\Downloaded Playlist\\" + playlist_name + "\%s" % versionToDownload["sg_uploaded_movie"]["name"]
            
        # The actual download and save function
        sg.download_attachment(versionToDownload['sg_uploaded_movie'], file_path=local_file_path)
        print("Downloaded: " + str(x + 1) + "/" + str(vCount))

    print("Complete!")
    raw_input("Press Enter key to exit.")
    
if __name__ == "__main__":

    try:
        pull = Pull()
    except Exception:
        print("Error")
