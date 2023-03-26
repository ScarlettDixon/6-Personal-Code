import os
from pytube import YouTube, Playlist
from argparse import ArgumentParser
import urllib
from mutagen.id3 import ID3, TPE1, TIT2, TRCK, TALB, APIC
from csv import writer
#import requests
#from tinytag import TinyTag
#import music_tag
#from moviepy.editor import *
#from pyyoutube import Api

class Video:
    def __init__ (self,link, fileoutputlocation):
        self.link = link
        self.filelocation = fileoutputlocation
        self.currentFailed = []
        self.error = ""
        self.video = YouTube(link)
        self.GetDetails()
        self.Link()
    def GetDetails(self):
        try:
            self.title = self.video.title
            print(f'-------Downloading {self.title}-----------')
            self.author = self.video.author
            self.thumbnail = self.video.thumbnail_url
            self.description = self.video.description
        except Exception as e:
            self.error = "Failed to gather details - " + f"{e}"
            print(self.error)
            self.currentFailed = [self.link,'' ,'', self.error]
            return
    def Link(self):
        print(f'-------Audio Only Streams-----------')
        try:
            audiostream=self.video.streams.filter(only_audio=True).first()
            tag = audiostream.itag
            #print(audiostream.itag)
            chosendownload = self.video.streams.get_by_itag(tag)
            VideoOut = chosendownload.download(self.filelocation)
            print(f'-------Download Successful-----------')
            if(VideoOut):
                VideoOut = self.AudioConvert(VideoOut)
        except Exception as e:
            self.error = "No Audio Streams Detected, Skipping - " + f"{e}"
            print(self.error)
            if not (self.currentFailed):
                self.currentFailed = [self.link, self.title ,self.author, self.error]
        
    def AudioConvert(self, VideoOut):
        try:
            print(f'-------Converting to MP3-----------')
            base, ext = os.path.splitext(VideoOut)
            #print(f'{base} and {ext}')
            Oldfile = base + '.mp4'
            NewFile = base + '.mp3'
            os.system(f'ffmpeg -vn -sn -dn -i "{Oldfile}" -codec:a libmp3lame -qscale:a 4 "{NewFile}" 2>/dev/null 1>/dev/null')
            #ffmpeg -vn -sn -dn -i input.mp4 -codec:a libmp3lame -qscale:a 4 output.mp3
            #os.rename(VideoOut, NewFile)
            os.remove(VideoOut)
            print(f'-------Convertion Successful-----------')
            self.MetadataAddition(NewFile)
        except Exception as e:
            self.error = "Failed audio conversion - " + f"{e}"
            print(self.error)
            if not (self.currentFailed):
                self.currentFailed = [self.link, self.title ,self.author, self.error]
            return VideoOut
        
    def MetadataAddition(self, AudioOut):
        print(f'-------Adding Metadata-----------')
        audio = ID3(AudioOut)
        try:
            #print(f"1: {audio}")
            audio['TPE1'] = TPE1(encoding=3, text=self.author) #Artist
            audio['TIT2'] = TIT2(encoding=3, text=self.title) #Title
            audio['TALB'] = TALB(encoding=3, text=self.title)#Album Title
            albumart = urllib.request.urlopen(f'{self.thumbnail}')
            #print(f"{albumart}")
            audio['APIC'] = APIC(
                  encoding=3,
                  mime='image/jpeg',
                  type=3,
                  desc=u'Cover',
                  data=albumart.read()
                )
            audio.save()
            print(f'-------Metadata Added-----------')
        except Exception as e:
            self.error = "Failed Metadata Addition - " + f"{e}"
            print(self.error)
            if not (self.currentFailed):
                self.currentFailed = [self.link, self.title ,self.author, self.error]
        #print(f"2: {audio}")
    

def PlayList(args):
    print(f'-------Ingesting playlist url-----------')
    playlist = Playlist(args.playlistlink)
    failed = []
    for videourls in playlist:
        print(videourls)
        CurrentVideo = Video(videourls, args.filelocation)
        if (CurrentVideo.currentFailed):
            failed.append(CurrentVideo.currentFailed)
            print(f'{CurrentVideo.currentFailed}')
        del CurrentVideo
    print(f'-------Playlist Injestion Succesfull-----------')
    if (failed):
        outputPath: str = getattr(args, 'filelocation')
        FailedWrite(failed, outputPath)

    #https://www.youtube.com/playlist?list=PLYp8CYBmmepGysjynkun2OOVTWrux-m2s

def FailedWrite(failed, outputPath):
    header = []
    if not header:
        header = ["Link", "VideoName", "Artist/Channel", "Latest Error"]
    output = outputPath + "/output.csv"
    print(f"output: {output}")
    with open (output, 'w', newline='') as csvfile:
        failedWriter= writer(csvfile)
        failedWriter.writerow(header)
        failedWriter.writerows(failed)


if __name__ == '__main__':
    print("Scarlett's Youtube Downloader")
    parser = ArgumentParser("Youtube Video Downloader")
    parser.add_argument('-l','--link', type=str, help="Enter the url of the video you want to download ")
    parser.add_argument('-p','--playlistlink', type=str, help="Enter the url of the playlist] you want to download ")
    parser.add_argument('-f','--filelocation', type=str, default=".", help="Location where would you like the files saved to")
    parser.add_argument('-a', '--audioconvert', type=str, help="Give a path + name of any MP4 youtube video already downloaded and convert to MP3")
    args = parser.parse_args()
    #GuiMain()
    if (args.link):
        V1 = Video(args.link, args.filelocation)
        del V1
    elif (args.playlistlink):
        PlayList(args)
    elif (args.audioconvert):
        AudioConvert(args.audioconvert)
    else:
        print("must have either a link to one video or playlist")


"""
Useful Links:
https://pytube3.readthedocs.io/en/latest/
https://towardsdatascience.com/build-a-youtube-downloader-with-python-8ef2e6915d97
https://www.geeksforgeeks.org/download-youtube-videos-or-whole-playlist-with-python/
https://github.com/willwen/Python-Music-Metadata-Fetcher
https://stackoverflow.com/questions/4040605/does-anyone-have-good-examples-of-using-mutagen-to-write-to-files


Using the code:
pyenv install 3.7.0 - install older version of python
pyenv local 3.7.0 - switch to it
python3 -m venv venv
source venv/bin/activate - Starting venv
pip install <PackageName>
pip install -r requirements.txt
python3 -m pip list --format=freeze > requirements.txt
python -m pip cache remove <Pattern>
deactivate


print(f'-------Ingesting single video url-----------')
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
    #print(f'-------Streams-----------')
    #print(video.streams)

    try:
            audio.add_tags()
        except error:
            pass
        meta = mutagen.File(VideoOut, easy=True)
        meta.delete()
        meta.save(AudioOut, v1=2)
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