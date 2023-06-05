import os
import datetime


class Options():
    def __init__(self, videoDir_Op, audioDir_Op, thumbDir_Op):
        self.video_directory = videoDir_Op
        self.audio_directory = audioDir_Op
        self.thumbnail_directory = thumbDir_Op

    @staticmethod
    def write_options():
        with open('options.txt', 'w+') as Op_file:
            Op_file.write(
                f'{datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")} "{os.path.dirname(os.path.realpath(__file__))}"\n')

    @staticmethod
    def read_options():
        with open('options.txt', 'r') as Op_file:
            print(Op_file.readline())


Options.write_options()
Options.read_options()
