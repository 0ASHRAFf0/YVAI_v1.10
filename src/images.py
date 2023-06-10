import os
from customtkinter import CTkImage
from PIL import Image
from paths import current_path, download_default_path, image_path


class Images():
    download_image = CTkImage(Image.open(rf"{image_path}\download.png"),
                              size=(20, 20))
    yvai_image = CTkImage(Image.open(rf'{image_path}\logo.png'), size=(80, 80))
    yvai_icon = (rf'{current_path}\logo.ico')
    settings_image = CTkImage(Image.open(rf'{image_path}\settings_image.png'))
    youtube_image = CTkImage(Image.open(rf'{image_path}\play_arrow_image.png'))
    about_image = CTkImage(Image.open(rf'{image_path}\info_image.png'))
