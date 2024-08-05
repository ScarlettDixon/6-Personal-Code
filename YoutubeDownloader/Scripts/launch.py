import os
from pytube import YouTube, Playlist
from argparse import ArgumentParser
import urllib
from mutagen.id3 import ID3, TPE1, TIT2, TRCK, TALB, APIC
from csv import writer, reader, DictReader
from datetime import datetime
#import requests
#from tinytag import TinyTag
#import music_tag
#from moviepy.editor import *
#from pyyoutube import Api

class Video:
    #Initialiser of Video class
    def __init__ (self, link, output_file_location, auth):
        self.link = link
        self.file_location = output_file_location
        self.current_failed = []
        self.error = ""
        if auth:
            self.video = YouTube(link, use_oauth=True, allow_oauth_cache=True)
        else:
            self.video = YouTube(link)
        self.get_details()
    #Attempts to gather the information necessary for successful download and later conversion
    def get_details(self):
        try:
            self.title = self.video.title
            print(f'---Downloading {self.title}---')
            self.author = self.video.author
            self.description = self.video.description
            try:
                self.thumbnail = self.video.thumbnail_url 
            except Exception as e:
                self.error = "Error: Failed to gather thumbnail - " + f"{e}"
                print(self.error)
                self.current_failed = [self.link,'' ,'', self.error]
            self.link()
        except Exception as e:
            self.error = "Error: Failed to gather details - " + f"{e}"
            print(self.error)
            self.current_failed = [self.link,'' ,'', self.error]
            return
    #Processing each individual link
    def link(self):
        print(f'---Audio Only Streams---')
        try:
            audio_stream=self.video.streams.filter(only_audio=True).first()
            tag = audio_stream.itag
            #print(audio_stream.itag)
            chosen_download = self.video.streams.get_by_itag(tag)
            video_out = chosen_download.download(self.file_location)
            print(f'---Download Successful---')
            if(video_out):
                video_out = self.audio_convert(video_out)
        except Exception as e:
            self.error = "Error: No Audio Streams Detected, Skipping - " + f"{e}"
            print(self.error)
            if not (self.current_failed):
                self.current_failed = [self.link, self.title ,self.author, self.error]
    #Converting from MP3 to MP4, both in file and metadata    
    def audio_convert(self, video_out):
        try:
            print(f'---Converting to MP3---')
            base, ext = os.path.splitext(video_out)
            #print(f'{base} and {ext}')
            old_file = base + '.mp4'
            new_file = base + '.mp3'
            if (os.path.isfile(new_file)): #Ensures that issues don't occur when two mp3s exist in the same space with the same name
                print(f"Information: File already exists, skipping")
                os.remove(video_out)
            else:
                os.system(f'ffmpeg -vn -sn -dn -i "{old_file}" -codec:a libmp3lame -qscale:a 4 "{new_file}" 2>/dev/null 1>/dev/null')
                #ffmpeg -vn -sn -dn -i input.mp4 -codec:a libmp3lame -qscale:a 4 output.mp3
                #os.rename(video_out, new_file)
                os.remove(video_out)
                print(f'---Convertion Successful---')
                self.metadata_addition(new_file)
                
        except Exception as e:
            self.error = "Failed audio conversion - " + f"{e}"
            print(self.error)
            if not (self.current_failed):
                self.current_failed = [self.link, self.title ,self.author, self.error]
            return video_out
    #Using mutagen to add the MP3 metadata
    def metadata_addition(self, audio_out):
        print(f'---Adding Metadata---')
        audio = ID3(audio_out)
        try:
            #print(f"1: {audio}")
            audio['TPE1'] = TPE1(encoding=3, text=self.author) #Artist
            audio['TIT2'] = TIT2(encoding=3, text=self.title) #Title
            audio['TALB'] = TALB(encoding=3, text=self.title)#Album Title
            album_art = urllib.request.urlopen(f'{self.thumbnail}')
            #print(f"{album_art}")
            audio['APIC'] = APIC(
                encoding=3,
                mime='image/jpeg',
                type=3,
                desc=u'Cover',
                data=album_art.read()
                )
            audio.save()
            print(f'---Metadata Added---')
        except Exception as e:
            self.error = "Error: Failed Metadata Addition - " + f"{e}"
            print(self.error)
            if not (self.current_failed):
                self.current_failed = [self.link, self.title ,self.author, self.error]
        #print(f"2: {audio}")
    
#Separate function to deal with playlists (many succesive links)
def playlist(args):
    print(f'---Ingesting playlist url---')
    playlist = Playlist(args.playlistlink)
    failed = []
    print(playlist.title)
    if (playlist): #Some issues can occur when youtube changes its access and encoding
        for video_number, video_url in enumerate(playlist):
            print(video_url)
            current_video = Video(video_url, args.filelocation, args.includeauth)
            if (current_video.current_failed):
                current_video.current_failed.insert(0,video_number)
                failed.append(current_video.current_failed)
                print(f'{current_video.current_failed}')
            del current_video
        print(f'---Playlist Injestion Succesfull---')
    else:
        print("Error: Either playlist is empty or a different error has occurred")
    if (failed):
        print("Error: Some urls failed to download, they will now be stored for ease of re-download")
        output_path: str = getattr(args, 'outputerrorlocation')
        failed_write(failed, output_path)

def error_file(input_error_path, output_file_location, output_error_location, include_auth):
    failed = []
    with open (input_error_path, 'r', newline='') as csv_file:
        error_reader = DictReader(csv_file)
        for video_number, row in enumerate(error_reader):
            print(f"URL: {row['Link']}")
            print(f"Video Name: {row['VideoName']}")
            print(f"Artist/Channel: {row['Artist/Channel']}")
            print(f"Current Error: {row['Latest Error']}")
            current_error_video = Video(row['Link'], output_file_location, include_auth)
            if (current_error_video.current_failed):
                current_error_video.current_failed.insert(0,video_number)
                failed.append(current_error_video.current_failed)
                print(f'New Error Entry: {current_error_video.current_failed}')
            del current_error_video
        print(f'---Playlist Injestion Succesfull---')

    if (failed):
        print("Error: Some urls failed to download, they will now be stored for ease of re-download")
        failed_write(failed, output_error_location)

#Created in the event of failure in any area of the playlist script as it may contain many videos and allows a user to manually go back through and fix these issues
def failed_write(failed, output_path):
    header = []
    if not header:
        header = ["Index","Link","VideoName", "Artist/Channel", "Latest Error"]
    date_today=datetime.today().strftime('%Y-%m-%d')
    output = output_path + f"/erroroutput-{date_today}.csv"
    print(f"Output File Name: {output}")
    with open (output, 'w', newline='') as csv_file:
        failedWriter= writer(csv_file)
        failedWriter.writerow(header)
        failedWriter.writerows(failed)

#Argument parsing
if __name__ == '__main__':
    print("---Scarlett's Youtube Downloader---")
    parser = ArgumentParser("Youtube Video Downloader")
    parser.add_argument('-l','--link', type=str, help="Enter the url of the video you want to download.")
    parser.add_argument('-p','--playlistlink', type=str, help="Enter the url of the playlist you want to download.")
    parser.add_argument('-e','--errorfile', type=str, help="Enter the location of a previously generated error file to be loaded and downloading re-attempted.")
    parser.add_argument('-f','--filelocation', type=str, default="Downloads", help="Location where would you like the files saved to.")
    parser.add_argument('-o','--outputerrorlocation', type=str, default="Outputs", help="Location where would you like the csv with details of any videos that failed to download.")
    parser.add_argument('-a', '--audioconvert', type=str, help="Give a path + name of any MP4 youtube video already downloaded and convert to MP3.")
    parser.add_argument('-i', '--includeauth', type=bool, default=False, help="Currently issues occur with Youtube needing authentication to work, this setting makes it so authentication takes place. Alternatives coming soon.")
    args = parser.parse_args()
    #GuiMain() #Possible GUI interface in future
    if (args.link):
        V1 = Video(args.link, args.filelocation, args.includeauth)
        del V1
    elif (args.playlistlink):
        playlist(args)
    elif (args.audioconvert):
        audio_convert(args.audioconvert)
    elif (args.errorfile):
        error_file(args.errorfile, args.filelocation, args.outputerrorlocation, args.includeauth)
    else:
        print("Warning: Please provide either a link to one video or playlist using the -l or -p tags respectively. Use -h for more help")


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