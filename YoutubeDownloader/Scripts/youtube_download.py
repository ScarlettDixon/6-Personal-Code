from pytube import YouTube, Playlist
import urllib
from mutagen.id3 import ID3, TPE1, TIT2, TRCK, TALB, APIC
from csv import writer, reader, DictReader
from datetime import datetime

from pytube import cipher
import re
from pytube.innertube import _default_clients

_default_clients[ "ANDROID"][ "context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients[ "ANDROID_EMBED"][ "context"][ "client"]["clientVersion"] = "19.08.35"
_default_clients[ "IOS_EMBED"][ "context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_MUSIC"][ "context"]["client"]["clientVersion"] = "6.41"
_default_clients[ "ANDROID_MUSIC"] = _default_clients[ "ANDROID_CREATOR" ]

def get_throttling_function_name(js: str) -> str:
    """Extract the name of the function that computes the throttling parameter.

    :param str js:
        The contents of the base.js asset file.
    :rtype: str
    :returns:
        The name of the function used to compute the throttling parameter.
    """
    function_patterns = [
        r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&\s*'
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)',
    ]
    #logger.debug('Finding throttling function name')
    for pattern in function_patterns:
        regex = re.compile(pattern)
        function_match = regex.search(js)
        if function_match:
            #logger.debug("finished regex search, matched: %s", pattern)
            if len(function_match.groups()) == 1:
                return function_match.group(1)
            idx = function_match.group(2)
            if idx:
                idx = idx.strip("[]")
                array = re.search(
                    r'var {nfunc}\s*=\s*(\[.+?\]);'.format(
                        nfunc=re.escape(function_match.group(1))),
                    js
                )
                if array:
                    array = array.group(1).strip("[]").split(",")
                    array = [x.strip() for x in array]
                    return array[int(idx)]

    raise RegexMatchError(
        caller="get_throttling_function_name", pattern="multiple"
    )

cipher.get_throttling_function_name = get_throttling_function_name


class Media:
    def __init__ (self, args):
        if (args.link):
            V1 = Video(args.link, args.filelocation, args.includeauth, args.video)
            del V1
        elif (args.playlistlink):
            self.playlist(args)
        elif (args.audioconvert):
            self.audio_convert(args.audioconvert)
        elif (args.errorfile):
            self.error_file(args.errorfile, args.filelocation, args.outputerrorlocation, args.includeauth)
        else:
            print("Warning: Please provide either a link to one video or playlist using the -l or -p tags respectively. Use -h for more help")
    #Separate function to deal with playlists (many succesive links)
    def playlist(self, args):
        print(f'---Ingesting playlist url---')
        playlist = Playlist(args.playlistlink)
        failed = []
        print(playlist.title)
        if (playlist): #Some issues can occur when youtube changes its access and encoding
            for video_number, video_url in enumerate(playlist):
                print(video_url)
                current_video = Video(video_url, args.filelocation, args.includeauth, args.video)
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

    def error_file(self, input_error_path, output_file_location, output_error_location, include_auth):
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
    def failed_write(self, failed, output_path):
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


class Video:
    #Initialiser of Video class
    def __init__ (self, link, output_file_location, auth, videobool):
        self.link = link
        self.file_location = output_file_location
        self.current_failed = []
        self.error = ""
        self.videobool = videobool
        #print(self.videobool)
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
            self.process_link()
        except Exception as e:
            self.error = "Error: Failed to gather details - " + f"{e}"
            print(self.error)
            self.current_failed = [self.link,'' ,'', self.error]
            return
    #Processing each individual link
    def process_link(self):
        print(f'---Processing Link---')
        if (self.videobool):
            print(f'---Video Streams---')
            try:
                video_stream=self.video.streams.get_highest_resolution()
                tag = video_stream.itag
                #if (video_stream.captions):
                #    captions = video_stream.captions
                #print(audio_stream.itag)
                chosen_download = self.video.streams.get_by_itag(tag)
                video_out = chosen_download.download(self.file_location)
                print(f'---Download Successful---')
            except Exception as e:
                self.error = "Error: No Video Streams Detected, Skipping - " + f"{e}"
                print(self.error)
                if not (self.current_failed):
                    self.current_failed = [self.link, self.title ,self.author, self.error]
        else:
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


