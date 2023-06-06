import os
import datetime
from current_path import current_path, download_default_path

class Settings():
    settings_dict = {'videoDir_Op': None,
                    'audioDir_Op':  None, 'thumbDir_Op': None}

    @staticmethod
    def write_settings(vid_setting, audio_setting, thumb_setting):
        with open(rf'{current_path}\settings.txt', 'w+') as Op_file:
            Op_file.write(
                f'{vid_setting}|{audio_setting}|{thumb_setting}')

    @staticmethod
    def read_settings():
        with open(rf'{current_path}\settings.txt', 'r') as Op_file:
            return (Op_file.readline()).split('|')
