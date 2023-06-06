import os
import datetime
from current_path import current_path, download_default_path


class Options():
    options_dict = {'videoDir_Op': None,
                    'audioDir_Op':  None, 'thumbDir_Op': None}

    @staticmethod
    def write_options(vid_option, audio_option, thumb_option):
        with open(rf'{current_path}\options.txt', 'w+') as Op_file:
            Op_file.write(
                f'{vid_option}|{audio_option}|{thumb_option}')

    @staticmethod
    def read_options():
        with open(rf'{current_path}\options.txt', 'r') as Op_file:
            print((Op_file.readline()).split('|'))


Options.write_options('D:\MOHAMED ASHRAF\Coding\projects\YVAI_v1.10',
                      'D:\MOHAMED ASHRAF\Coding\projects\YVAI_v1.10', 'D:\MOHAMED ASHRAF\Coding\projects\YVAI_v1.10')
Options.read_options()
