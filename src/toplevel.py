from pytube import YouTube
import asyncio
'''
https://youtu.be/17NLNg6v1qg
www.youtube.com/watch?v=oElol6JnT0w
https://www.youtube.com/watch?v=PITSYsAEjF0
'''
class Youtube(YouTube('https://youtu.be/17NLNg6v1qg')):
    '''Youtube Video Informations'''

    def __init__(self, **kwargs):
        super().__init__(Youtube.url)

        Youtube.url: str = 'https://youtu.be/17NLNg6v1qg'


    async def write(self):
        await Youtube.get_video_info(self)
        global streams_dict, audio_dict, video_dict
        streams_dict = {}
        video_dict = {}
        audio_dict = {}

        for video in video_streams:
            streams_dict.update(
                [(f'{video.resolution} (.{video.mime_type[6:]})            {video.filesize_mb:.1f} mb.', video.itag)])
            video_dict.update(
                [(f'{video.resolution} (.{video.mime_type[6:]})            {video.filesize_mb:.1f} mb.', video.itag)])
        for audio in audio_streams:
            if audio.mime_type[6:] == 'mp4':
                streams_dict.update([(f'{audio.abr} (.mp3)', audio.itag)])
                audio_dict.update([(f'{audio.abr} (.mp3)', audio.itag)])
        for i in streams_dict :
            print(i,streams_dict[i])
    async def get_video_info(self):
        global streams,video_title, video_views, video_channel, video_publish, video_streams, audio_streams, video_thumbnail_url, video_url
        video_url = self.url
        video_title = self.title
        video_views = self.views
        video_channel = self.author
        video_publish = self.publish_date.strftime("%Y-%m-%d, %A")
        video_streams = self.streams.filter(
            progressive=True, type='video')
        audio_streams = self.streams.filter(type='audio').order_by('abr')
        video_thumbnail_url = self.thumbnail_url
        streams = self.streams
asyncio.run(Youtube.get_video_info(self=Youtube()))
print(streams)