import os
from Exc import Exc
from images import Images
from time import strftime, gmtime
from options import Options
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
#344955 center
#232F34 darker
#4A6572 lighter
#F9AA33 yellow

https://youtu.be/17NLNg6v1qg
www.youtube.com/watch?v=oElol6JnT0w
https://www.youtube.com/watch?v=PITSYsAEjF0
'''


class Youtube(YouTube):
    '''Youtube Video Informations'''

    def __init__(self=None, **kwargs):
        super().__init__(Youtube.url)
        Youtube.url = ''

    async def write(self):
        await Youtube.get_video_info(self)
        global video_thumbnail, video_dict, audio_dict
        audio_dict = {}
        video_dict = {}

        for video in video_streams:
            video_dict.update(
                [(f'{video.resolution} (.{video.mime_type[6:]}), ', f'{video.filesize_mb:.1f}')])
        for audio in audio_streams:
            audio_dict.update([(audio.abr, audio.itag)])
        print(
            f'{video_title}\n{video_views}\n{video_channel}\n{video_length}\n{video_publish}\n')
        print(audio_dict)
        print(video_dict)
        print(audio_streams)
        thumbnail_response = get(video_thumbnail_url)
        video_thumbnail = Image.open(BytesIO(thumbnail_response.content))
        video_thumbnail.resize(size=(
            video_thumbnail.width//2, video_thumbnail.height//2), resample=Image.ANTIALIAS)

    async def get_video_info(self):
        global video_title, video_length, video_views, video_channel, video_publish, video_streams, audio_streams, video_thumbnail_url
        video_title = self.title
        video_views = self.views
        video_channel = self.author
        video_length = strftime("%H:%M:%S", gmtime(self.length))
        video_publish = self.publish_date.strftime("%Y-%m-%d, %A")
        video_streams = self.streams.filter(
            progressive=True, type='video')
        audio_streams = self.streams.filter(type='audio').order_by('abr')
        video_thumbnail_url = self.thumbnail_url


class Root(cust.CTk):
    """Main Class Of App (Root Of App)"""

    def __init__(self, **kwargs):
        super().__init__()
        self.title('Yvai')
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)
        self.geometry("%dx%d+0+0" %
                      (self.winfo_screenwidth(), self.winfo_screenheight()))
        # Navigation Frame Init

        self.navigation_frame = cust.CTkFrame(
            self, corner_radius=0, fg_color='#232F34')
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        self.navigation_frame_label = cust.CTkLabel(self.navigation_frame, text="Y  V  A  I",
                                                    compound="left", font=cust.CTkFont('Tajawal', weight='bold', size=20))
        self.navigation_frame_label.grid(row=0, column=0, padx=5, pady=50)

        # Nav Buttons Init

        self.youtube_button = cust.CTkButton(self.navigation_frame, corner_radius=7, height=40, border_spacing=10, text="Youtube", fg_color="transparent", text_color=(
            "gray10", "gray90"), hover_color=("#4A6572", "#4A6572"), anchor="w", font=cust.CTkFont('Tajawal', weight='bold', size=14), command=self.youtube_button_event)
        self.youtube_button.grid(row=1, column=0, sticky="ew", pady=15)
        self.options_button = cust.CTkButton(self.navigation_frame, corner_radius=7, height=40, border_spacing=10, text="Options",
                                             fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("#4A6572", "#4A6572"), font=cust.CTkFont('Tajawal', weight='bold'),
                                             anchor="w", command=self.option_button_event)
        self.options_button.grid(row=5, column=0, sticky="ew", pady=10)
        self.about_button = cust.CTkButton(self.navigation_frame, corner_radius=7, height=40, border_spacing=10, text="About",
                                           fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("#4A6572", "#4A6572"), font=cust.CTkFont('Tajawal', weight='bold'),
                                           anchor="w", command=self.about_button_event)
        self.about_button.grid(row=6, column=0, sticky="ew", pady=10)
        # Options Frame init

        self.options_frame = cust.CTkScrollableFrame(
            self, corner_radius=10, fg_color='#344955', bg_color='#232F34')
        self.options_frame.grid_rowconfigure(3, weight=1)
        self.options_frame.grid_columnconfigure(0, weight=1)
        self.options_frame.grid_columnconfigure(1, weight=6)

        # YouTube Frame Init

        self.youtube_frame = cust.CTkScrollableFrame(
            self, corner_radius=10, fg_color='#344955', bg_color='#232F34')
        self.youtube_frame.grid_rowconfigure(0, weight=1)
        self.youtube_frame.grid_rowconfigure(1, weight=1)
        self.youtube_frame.grid_rowconfigure(2, weight=3)
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
            self.URL_frame, text="URL :   ", text_color='#eee', font=cust.CTkFont('Tajawal', weight='bold'))
        self.URL_Label.grid(column=0, row=0, sticky='e', padx=10)
        self.URL_entryField = cust.CTkEntry(
            self.URL_entry_field_Frame, justify='center', height=35, text_color='#eee')
        self.URL_entryField.grid(column=0, row=1, sticky='ew', pady=10)
        self.URL_entryField.bind(
            '<Return>', lambda x: self.url_func())
        self.URL_button = cust.CTkButton(
            self.URL_frame, text='Start', height=35, command=self.url_func, fg_color='#F9AA33', border_color='#111', text_color='#111', border_width=1, hover_color='#4A6572', font=cust.CTkFont('Tajawal', weight='bold'))
        self.URL_button.grid(row=0, column=2, sticky='w', padx=10)
        self.URL_paste = cust.CTkButton(self.URL_frame, text='Paste', height=5, fg_color=self.URL_entryField._fg_color, bg_color='transparent', border_spacing=8, border_color=self.URL_entryField._border_color,
                                        border_width=2, width=8, corner_radius=self.URL_entryField._corner_radius, font=cust.CTkFont(family='Helvatica', size=13, weight='bold'), command=self.paste_URL)
        self.URL_paste.grid(row=0, column=1, sticky='e', padx=1)

        # info frame init
        self.info_frame = cust.CTkFrame(
            self.youtube_frame, fg_color='#232F34')
        self.info_frame.columnconfigure(0, weight=1)
        self.info_frame.columnconfigure(1, weight=1)
        self.info_frame.rowconfigure(0, weight=1)
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

    def paste_URL(self):
        global data
        data = self.clipboard_get()
        self.URL_entryField.delete(0, cust.END)
        self.URL_entryField.insert(string=data, index=0)

    def delete_first(self):
        self.thumbnail_frame.grid_forget()
# show video informations

    def show_info(self):
        self.tkinterImage_video_thumbnail = cust.CTkImage(light_image=video_thumbnail,
                                                          dark_image=video_thumbnail,
                                                          size=(video_thumbnail.width*(2/3), video_thumbnail.height*(2/3)))
        self.thumbnail_frame = cust.CTkLabel(
            self.info_frame, image=self.tkinterImage_video_thumbnail, fg_color='#000', text='', corner_radius=4)
        self.thumbnail_frame.grid(row=0, column=0, padx=10, pady=20)
        try:
            self.thumbnail_download = cust.CTkButton(
                self.thumbnail_frame, text=None, image=Images.download_image, fg_color='#F9AA33', hover_color='#4A6572', text_color='#111', height=10, width=10, border_color='#111', border_width=2, corner_radius=3, command=self.dl_thumbnail)
        except:
            self.thumbnail_download = cust.CTkButton(
                self.thumbnail_frame, text='download', fg_color='#F9AA33', hover_color='#4A6572', border_width=2, corner_radius=3, command=self.dl_thumbnail)
        self.thumbnail_download.grid(
            row=0, column=0, sticky='ne', padx=10, pady=10)
        # video details frame init :
        self.details_frame = cust.CTkFrame(self.info_frame, fg_color='transparent',
                                           width=self.info_frame.winfo_width()//2, height=self.info_frame.winfo_height())
        self.details_frame.columnconfigure(0, weight=1)
        self.details_frame.rowconfigure(0, weight=1)
        self.details_frame.rowconfigure(1, weight=1)
        self.details_frame.rowconfigure(2, weight=1)
        self.details_frame.rowconfigure(3, weight=1)
        self.details_frame.rowconfigure(4, weight=1)
        self.details_frame.grid(
            row=0, column=1, sticky='nsew', padx=20, pady=20)
        self.vid_title = cust.CTkLabel(self.details_frame, font=cust.CTkFont(
            'Tajawal', weight='normal', size=17), text=f'Title: {video_title}', justify='left')
        self.vid_title.grid(row=0, sticky='w')
        self.vid_length = cust.CTkLabel(self.details_frame, font=cust.CTkFont(
            'Tajawal', weight='normal', size=17), text=f'Duration: {video_length}', justify='left')
        self.vid_length.grid(row=1, sticky='w')
        self.vid_author = cust.CTkLabel(self.details_frame, font=cust.CTkFont(
            'Tajawal', weight='normal', size=17), text=f'Channel: {video_channel}', justify='left')
        self.vid_author.grid(row=2, sticky='w')
        self.vid_views = cust.CTkLabel(self.details_frame, font=cust.CTkFont(
            'Tajawal', weight='normal', size=17), text=f'{video_views:,d} View', justify='left')
        self.vid_views.grid(row=3, sticky='w')
        self.vid_publish = cust.CTkLabel(self.details_frame, font=cust.CTkFont(
            'Tajawal', weight='normal', size=17), text=f'Publish date: {video_publish}', justify='left')
        self.vid_publish.grid(row=4, sticky='w')
        self.info_frame.grid(row=2, column=0, sticky='nsew', pady=10)

        # self.vid_streams = video_dict
        # self.audio_streams = audio_dict
 # show download options
    def show_dl_options(self):
        self.download_frame = cust.CTkFrame(
            self.youtube_frame, fg_color='transparent')
        self.download_frame.grid_rowconfigure(0, weight=1)
        self.download_frame.grid_rowconfigure(1, weight=1)
        self.download_frame.grid_rowconfigure(2, weight=1)
        self.download_frame.grid_columnconfigure(0, weight=1)
        self.download_frame.grid(row=1, column=0, sticky='nsew')
        self.download_frame.grid_propagate(0)
        self.download_options_frame = cust.CTkFrame(
            self.download_frame, fg_color='transparent')
        self.download_options_frame.grid_rowconfigure(0, weight=1)
        self.download_options_frame.grid_columnconfigure(0, weight=2)
        self.download_options_frame.grid_columnconfigure(1, weight=3)
        self.download_options_frame.grid(row=0, column=0, sticky='nsew')
        self.download_button = cust.CTkButton(
            self.download_options_frame, text='Download', height=35, command=self.dl_video, fg_color='#F9AA33', border_color='#111', text_color='#111', border_width=1, hover_color='#4A6572', font=cust.CTkFont('Tajawal', weight='bold'), text_color_disabled='gray40')
        self.download_button.grid(row=0, column=1, sticky='w', padx=(20, 0))
        menu_stringVar = cust.StringVar(value='Choose download option')
        self.download_menu = cust.CTkOptionMenu(self.download_options_frame, height=35, variable=menu_stringVar, fg_color='#232F34', bg_color='transparent', button_color='#4A6572', button_hover_color='#F9AA33', corner_radius=4,
                                                dropdown_fg_color='#232F34', dropdown_text_color='#eee', font=cust.CTkFont('Tajawal'), dropdown_font=cust.CTkFont('Tajawal'), values=['1', '2', '3'], hover='#4A6572', dropdown_hover_color='#4A6572')
        self.download_menu.grid(row=0, column=0, sticky='e', padx=(0, 20))

# Directory Entry Init
        directory_stringVar = cust.StringVar(value=f'{Root.video_directory}')
        videoName_stringVar = cust.StringVar(value=f'{video_title}')
        self.directory_Frame = cust.CTkFrame(
            self.download_frame, fg_color='transparent')
        self.directory_Frame.grid_rowconfigure(0, weight=1)
        self.directory_Frame.grid_columnconfigure(0, weight=1)
        self.directory_Frame.grid_columnconfigure(1, weight=6)
        self.directory_Frame.grid(
            row=1, column=0, sticky='nsew')
        self.browse_Label = cust.CTkLabel(
            self.directory_Frame, text="download directory :", text_color='#eee', font=cust.CTkFont('Tajawal', weight='bold'))
        self.browse_Label.grid(column=0, row=0, sticky='e', padx=20)
        self.directory_Entry = cust.CTkEntry(
            self.directory_Frame, justify='center', height=35, text_color='#eee', width=self.URL_entryField.winfo_width(), textvariable=directory_stringVar)
        self.directory_Entry.grid(column=1, row=0, sticky='w', pady=10)
        self.browse_Button = cust.CTkButton(self.directory_Entry, text='Browse', height=5, fg_color=self.directory_Entry._fg_color, bg_color='transparent', border_spacing=8, border_color=self.directory_Entry._border_color,
                                            border_width=2, width=8, corner_radius=self.directory_Entry._corner_radius, font=cust.CTkFont(family='Helvatica', size=13, weight='bold'), command=self.paste_URL)
        self.browse_Button.grid(row=0, column=1, sticky='e')
# Video Entry Init

        self.videoName_Frame = cust.CTkFrame(
            self.download_frame, fg_color='transparent')
        self.videoName_Frame.grid_rowconfigure(0, weight=1)
        self.videoName_Frame.grid_columnconfigure(0, weight=1)
        self.videoName_Frame.grid_columnconfigure(1, weight=6)
        self.videoName_Frame.grid(
            row=2, column=0, sticky='nsew')
        self.videoName_Label = cust.CTkLabel(
            self.videoName_Frame, text="File name   :    ", text_color='#eee', font=cust.CTkFont('Tajawal', weight='bold'))
        self.videoName_Label.grid(column=0, row=0, sticky='e', padx=37)
        self.videoName_Entry = cust.CTkEntry(
            self.videoName_Frame, justify='center', height=35, text_color='#eee', width=self.URL_entryField.winfo_width(), textvariable=videoName_stringVar)
        self.videoName_Entry.grid(column=1, row=0, sticky='w', pady=10)
        self.videoName_Button = cust.CTkButton(self.videoName_Entry, text='Default', height=5, fg_color=self.directory_Entry._fg_color, bg_color='transparent', border_spacing=8, border_color=self.directory_Entry._border_color,
                                               border_width=2, width=8, corner_radius=self.directory_Entry._corner_radius, font=cust.CTkFont(family='Helvatica', size=13, weight='bold'), command=self.paste_URL)
        self.videoName_Button.grid(row=0, column=1, sticky='e')

    def write_video_streamsMenuOptions(self):
        pass

    def dl_video(self):
        if self.download_menu.get() == 'Choose download option':
            self.download_menu['fg_color'] == 'red'
        if self.directory_Entry.get() == 'lol':
            self.directory_Entry['border_color'] == 'red'
        if self.videoName_Entry.get() == 'lol':
            self.videoName_Entry['border_color'] == 'red'

    def dl_thumbnail(self):
        try:
            video_thumbnail.save(
                rf"{Images.current_path}\Downloads\{video_title.replace(' ','_')}.png")
            messagebox.showinfo(
                message=f'Thumbnail downloaded in "{Images.current_path}\Downloads"')
        except Exception as e:
            messagebox.showerror(message=f'Download failed', title='Error')

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
                self.show_dl_options()
            except Exception as e:
                if e in Exc.Internet_ExcList:
                    messagebox.showerror(
                        message='Check internet connection and try again', title='Error')
                elif e == Exc.ageRestricted_Error:
                    messagebox.showerror(
                        message='The Video is age restricted, can\'t be accessed ', title='Error')
                elif e == Exc.stream_Error:
                    messagebox.showerror(
                        message='The Video is a live stream, it\'s not downloadable', title='Error')
                elif e == Exc.videoMembersOnly_Error:
                    messagebox.showerror(
                        message='The Video is members only, can\'t be accessed ', title='Error')
                elif e == Exc.videoPrivate_Error:
                    messagebox.showerror(
                        message='The Video is Private', title='Error')
                elif e == Exc.videoRegionBlocked_Error:
                    messagebox.showerror(
                        message='The Video is unavailable in your region', title='Error')
                elif e == Exc.videoUnavailable_Error:
                    messagebox.showerror(
                        message='The Video is unavailable', title='Error')
                else:
                    messagebox.showerror(
                        message='URL is invalid            ', title='Error')
                raise e


if __name__ == "__main__":
    root = Root()
    root.mainloop()
