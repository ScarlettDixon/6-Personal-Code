import os
import sys
from argparse import ArgumentParser
from PyQt6.QtWidgets import (
    QApplication)
import gui
import youtube_download
#import requests
#from tinytag import TinyTag
#import music_tag
#from moviepy.editor import *
#from pyyoutube import Api

#Argument parsing
if __name__ == '__main__':
    print("---Scarlett's Youtube Downloader---")
    parser = ArgumentParser("Youtube Video Downloader")
    parser.add_argument('-a', '--audioconvert', type=str, help="Give a path + name of any MP4 youtube video already downloaded and convert to MP3.")
    parser.add_argument('-e','--errorfile', type=str, help="Enter the location of a previously generated error file to be loaded and downloading re-attempted.")
    parser.add_argument('-f','--filelocation', type=str, default="Downloads", help="Location where would you like the files saved to.")
    parser.add_argument('-g','--gui', type=bool, help="Starts the graphical user interface")
    parser.add_argument('-i', '--includeauth', type=bool, default=False, help="Currently issues occur with Youtube needing authentication to work, this setting makes it so authentication takes place. Alternatives coming soon.")
    parser.add_argument('-l','--link', type=str, help="Enter the url of the video you want to download.")
    parser.add_argument('-o','--outputerrorlocation', type=str, default="Outputs", help="Location where would you like the csv with details of any videos that failed to download.")
    parser.add_argument('-p','--playlistlink', type=str, help="Enter the url of the playlist you want to download.")
    parser.add_argument('-v', '--video', type=bool, default=False, help="Allows for download without conversion to audio only.")
    args = parser.parse_args()
    #GuiMain() #Possible GUI interface in future
    if (args.gui):
        app = QApplication(sys.argv)
        # create the main window
        window = gui.MainWindow()
        # start the event loop
        sys.exit(app.exec())
    else:
        Project=youtube_download.Media(args)
        del Project


"""
Using the code:
pyenv install 3.7.0 - install older version of python
pyenv local 3.7.0 - switch to it
python3 -m venv venv
source venv/bin/activate - Starting venv
pip install <PackageName>
pip install -r requirements.txt
pip install -r requirements.txt --upgrade
Issues can be caused by none up to date packages, stop this by doing the following:
python -m pip install --upgrade pytube & python -m pip install --upgrade pip
python3 -m pip list --format=freeze > requirements.txt
python -m pip cache remove <Pattern>
deactivate


print(f'---Ingesting single video url---')
    print(args.link)
    video = YouTube(args.link)
    #Title of video
    print("Title: ",video.title)
    #URL of thumbnail
    print("Thumbnail: ",video.thumbnail_url)
    #Number of views of video
    print("Number of views: ",video.views)
    #Length of the video
    print("Length of video: ",video.length,"seconds")
    #Description of video
    print("Description: ",video.description)
    #Rating
    print("Ratings: ",video.rating)
    #printing all the available streams
    #print(f'---Streams---')
    #print(video.streams)

    try:
            audio.add_tags()
        except error:
            pass
        meta = mutagen.File(video_out, easy=True)
        meta.delete()
        meta.save(audio_out, v1=2)
        print(f"metadata: {meta}")


tags["TIT2"] = TIT2(encoding=3, text=title)
tags["TALB"] = TALB(encoding=3, text=u'mutagen Album Name')
tags["TPE2"] = TPE2(encoding=3, text=u'mutagen Band')
tags["COMM"] = COMM(encoding=3, lang=u'eng', desc='desc', text=u'mutagen comment')
tags["TPE1"] = TPE1(encoding=3, text=u'mutagen Artist')
tags["TCOM"] = TCOM(encoding=3, text=u'mutagen Composer')
tags["TCON"] = TCON(encoding=3, text=u'mutagen Genre')
tags["TDRC"] = TDRC(encoding=3, text=u'2010')
tags["TRCK"] = TRCK(encoding=3, text=u'track_number')

"""