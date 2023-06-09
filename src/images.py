import os
from customtkinter import CTkImage
from PIL import Image
from paths import current_path, download_default_path, image_path


class Images():
    download_image = CTkImage(Image.open(rf"{image_path}\download.png"),
                              size=(20, 20))
    # yvai_cover = CTkImage(Image.open(rf'{image_path}\yvai_cover.png'))
