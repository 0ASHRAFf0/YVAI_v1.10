import os,customtkinter as cust
from PIL import Image
class Images() :
    current_path = os.path.dirname(os.path.realpath(__file__))
    download_image = cust.CTkImage(Image.open(current_path + "/images/download.png"),
                                               size=(20,20))