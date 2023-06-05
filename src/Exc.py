from pytube import exceptions
from requests.exceptions import ConnectionError, HTTPError, Timeout, ReadTimeout
from urllib.error import URLError


class Exc():
    Internet_ExcList = [ConnectionError, HTTPError, ReadTimeout,
                        Timeout, URLError, exceptions.HTMLParseError, OSError]
    stream_Error = exceptions.LiveStreamError
    ageRestricted_Error = exceptions.AgeRestrictedError
    videoUnavailable_Error = exceptions.VideoUnavailable
    videoPrivate_Error = exceptions.VideoPrivate
    videoRegionBlocked_Error = exceptions.VideoRegionBlocked
    videoMembersOnly_Error = exceptions.MembersOnly
