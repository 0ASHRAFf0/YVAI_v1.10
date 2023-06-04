import os
from Exc import Exc
import time
import asyncio
import threading
import webbrowser
import customtkinter as cust
from PIL import Image
from io import BytesIO
from pathlib import Path
from tkinter import messagebox
from pytube import YouTube
from requests import get
from moviepy.video.io.VideoFileClip import VideoFileClip
# -----------Main class--------------
'''
#344955
#232F34
#4A6572
#F9AA33
# '''

#https://youtu.be/17NLNg6v1qg
#www.youtube.com/watch?v=oElol6JnT0w
class Youtube(YouTube):
    '''Youtube Video Informations'''

    def __init__(self=None, **kwargs):
        super().__init__(Youtube.url)
        Youtube.url = ''

    async def write(self):
        await Youtube.get_video_info(self)
        global video_thumbnail,video_dict,audio_dict
        audio_dict = {}
        video_dict = {}

        for video in video_streams:
            video_dict.update(
                [(f'{video.resolution} (.{video.mime_type[6:]}), ', f'{video.filesize_mb:.1f}')])
        for audio in audio_streams:
            audio_dict.update([(audio.abr, audio.itag)])
        print(f'{video_title}\n{video_views}\n{video_channel}\n{video_length}\n{video_publish}\n')
        print(audio_dict)
        print(video_dict)
        print(audio_streams)
        thumbnail_response = get(video_thumbnail_url)
        video_thumbnail = Image.open(BytesIO(thumbnail_response.content))
        video_thumbnail.resize(size=(video_thumbnail.width//2,video_thumbnail.height//2),resample=Image.ANTIALIAS)
    async def get_video_info(self):
        global video_title, video_length, video_views, video_channel,video_publish, video_streams, audio_streams,video_thumbnail_url
        video_title = self.title
        video_views = self.views
        video_channel = self.author
        video_length = self.length
        video_publish = self.publish_date
        video_streams = self.streams.filter(
            progressive=True, type='video')
        audio_streams = self.streams.filter(type='audio').order_by('abr')
        video_thumbnail_url = self.thumbnail_url


class Root(cust.CTk):
    """Main Class Of App (Root Of App)"""

    def __init__(self, **kwargs):
        super().__init__()
        self.title = 'Yvai'
        self.geometry(
            '700x500+0+0')
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)

        # Navigation Frame Init

        self.navigation_frame = cust.CTkFrame(
            self, corner_radius=0, fg_color='#232F34')
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        self.navigation_frame_label = cust.CTkLabel(self.navigation_frame, text="Y  V  A  I",
                                                    compound="left", font= cust.CTkFont('Tajawal',weight='bold',size=20))
        self.navigation_frame_label.grid(row=0, column=0, padx=5, pady=50)

        # Nav Buttons Init

        self.youtube_button = cust.CTkButton(self.navigation_frame, corner_radius=7, height=40, border_spacing=10, text="Youtube", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("#4A6572", "#4A6572"), anchor="w", font= cust.CTkFont('Tajawal',weight='bold',size=14), command=self.youtube_button_event)
        self.youtube_button.grid(row=1, column=0, sticky="ew", pady=15)
        self.options_button = cust.CTkButton(self.navigation_frame, corner_radius=7, height=40, border_spacing=10, text="Options",
                                             fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("#4A6572", "#4A6572"), font= cust.CTkFont('Tajawal',weight='bold'),
                                             anchor="w", command=self.option_button_event)
        self.options_button.grid(row=5, column=0, sticky="ew", pady=10)
        self.about_button = cust.CTkButton(self.navigation_frame, corner_radius=7, height=40, border_spacing=10, text="About",
                                           fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("#4A6572", "#4A6572"), font= cust.CTkFont('Tajawal',weight='bold'),
                                           anchor="w", command=self.about_button_event)
        self.about_button.grid(row=6, column=0, sticky="ew", pady=10)

        # Button Frames Init

        self.youtube_frame = cust.CTkScrollableFrame(
            self, corner_radius=10, fg_color='#344955', bg_color='#232F34')
        self.youtube_frame.grid_rowconfigure(0, weight=1)
        self.youtube_frame.grid_rowconfigure(1, weight=3)
        self.youtube_frame.grid_columnconfigure(0, weight=1)
        self.youtube_frame.grid(row=0, column=1, sticky="nsew")
        self.options_frame = cust.CTkFrame(
            self, corner_radius=10, fg_color='#344955', bg_color='#232F34')
        self.about_frame = cust.CTkFrame(
            self, corner_radius=10, fg_color='#344955', bg_color='#232F34')

        # URL(Youtube) frame init
        self.URL_frame = cust.CTkFrame(
            self.youtube_frame, fg_color='transparent', bg_color='transparent')
        self.URL_frame.grid_rowconfigure(0, weight=1)
        self.URL_frame.grid_columnconfigure(0, weight=2)
        self.URL_frame.grid_columnconfigure(1, weight=6)
        self.URL_frame.grid_columnconfigure(2, weight=3)
        self.URL_frame.grid(column=0, row=0, sticky='nsew')

        self.URL_entry_field_Frame = cust.CTkFrame(
            self.URL_frame, fg_color='transparent')
        self.URL_entry_field_Frame.grid_columnconfigure(0, weight=1)
        self.URL_entry_field_Frame.grid_rowconfigure(0, weight=0)
        self.URL_entry_field_Frame.grid_rowconfigure(1, weight=6)
        self.URL_entry_field_Frame.grid_rowconfigure(2, weight=1)
        self.URL_entry_field_Frame.grid(
            row=0, column=1, sticky='nsew', pady=90)
        self.URL_Label = cust.CTkLabel(
            self.URL_frame, text="URL :   ", text_color='#eee', font= cust.CTkFont('Tajawal',weight='bold'))
        self.URL_Label.grid(column=0, row=0, sticky='e', padx=10)
        self.URL_entryField = cust.CTkEntry(
            self.URL_entry_field_Frame, justify='center', height=35, text_color='#eee')
        self.URL_entryField.grid(column=0, row=1, sticky='ew', pady=10)
        self.URL_entryField.bind(
            '<Return>', lambda x: self.url_func())
        self.URL_entryField.focus_set()
        self.URL_button = cust.CTkButton(
            self.URL_frame, text='Start', height=35, command=self.url_func, fg_color='#F9AA33', border_color='#111', text_color='#111', border_width=1, hover_color='#4A6572', font= cust.CTkFont('Tajawal',weight='bold'))
        self.URL_button.grid(row=0, column=2, sticky='w')
        self.URL_copy = cust.CTkButton(self.URL_frame, text='Paste',height=5,fg_color=self.URL_entryField._fg_color,bg_color='transparent', border_spacing=8,border_color=self.URL_entryField._border_color,border_width=2,width=8,corner_radius=self.URL_entryField._corner_radius,font=cust.CTkFont(family='Helvatica',size=13,weight='bold'),command=self.copy_URL)
        self.URL_copy.grid(row=0,column=1,sticky='e',padx=1)
        # info frame init
        self.info_frame = cust.CTkFrame(self.youtube_frame,fg_color='transparent')
        self.info_frame.columnconfigure(0,weight=1)
        self.info_frame.columnconfigure(1,weight=1)
        self.info_frame.rowconfigure(0,weight=1)
        self.info_frame.grid(row=1,column=0,sticky='nsew')
        # Select Frames Init

        self.select_frame_by_name("youtube")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.youtube_button.configure(
            bg_color=("#F9AA33", "#344955") if name == "youtube" else "transparent")
        self.options_button.configure(
            bg_color=("#F9AA33", "#344955") if name == "options" else "transparent")
        self.about_button.configure(
            bg_color=("#F9AA33", "#344955") if name == "about" else "transparent")
        # show selected frame
        if name == "youtube":
            self.youtube_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.youtube_frame.grid_forget()
        if name == "options":
            self.options_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.options_frame.grid_forget()
        if name == "about":
            self.about_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.about_frame.grid_forget()

    def youtube_button_event(self):
        self.select_frame_by_name("youtube")

    def option_button_event(self):
        self.select_frame_by_name("options")

    def about_button_event(self):
        self.select_frame_by_name("about")

    def copy_URL(self) :
        global data
        data = self.clipboard_get()
        self.URL_entryField.delete(0, cust.END)
        self.URL_entryField.insert(string=data,index=0)

    def delete_first(self) :
        self.thumbnail_frame.grid_forget()

    def show_info(self) :
        self.tkinterImage_video_thumbnail = cust.CTkImage(light_image=video_thumbnail,
                                  dark_image=video_thumbnail,
                                  size=(video_thumbnail.width*(2/3),video_thumbnail.height*(2/3)))
        self.thumbnail_frame = cust.CTkLabel(self.info_frame,image=self.tkinterImage_video_thumbnail,fg_color='#000',text='',corner_radius=4)
        self.thumbnail_frame.grid(row=0,column=0,padx=10)
        # video details frame init :
        self.details_frame = cust.CTkFrame(self.info_frame,fg_color='transparent',width=self.info_frame.winfo_width()//2,height=self.info_frame.winfo_height())
        self.details_frame.columnconfigure(0,weight=1)
        self.details_frame.rowconfigure(0,weight=1)
        self.details_frame.rowconfigure(1,weight=1)
        self.details_frame.rowconfigure(2,weight=1)
        self.details_frame.rowconfigure(3,weight=1)
        self.details_frame.rowconfigure(4,weight=1)
        self.details_frame.grid(row=0,column=1,sticky='nsew',padx=20,pady=20)
        self.vid_title = cust.CTkLabel(self.details_frame,font=cust.CTkFont('Tajawal',weight='normal',size=17),text=f'title: {video_title}',justify='left')
        self.vid_title.grid(row=0,sticky='w')
        self.vid_length  = cust.CTkLabel(self.details_frame,font=cust.CTkFont('Tajawal',weight='normal',size=17),text=f'video duration: {video_length}',justify='left')
        self.vid_length.grid(row=1,sticky='w')
        self.vid_author = cust.CTkLabel(self.details_frame,font=cust.CTkFont('Tajawal',weight='normal',size=17),text=f'channel: {video_channel}',justify='left')
        self.vid_author.grid(row=2,sticky='w')
        self.vid_views = cust.CTkLabel(self.details_frame,font=cust.CTkFont('Tajawal',weight='normal',size=17),text=f'{video_views} view',justify='left')
        self.vid_views.grid(row=3,sticky='w')
        self.vid_publish = cust.CTkLabel(self.details_frame,font=cust.CTkFont('Tajawal',weight='normal',size=17),text=f'publish date: {video_publish}',justify='left')
        self.vid_publish.grid(row=4,sticky='w')
        #self.vid_streams = video_dict
        #self.audio_streams = audio_dict
    def url_func(self):
        if not self.URL_entryField.get():  # if entry was empty
            messagebox.showerror(
                message='URL field is empty            ', title='Error')
        else:
            try:
                try:
                    self.delete_first()
                except Exception:
                    pass
                Youtube.url = self.URL_entryField.get()
                YouTube(Youtube.url).check_availability()
                asyncio.run(Youtube.write(Youtube()))
                self.show_info()
            except Exception as e:
                if e in Exc.Internet_ExcList :
                    messagebox.showerror(
                        message='Check internet connection and try again', title='Error')
                elif e == Exc.ageRestricted_Error :
                     messagebox.showerror(
                        message='The Video is age restricted, can\'t be accessed ', title='Error')
                elif e == Exc.stream_Error :
                    messagebox.showerror(
                        message='The Video is a live stream, it\'s not downloadable', title='Error')
                elif e == Exc.videoMembersOnly_Error :
                    messagebox.showerror(
                        message='The Video is members only, can\'t be accessed ', title='Error')
                elif e == Exc.videoPrivate_Error :
                    messagebox.showerror(
                        message='The Video is Private', title='Error')
                elif e == Exc.videoRegionBlocked_Error :
                    messagebox.showerror(
                        message='The Video is unavailable in your region', title='Error')
                elif e == Exc.videoUnavailable_Error :
                    messagebox.showerror(
                        message='The Video is unavailable', title='Error')
                else :
                    messagebox.showerror(
                        message='URL is invalid            ', title='Error')
                raise e

if __name__ == "__main__":
    root = Root()
    root.mainloop()
