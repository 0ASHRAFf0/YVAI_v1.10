from pytube import exceptions
from requests.exceptions import ConnectionError, HTTPError, Timeout, ReadTimeout
import urllib.error
import logging
logging.basicConfig(filename='error_log.log', filemode='a',
                    format='%(asctime)s: %(name)s, %(levelname)s : %(message)s')


class Exc():
    invalid_char = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    Internet_Error = urllib.error.URLError
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
