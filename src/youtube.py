from pytube import YouTube
import moviepy.editor
import asyncio
url = YouTube(url='https://www.youtube.com/watch?v=t5Bo1Je9EmE')
video_streams = url.streams.filter(progressive=True, type='video')
audio_streams = url.streams.filter(type='audio').order_by('abr')
audio_dict = {}
# sort video resolution
for video in video_streams:
    print(
        f'{video.resolution} (.{video.mime_type[6:]}), {video.filesize_mb:.1f}')
for audio in audio_streams:
    print(f'{audio.abr} (.mp3), {audio.filesize_mb:.1f}')
    audio_dict.update([(audio.abr,audio.itag)])
print(audio_dict)
