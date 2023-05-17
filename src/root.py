from typing import Optional, Tuple, Union
import customtkinter as cust
from tkinter import ttk, messagebox
import os
import webbrowser
from pytube import YouTube
from PIL import Image
import requests
from io import BytesIO
from moviepy.video.io.VideoFileClip import VideoFileClip
from pathlib import Path


#-----------Main class--------------
class Root(cust.CTk) :
    def __init__(self, **kwargs):
        super().__init__()
if __name__ == "__main__" :
    root = Root()
    root.mainloop()