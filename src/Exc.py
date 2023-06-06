from pytube import exceptions
from requests.exceptions import ConnectionError, HTTPError, Timeout, ReadTimeout
from urllib.error import URLError
import logging
from current_path import current_path,download_default_path

logging.basicConfig(filename='error_log.log', filemode='a',
                    format='%(asctime)s: %(name)s, %(levelname)s : %(message)s')


class Exc():
    invalid_char = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    Internet_ExcList = [ConnectionError, HTTPError, ReadTimeout,
                        Timeout, URLError, exceptions.HTMLParseError, OSError]
    stream_Error = exceptions.LiveStreamError
    ageRestricted_Error = exceptions.AgeRestrictedError
    videoUnavailable_Error = exceptions.VideoUnavailable
    videoPrivate_Error = exceptions.VideoPrivate
    videoRegionBlocked_Error = exceptions.VideoRegionBlocked
    videoMembersOnly_Error = exceptions.MembersOnly

    @staticmethod
    def error_log(err):
        logging.error(msg=err)

    @staticmethod
    def replace_invalid_char(name: str):
        title = ''
        for i in name:
            if i in Exc.invalid_char:
                title += '_'
            else:
                title += i
        return title