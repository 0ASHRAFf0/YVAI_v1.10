import os
from settings import Settings
from Exc import Exc
current_path = os.path.dirname(os.path.realpath(__file__))
download_default_path = rf'{current_path}\Downloads'
image_path = rf'{current_path}\images'


def check_download_path():
    for i in Settings.read_settings():
        if i.replace(" ", "") == '':
            if not os.path.isdir(download_default_path):
                try:
                    os.makedirs(download_default_path)
                    Settings.write_settings(vid_setting=download_default_path,
                                            audio_setting=download_default_path, thumb_setting=download_default_path)
                except Exception as e:
                    pass
                    try:
                        Exc.error_log(f'handling while starts : {e}')
                    except Exception as e:
                        pass
            else:
                try:
                    Settings.write_settings(vid_setting=download_default_path,
                                            audio_setting=download_default_path, thumb_setting=download_default_path)
                except Exception as e:
                    pass
                    try:
                        Exc.error_log(f'handling while starts : {e}')
                    except Exception as e:
                        pass
