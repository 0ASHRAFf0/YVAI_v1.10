import os
import customtkinter as cust
from PIL import Image
from paths import current_path, download_default_path


class Images():
    download_image = cust.CTkImage(Image.open(current_path + "/images/download.png"),
                                   size=(20, 20))
