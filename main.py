import os
import argparse
import settings_lib
import colorama
from ripper import Ripper
import helper
import caffeine

VERSION = "2025-04-23"
DRYRUN = False

current_path = helper.get_current_path()


def main():
    colorama.init()
    if not os.environ.get('PYTHONIOENCODING'):
        os.environ['PYTHONIOENCODING'] = str("utf-8")

    # Load settings
    settings = settings_lib.load_settings()

    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="Record music from Spotify as MP3 files.")
    parser.add_argument('link', type=str,
                        help='Link to the resource to be recorded. It can be a track, an album (*), an artist (*) or,'
                             ' a playlist (*) uri or url, as well as a .txt file containing a list of those. '
                             'Note (*): requires env variables SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET set.'
                        )
    parser.add_argument('-s', '--start_from', type=int, default=1,
                        help='In case of a link containing more than one track, from which track of the list to start. '
                             'The first is 1.'
                        )

    # Parse arguments
    args = parser.parse_args()
    tracks, _ = helper.parse_input(args.link, args.start_from - 1)

    print("Ripping {} track{}.".format(len(tracks), "s" if len(tracks) > 1 else ""))
    for track in tracks:
        if not DRYRUN:
            ripper = Ripper(current_path=current_path,
                            rip_dir=settings["rip_dir"],
                            ripped_folder_structure=settings["ripped_folder_structure"])
            ripper.rip(helper.convert_to_uri(track.rstrip()))
        else:
            print(track)
    return


if __name__ == "__main__":
    if not os.path.exists(os.path.join(current_path, "settings.json")):
        settings_lib.create_settings()
    caffeine.on(display=False)  # Keeps system awake, allows display to sleep
    main()
    caffeine.off()  # Release the assertion before exiting

