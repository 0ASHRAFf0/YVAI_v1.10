import os,customtkinter as cust
from PIL import Image
from current_path import current_path,download_default_path
class Images() :
    download_image = cust.CTkImage(Image.open(current_path + "/images/download.png"),
                                               size=(20,20))