import os
crnt_path = os.path.dirname(os.path.realpath(__file__))


class Settings():

    @staticmethod
    def write_settings(vid_setting, audio_setting, thumb_setting):
        with open(rf'{crnt_path}\settings.txt', 'w+') as Op_file:
            Op_file.write(
                f'{vid_setting}|{audio_setting}|{thumb_setting}')

    @staticmethod
    def read_settings():
        if not os.path.isfile(rf'{crnt_path}\settings.txt'):
            with open(rf'{crnt_path}\settings.txt', 'w') as Op_file:
                pass
        with open(rf'{crnt_path}\settings.txt', 'r') as Op_file:
            return (Op_file.readline()).split('|')
