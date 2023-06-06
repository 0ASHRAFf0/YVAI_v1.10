import os
from win32com.shell import shell, shellcon
current_path = os.path.dirname(os.path.realpath(__file__))
download_default_path = f'{os.path.dirname(os.path.realpath(__file__))}/Downloads'
program_files_path = shell.SHGetFolderPath(0, shellcon.CSIDL_PROGRAM_FILESX86, None, 0)