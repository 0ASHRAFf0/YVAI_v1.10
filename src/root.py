import os
import asyncio
import threading
import webbrowser
import customtkinter as cust
from Exc import Exc
from re import search
from PIL import Image
from io import BytesIO
from requests import get
from images import Images
from pytube import YouTube
from settings import Settings
from time import strftime, gmtime
from tkinter import messagebox, Menu
from moviepy.video.io.VideoFileClip import VideoFileClip
from paths import current_path, download_default_path, check_download_path
# -----------Main class--------------
'''
https://youtu.be/17NLNg6v1qg
www.youtube.com/watch?v=oElol6JnT0w
https://www.youtube.com/watch?v=PITSYsAEjF0

#344955 center
#232F34 darker
#4A6572 lighter
#F9AA33 yellow
'''


class Youtube(YouTube):
    '''Youtube Video Informations'''

    def __init__(self, **kwargs):
        super().__init__(Youtube.url)

        Youtube.url: str

    async def write(self):
        await Youtube.get_video_info(self)
        global video_thumbnail, streams_dict, audio_dict, video_dict
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
        thumbnail_response = get(video_thumbnail_url)
        video_thumbnail = Image.open(BytesIO(thumbnail_response.content))
        video_thumbnail.resize(size=(
            video_thumbnail.width//2, video_thumbnail.height//2), resample=Image.Resampling.LANCZOS)

    async def get_video_info(self):
        global video_title, video_length, video_views, video_channel, video_publish, video_streams, audio_streams, video_thumbnail_url, video_url
        video_url = self.url
        video_title = self.title
        video_views = self.views
        video_channel = self.author
        video_length = strftime("%H:%M:%S", gmtime(self.length))
        video_publish = self.publish_date.strftime("%Y-%m-%d, %A")
        video_streams = self.streams.filter(
            progressive=True, type='video')
        audio_streams = self.streams.filter(type='audio').order_by('abr')
        video_thumbnail_url = self.thumbnail_url

    async def download_stream(self, itag, path_dir, filename):
        YouTube(url=video_url).streams.get_by_itag(itag=itag).download(
            output_path=path_dir, filename=filename)


class Root(cust.CTk):
    """Main Class Of App (Root Of App)"""

    def __init__(self, **kwargs):
        super().__init__()
        self.title('Yvai')
        check_download_path()
        self.after(0, lambda: self.state('zoomed'))
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)
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
        self.settings_button = cust.CTkButton(self.navigation_frame, corner_radius=7, height=40, border_spacing=10, text="Settings",
                                              fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("#4A6572", "#4A6572"), font=cust.CTkFont('Tajawal', weight='bold'),
                                              anchor="w", command=self.setting_button_event)
        self.settings_button.grid(row=5, column=0, sticky="ew", pady=10)
        self.about_button = cust.CTkButton(self.navigation_frame, corner_radius=7, height=40, border_spacing=10, text="About",
                                           fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("#4A6572", "#4A6572"), font=cust.CTkFont('Tajawal', weight='bold'),
                                           anchor="w", command=self.about_button_event)
        self.about_button.grid(row=6, column=0, sticky="ew", pady=10)
        # settings Frame init
        self.settings_frame = cust.CTkScrollableFrame(
            self, corner_radius=10, fg_color='#344955', bg_color='#232F34')
        self.settings_frame.grid_columnconfigure(0, weight=1)
        self.settings_frame.grid_rowconfigure(3, weight=1)
        self.settings_label = cust.CTkLabel(self.settings_frame, text='Download Settings', font=cust.CTkFont(
            'Tajawal', weight='bold', size=19), text_color='#eee')
        self.settings_label.grid(row=0, column=0, padx=30,
                                 pady=(60, 20), sticky='w')
        self.settings_save_frame = cust.CTkFrame(
            self.settings_frame, fg_color='transparent')
        self.settings_save_frame.grid_rowconfigure(0, weight=1)
        self.settings_save_frame.grid_columnconfigure(0, weight=1)
        self.settings_save_frame.grid(sticky='sew', row=15)
        self.settings_save_frame.grid_propagate(0)
        self.settings_save_button = cust.CTkButton(self.settings_save_frame, text='Save', height=35, command=self.save_settings, fg_color='#F9AA33',
                                                   border_color='#111', text_color='#111', border_width=1, hover_color='#4A6572', font=cust.CTkFont('Tajawal', weight='bold'))
        self.settings_save_button.grid(
            row=0, column=0, sticky='es', padx=20, pady=20)
    # Video Dir settings Init
        self.settings_videoDir_Frame = cust.CTkFrame(
            self.settings_frame, fg_color='transparent')
        self.settings_videoDir_Frame.grid_rowconfigure(0, weight=1)
        self.settings_videoDir_Frame.grid_columnconfigure(0, weight=1)
        self.settings_videoDir_Frame.grid_columnconfigure(1, weight=6)
        self.settings_videoDir_Frame.grid(
            row=1, column=0, sticky='nsew', pady=(0, 20))
        self.settings_videoDir_label = cust.CTkLabel(
            self.settings_videoDir_Frame, text="Default video directory :", text_color='#eee', font=cust.CTkFont('Tajawal', size=14))
        self.settings_videoDir_label.grid(column=0, row=0, sticky='w', padx=30)
        self.settings_videoDir_Entry = cust.CTkEntry(
            self.settings_videoDir_Frame, justify='center', height=35, width=400, text_color='#eee', textvariable=None)
        self.settings_videoDir_Entry.grid(column=1, row=0, sticky='w', pady=10)
        self.settings_videoDir_button = cust.CTkButton(self.settings_videoDir_Entry, text='Browse', height=5, fg_color=self.settings_videoDir_Entry._fg_color, bg_color='transparent', border_spacing=8, border_color=self.settings_videoDir_Entry._border_color,
                                                       border_width=2, width=8, corner_radius=self.settings_videoDir_Entry._corner_radius, font=cust.CTkFont(family='Helvatica', size=13, weight='bold'), command=lambda: self.browse_dir(btn=self.settings_videoDir_Entry))
        self.settings_videoDir_button.grid(row=0, column=1, sticky='e')
    # Audio Dir settings Init
        self.settings_audioDir_Frame = cust.CTkFrame(
            self.settings_frame, fg_color='transparent')
        self.settings_audioDir_Frame.grid_rowconfigure(0, weight=1)
        self.settings_audioDir_Frame.grid_columnconfigure(0, weight=1)
        self.settings_audioDir_Frame.grid_columnconfigure(1, weight=6)
        self.settings_audioDir_Frame.grid(
            row=2, column=0, sticky='nsew', pady=20)
        self.settings_audioDir_label = cust.CTkLabel(
            self.settings_audioDir_Frame, text="Default audio directory :", text_color='#eee', font=cust.CTkFont('Tajawal', size=14))
        self.settings_audioDir_label.grid(
            column=0, row=0, sticky='w', padx=(30, 32))
        self.settings_audioDir_Entry = cust.CTkEntry(
            self.settings_audioDir_Frame, justify='center', height=35, width=400, text_color='#eee', textvariable=None)
        self.settings_audioDir_Entry.grid(column=1, row=0, sticky='w', pady=10)
        self.settings_audioDir_button = cust.CTkButton(self.settings_audioDir_Entry, text='Browse', height=5, fg_color=self.settings_audioDir_Entry._fg_color, bg_color='transparent', border_spacing=8, border_color=self.settings_audioDir_Entry._border_color,
                                                       border_width=2, width=8, corner_radius=self.settings_audioDir_Entry._corner_radius, font=cust.CTkFont(family='Helvatica', size=13, weight='bold'), command=lambda: self.browse_dir(btn=self.settings_audioDir_Entry))
        self.settings_audioDir_button.grid(row=0, column=1, sticky='e')
    # Audio Dir settings Init
        self.settings_thumbnailDir_Frame = cust.CTkFrame(
            self.settings_frame, fg_color='transparent')
        self.settings_thumbnailDir_Frame.grid_rowconfigure(0, weight=1)
        self.settings_thumbnailDir_Frame.grid_columnconfigure(0, weight=1)
        self.settings_thumbnailDir_Frame.grid_columnconfigure(1, weight=6)
        self.settings_thumbnailDir_Frame.grid(
            row=3, column=0, sticky='nsew', pady=20)
        self.settings_thumbnailDir_label = cust.CTkLabel(
            self.settings_thumbnailDir_Frame, text="Default thumbnail directory :", text_color='#eee', font=cust.CTkFont('Tajawal', size=14))
        self.settings_thumbnailDir_label.grid(
            column=0, row=0, sticky='w', padx=(30, 5))
        self.settings_thumbnailDir_Entry = cust.CTkEntry(
            self.settings_thumbnailDir_Frame, justify='center', height=35, width=400, text_color='#eee', textvariable=None)
        self.settings_thumbnailDir_Entry.grid(
            column=1, row=0, sticky='w', pady=10)
        self.settings_thumbnailDir_button = cust.CTkButton(self.settings_thumbnailDir_Entry, text='Browse', height=5, fg_color=self.settings_thumbnailDir_Entry._fg_color, bg_color='transparent', border_spacing=8, border_color=self.settings_thumbnailDir_Entry._border_color,
                                                           border_width=2, width=8, corner_radius=self.settings_thumbnailDir_Entry._corner_radius, font=cust.CTkFont(family='Helvatica', size=13, weight='bold'), command=lambda: self.browse_dir(btn=self.settings_thumbnailDir_Entry))
        self.settings_thumbnailDir_button.grid(row=0, column=1, sticky='e')

        # YouTube Frame Init

        self.youtube_frame = cust.CTkScrollableFrame(
            self, corner_radius=10, fg_color='#344955', bg_color='#232F34')
        self.youtube_frame.grid_rowconfigure(0, weight=1)
        self.youtube_frame.grid_rowconfigure(1, weight=1)
        self.youtube_frame.grid_rowconfigure(2, weight=3)
        self.youtube_frame.grid_columnconfigure(0, weight=1)
        self.youtube_frame.grid(row=0, column=1, sticky="nsew")
        self.about_frame = cust.CTkFrame(
            self, corner_radius=10, fg_color='#344955', bg_color='#232F34')

        # URL(Youtube) frame init
        self.URL_frame = cust.CTkFrame(
            self.youtube_frame, fg_color='transparent', bg_color='transparent')
        self.URL_frame.grid_rowconfigure(0, weight=5)
        self.URL_frame.grid_rowconfigure(1, weight=1)
        self.URL_frame.grid_columnconfigure(0, weight=2)
        self.URL_frame.grid_columnconfigure(1, weight=6)
        self.URL_frame.grid_columnconfigure(2, weight=3)
        self.URL_frame.grid(column=0, row=0, sticky='nsew')

        self.URL_entry_field_Frame = cust.CTkFrame(
            self.URL_frame, fg_color='transparent')
        self.URL_entry_field_Frame.grid_columnconfigure(0, weight=1)
        self.URL_entry_field_Frame.grid_rowconfigure(0, weight=1)
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
        self.fetching_label = cust.CTkLabel(
            self.URL_frame, text='Fetching video data...', text_color='#b22222', font=cust.CTkFont('Helvatica', size=15, slant='italic'))

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
        self.settings_button.configure(
            bg_color=("#F9AA33", "#344955") if name == "settings" else "transparent")
        self.about_button.configure(
            bg_color=("#F9AA33", "#344955") if name == "about" else "transparent")
        # show selected frame
        if name == "youtube":
            self.youtube_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.youtube_frame.grid_forget()
        if name == "settings":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_frame.grid_forget()
            self.import_settings()
        if name == "about":
            self.about_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.about_frame.grid_forget()

    def youtube_button_event(self):
        self.select_frame_by_name("youtube")

    def setting_button_event(self):
        self.select_frame_by_name("settings")

    def about_button_event(self):
        self.select_frame_by_name("about")

    def get_ext(self, stream):
        ext = search(r'\(([\.].*)\)', stream)
        return ext.group()

    def paste_URL(self):
        global data
        data = self.clipboard_get()
        self.URL_entryField.delete(0, cust.END)
        self.URL_entryField.insert(string=data, index=0)
        self.update_idletasks()
        self.url_func()

    def delete_first(self):
        self.download_frame.grid_forget()
        self.info_frame.grid_forget()
        self.update_idletasks()
# show video informations

    def browse_dir(self, btn: cust.CTkButton):
        browsed_dir = cust.filedialog.askdirectory()
        if btn.winfo_parent() == '.!ctkframe2.!canvas.!ctkscrollableframe.!ctkframe2':
            self.settings_videoDir_Entry.delete(0, cust.END)
            self.settings_videoDir_Entry.insert(string=browsed_dir, index=0)
        elif btn.winfo_parent() == '.!ctkframe2.!canvas.!ctkscrollableframe.!ctkframe3':
            self.settings_audioDir_Entry.delete(0, cust.END)
            self.settings_audioDir_Entry.insert(string=browsed_dir, index=0)
        elif btn.winfo_parent() == '.!ctkframe2.!canvas.!ctkscrollableframe.!ctkframe4':
            self.settings_thumbnailDir_Entry.delete(0, cust.END)
            self.settings_thumbnailDir_Entry.insert(
                string=browsed_dir, index=0)

    def save_settings(self):
        vid_Op_get = self.settings_videoDir_Entry.get()
        audio_Op_get = self.settings_audioDir_Entry.get()
        thumbnail_Op_get = self.settings_thumbnailDir_Entry.get()
        for i in [vid_Op_get, audio_Op_get, thumbnail_Op_get]:
            if not os.path.isdir(i):
                messagebox.showerror(
                    title='Error', message=f'Unknown dir : {i}\nSettings Unsaved')
                return 0
        Settings.write_settings(
            vid_setting=vid_Op_get, audio_setting=audio_Op_get, thumb_setting=thumbnail_Op_get)
        messagebox.showinfo(
            title='Saved', message='Settings saved successfully')

    def import_settings(self):
        settings_Entries_list = [self.settings_videoDir_Entry,
                                 self.settings_audioDir_Entry, self.settings_thumbnailDir_Entry]
        for i in settings_Entries_list:
            i.delete(0, cust.END)
            try:
                i.insert(index=0, string=Settings.read_settings()
                         [settings_Entries_list.index(i)])
            except Exception as e:
                check_download_path()

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

# show download settings
    def show_dl_settings(self):
        self.download_frame = cust.CTkFrame(
            self.youtube_frame, fg_color='transparent')
        self.download_frame.grid_rowconfigure(0, weight=1)
        self.download_frame.grid_rowconfigure(1, weight=1)
        self.download_frame.grid_rowconfigure(2, weight=1)
        self.download_frame.grid_columnconfigure(0, weight=1)
        self.download_frame.grid(row=1, column=0, sticky='nsew')
        self.download_frame.grid_propagate(0)
        self.download_settings_frame = cust.CTkFrame(
            self.download_frame, fg_color='transparent')
        self.download_settings_frame.grid_rowconfigure(0, weight=1)
        self.download_settings_frame.grid_columnconfigure(0, weight=2)
        self.download_settings_frame.grid_columnconfigure(1, weight=3)
        self.download_settings_frame.grid(row=0, column=0, sticky='nsew')
        self.download_button = cust.CTkButton(
            self.download_settings_frame, text='Download', height=35, command=self.dl_video, fg_color='#F9AA33', border_color='#111', text_color='#111', border_width=1, hover_color='#4A6572', font=cust.CTkFont('Tajawal', weight='bold'), text_color_disabled='gray40')
        self.menu_stringVar = cust.StringVar(value='Choose download option')
        self.download_menu = cust.CTkOptionMenu(self.download_settings_frame, height=35, variable=self.menu_stringVar, fg_color='#232F34', bg_color='transparent', button_color='#4A6572', button_hover_color='#F9AA33', corner_radius=4,
                                                dropdown_fg_color='#232F34', dropdown_text_color='#eee', font=cust.CTkFont('Tajawal'), dropdown_font=cust.CTkFont('Tajawal'), hover='#4A6572', dropdown_hover_color='#4A6572')
        self.download_button.grid(row=0, column=1, sticky='w', padx=(20, 0))
        self.download_menu.grid(row=0, column=0, sticky='e', padx=(0, 20))


# Video Entry Init
        self.videoName_stringVar = cust.StringVar(
            value=Exc.replace_invalid_char(video_title))
        self.videoName_Frame = cust.CTkFrame(
            self.download_frame, fg_color='transparent')
        self.videoName_Frame.grid_rowconfigure(0, weight=1)
        self.videoName_Frame.grid_columnconfigure(0, weight=1)
        self.videoName_Frame.grid_columnconfigure(1, weight=6)
        self.videoName_Frame.grid(
            row=1, column=0, sticky='nsew')
        self.videoName_Label = cust.CTkLabel(
            self.videoName_Frame, text="File name   :    ", text_color='#eee', font=cust.CTkFont('Tajawal', weight='bold'))
        self.videoName_Label.grid(column=0, row=0, sticky='e', padx=37)
        self.fileName_Entry = cust.CTkEntry(
            self.videoName_Frame, justify='center', height=35, text_color='#eee', width=self.URL_entryField.winfo_width(), textvariable=self.videoName_stringVar)
        self.fileName_Entry.grid(column=1, row=0, sticky='w', pady=10)
        self.videoName_Button = cust.CTkButton(self.fileName_Entry, text='Default', height=5, fg_color=self.URL_entryField._fg_color, bg_color='transparent', border_spacing=8, border_color=self.URL_entryField._border_color,
                                               border_width=2, width=8, corner_radius=self.URL_entryField._corner_radius, font=cust.CTkFont(family='Helvatica', size=13, weight='bold'), command=self.set_default)
        self.videoName_Button.grid(row=0, column=1, sticky='e')
        self.write_video_streamsMenusettings()

    def set_default(self):
        self.fileName_Entry.delete(0, cust.END)
        self.fileName_Entry.insert(
            index=0, string=Exc.replace_invalid_char(video_title))
        self.update_idletasks()

    def write_video_streamsMenusettings(self):
        self.stream_options_list = []
        for stream in streams_dict:
            self.stream_options_list.append(stream)
        self.download_menu.configure(values=self.stream_options_list)
    # init decorator to check download options

    def checking_decorator(func):
        def check_download_options(self):
            self.default_border = self.fileName_Entry.cget('border_color')
            if self.download_menu.get() == 'Choose download option':
                self.download_menu.configure(button_color='red')
                self.update_idletasks()
            if self.fileName_Entry.get() == '':
                self.fileName_Entry.configure(border_color='red')
                self.update_idletasks()
            else:
                for i in self.fileName_Entry.get():
                    if i in Exc.invalid_char:
                        self.fileName_Entry.configure(border_color='red')
                        self.update_idletasks()
                        break
            if self.download_menu.cget('button_color') == 'red' or self.fileName_Entry.cget('border_color') == 'red':
                self.after(1500, self.fileName_Entry.configure(
                    border_color=self.default_border))
                self.after(0, self.download_menu.configure(
                    button_color='#4A6572'))
                return 0
            else:
                self.after(1500, self.fileName_Entry.configure(
                    border_color=self.default_border))
                self.after(0, self.download_menu.configure(
                    button_color='#4A6572'))

            func(self)
        return check_download_options

    @checking_decorator
    def dl_video(self):
        self.option_choosen = self.download_menu.get()
        self.itag = streams_dict[self.option_choosen]
        self.file_ext = self.get_ext(self.option_choosen[1:-1])
        self.path = self.settings_videoDir_Entry.get(
        ) if self.option_choosen in video_dict else self.settings_audioDir_Entry.get()
        self.filename = f'{self.fileName_Entry.get()}{self.file_ext[1:-1]}'
        try:
            asyncio.run(Youtube.download_stream(
                self=self, itag=self.itag, path_dir=self.path, filename=self.filename))
            messagebox.showinfo(
                message=f'File Downloaded Successfully in {self.path}')
        except PermissionError as e:
            messagebox.showerror(
                'Error', message='Download failed\ntry to change download path in settings')
            raise e

    def dl_thumbnail(self):
        try:
            video_thumbnail.save(
                rf"{self.settings_thumbnailDir_Entry.get()}\Thumbnail_{Exc.replace_invalid_char(video_title)}.png")
            messagebox.showinfo(
                message=f'Thumbnail downloaded in "{self.settings_thumbnailDir_Entry.get()}"')
        except Exception as e:
            messagebox.showerror(message=f'Download failed', title='Error')
            Exc.error_log(f'Thumbnail Failed ({e})')

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
                self.fetching_label.grid(row=1, column=1)
                self.update_idletasks()
                Youtube.url = self.URL_entryField.get()
                YouTube(Youtube.url).check_availability()
                asyncio.run(Youtube.write(Youtube()))
                self.show_info()
                self.show_dl_settings()
                self.fetching_label.grid_forget()
                self.update_idletasks()
            except Exception as e:
                if e == Exc.Internet_Error:
                    self.fetching_label.grid_forget()
                    self.update_idletasks()
                    messagebox.showerror(
                        message='Check internet connection and try again', title='Error')
                    Exc.error_log(f'Video Failed ({e})')
                elif e == Exc.ageRestricted_Error:
                    self.fetching_label.grid_forget()
                    self.update_idletasks()
                    messagebox.showerror(
                        message='The Video is age restricted, can\'t be accessed ', title='Error')
                    Exc.error_log(f'Video Failed ({e})')
                elif e == Exc.stream_Error:
                    self.fetching_label.grid_forget()
                    self.update_idletasks()
                    messagebox.showerror(
                        message='The Video is a live stream, it\'s not downloadable', title='Error')
                    Exc.error_log(f'Video Failed ({e})')
                elif e == Exc.videoMembersOnly_Error:
                    self.fetching_label.grid_forget()
                    self.update_idletasks()
                    messagebox.showerror(
                        message='The Video is members only, can\'t be accessed ', title='Error')
                    Exc.error_log(f'Video Failed ({e})')
                elif e == Exc.videoPrivate_Error:
                    self.fetching_label.grid_forget()
                    self.update_idletasks()
                    messagebox.showerror(
                        message='The Video is Private', title='Error')
                    Exc.error_log(f'Video Failed ({e})')
                elif e == Exc.videoRegionBlocked_Error:
                    self.fetching_label.grid_forget()
                    self.update_idletasks()
                    messagebox.showerror(
                        message='The Video is unavailable in your region', title='Error')
                    Exc.error_log(f'Video Failed ({e})')
                elif e == Exc.videoUnavailable_Error:
                    self.fetching_label.grid_forget()
                    self.update_idletasks()
                    messagebox.showerror(
                        message='The Video is unavailable', title='Error')
                    Exc.error_log(f'Video Failed ({e})')
                else:
                    self.fetching_label.grid_forget()
                    self.update_idletasks()
                    messagebox.showerror(
                        message='URL is invalid            ', title='Error')
                    Exc.error_log(f'Video Failed ({e})')
                    raise e


if __name__ == "__main__":
    root = Root()
    root.mainloop()
