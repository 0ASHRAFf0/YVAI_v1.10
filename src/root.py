import os
import time
import asyncio
import requests
import threading
import webbrowser
import customtkinter as cust
from PIL import Image
from io import BytesIO
from pathlib import Path
from pytube import YouTube
from tkinter import ttk, messagebox
from moviepy.video.io.VideoFileClip import VideoFileClip
# -----------Main class--------------
'''
#344955
#232F34
#4A6572
#F9AA33
# '''

#https://youtu.be/17NLNg6v1qg

class Youtube(YouTube):
    '''Youtube Video Informations'''

    def __init__(self=None, **kwargs):
        super().__init__(Youtube.url)
        Youtube.url = ''

    async def write(self):
        await Youtube.get_video_info(self)
        audio_dict = {}
        video_dict = {}

        for video in video_streams:
            video_dict.update(
                [(f'{video.resolution} (.{video.mime_type[6:]}), ', f'{video.filesize_mb:.1f}')])
        for audio in audio_streams:
            # file.write(f'{audio.abr} (.mp3), {audio.filesize_mb:.1f}')
            audio_dict.update([(audio.abr, audio.itag)])
        print(f'{video_title}\n{video_views}\n{video_channel}\n{video_length}\n')
        print(audio_dict)
        print(video_dict)
        Root().fetching_bar.grid_remove()
        Root().url_frame_EMPTY.grid_remove()

    async def get_video_info(self):
        global video_title, video_length, video_views, video_channel, video_streams, audio_streams
        video_title = self.title
        video_views = self.views
        video_channel = self.author
        video_length = self.length
        video_streams = self.streams.filter(
            progressive=True, type='video')
        audio_streams = self.streams.filter(type='audio').order_by('abr')


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
        self.navigation_frame_label = cust.CTkLabel(self.navigation_frame, text="  Y  V  A  I",
                                                    compound="left", font=cust.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=5, pady=50)

        # Nav Buttons Init

        self.youtube_button = cust.CTkButton(self.navigation_frame, corner_radius=7, height=40, border_spacing=10, text="Youtube", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("#4A6572", "#4A6572"), anchor="w", command=self.youtube_button_event)
        self.youtube_button.grid(row=1, column=0, sticky="ew", pady=15)
        self.facebook_button = cust.CTkButton(self.navigation_frame, corner_radius=7, height=40, border_spacing=10, text="Facebook",
                                              fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("#4A6572", "#4A6572"),
                                              anchor="w", command=self.facebook_button_event)
        self.facebook_button.grid(row=2, column=0, sticky="ew", pady=15)
        self.instagram_button = cust.CTkButton(self.navigation_frame, corner_radius=7, height=40, border_spacing=10, text="Instagram", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("#4A6572", "#4A6572"),
                                               anchor="w", command=self.instagram_button_event)
        self.instagram_button.grid(row=3, column=0, sticky="ew", pady=15)
        self.options_button = cust.CTkButton(self.navigation_frame, corner_radius=7, height=40, border_spacing=10, text="Options",
                                             fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("#4A6572", "#4A6572"),
                                             anchor="w", command=self.option_button_event)
        self.options_button.grid(row=5, column=0, sticky="ew", pady=10)
        self.about_button = cust.CTkButton(self.navigation_frame, corner_radius=7, height=40, border_spacing=10, text="About",
                                           fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("#4A6572", "#4A6572"),
                                           anchor="w", command=self.about_button_event)
        self.about_button.grid(row=6, column=0, sticky="ew", pady=10)

        # Button Frames Init

        self.youtube_frame = cust.CTkScrollableFrame(
            self, corner_radius=10, fg_color='#344955', bg_color='#232F34')
        self.youtube_frame.grid_rowconfigure(1, weight=4)
        self.youtube_frame.grid_rowconfigure(2, weight=1)
        self.youtube_frame.grid_rowconfigure(0, weight=1)
        self.youtube_frame.grid_columnconfigure(0, weight=1)
        self.youtube_frame.grid(row=0, column=1, sticky="nsew")
        self.facebook_frame = cust.CTkFrame(
            self, corner_radius=10, fg_color='#344955', bg_color='#232F34')
        self.instagram_frame = cust.CTkFrame(
            self, corner_radius=10, fg_color='#344955', bg_color='#232F34')
        self.options_frame = cust.CTkFrame(
            self, corner_radius=10, fg_color='#344955', bg_color='#232F34')
        self.about_frame = cust.CTkFrame(
            self, corner_radius=10, fg_color='#344955', bg_color='#232F34')

        # youtube frame init
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
        self.url_frame_EMPTY = cust.CTkFrame(
            self.URL_entry_field_Frame, width=2, height=2, bg_color='transparent', fg_color='transparent')
        self.url_frame_EMPTY.grid(row=0, pady=8)
        self.URL_Label = cust.CTkLabel(
            self.URL_frame, text="URL :   ", text_color='#eee')
        self.URL_Label.grid(column=0, row=0, sticky='e', padx=10)
        self.URL_entryField = cust.CTkEntry(
            self.URL_entry_field_Frame, justify='center', height=35, text_color='#eee')
        self.URL_entryField.grid(column=0, row=1, sticky='ew', pady=10)
        self.URL_entryField.bind(
            '<Return>', lambda x: self.url_func())
        self.URL_entryField.focus_set()
        self.URL_button = cust.CTkButton(
            self.URL_frame, text='Start', height=35, command=self.url_func, fg_color='#F9AA33', border_color='#111', text_color='#111', border_width=1, hover_color='#4A6572')
        self.URL_button.grid(row=0, column=2, sticky='w')
        self.fetching_bar = cust.CTkProgressBar(
            self.URL_entry_field_Frame, width=200, mode='indeterminate', progress_color='green')
        self.fetching_bar.grid(row=2, column=0, pady=5)
        self.fetching_bar.grid_remove()
        self.url_frame_EMPTY.grid_remove()

        # Select Frames Init

        self.select_frame_by_name("youtube")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.youtube_button.configure(
            bg_color=("#F9AA33", "#344955") if name == "youtube" else "transparent")
        self.facebook_button.configure(
            bg_color=("#F9AA33", "#344955") if name == "facebook" else "transparent")
        self.instagram_button.configure(
            bg_color=("#F9AA33", "#344955") if name == "instagram" else "transparent")
        self.options_button.configure(
            bg_color=("#F9AA33", "#344955") if name == "options" else "transparent")
        self.about_button.configure(
            bg_color=("#F9AA33", "#344955") if name == "about" else "transparent")
        # show selected frame
        if name == "youtube":
            self.youtube_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.youtube_frame.grid_forget()
        if name == "facebook":
            self.facebook_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.facebook_frame.grid_forget()
        if name == "instagram":
            self.instagram_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.instagram_frame.grid_forget()
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

    def facebook_button_event(self):
        self.select_frame_by_name("facebook")

    def instagram_button_event(self):
        self.select_frame_by_name("instagram")

    def option_button_event(self):
        self.select_frame_by_name("options")

    def about_button_event(self):
        self.select_frame_by_name("about")

    def show_fetching_bar(self):
        self.fetching_bar.grid(row=2, column=0, pady=5)
        self.url_frame_EMPTY.grid(row=0, pady=8)
        self.fetching_bar.start()

    def url_func(self):
        if not self.URL_entryField.get():  # if entry was empty
            messagebox.showerror(
                message='URL field is empty            ', title='Error')
        else:
            try:
                Youtube.url = self.URL_entryField.get()
                YouTube(Youtube.url).check_availability()
                asyncio.run(Youtube.write(Youtube()))
                Root().show_fetching_bar()
            except Exception as e:
                messagebox.showerror(
                    message='URL is invalid            ', title='Error')


if __name__ == "__main__":
    root = Root()
    root.mainloop()
