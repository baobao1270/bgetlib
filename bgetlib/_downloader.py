import os.path
import uuid
from typing import Union, Callable, Any, Tuple, List, Optional, Literal, Dict

from ._canlogin import CanLogin


class Downloader(CanLogin):
    import bgetlib.error as _error
    import bgetlib.model as _model
    import bgetlib.consts as _CONST_

    def __init__(self, user_agent: str = _CONST_.DEFAULT_DOWNLOAD_UA):
        super().__init__()
        self.headers = {
            "User-Agent": user_agent,
            "Referer": "https://www.bilibili.com/",
            "Accept": "*/*",
            "Icy-MetaData": "1"
        }
        from bgetlib.model import DownloadProgress
        self.callbacks: List[Callable[[DownloadProgress], bool]] = []

    def callback_func(self, func: Callable[[_model.DownloadProgress], bool]) -> None:
        self.callbacks.append(func)

    def download(self, avid: int, cid: int, tmp_dir: str, chunk_size: int = 4096,
                 cdn_host: Optional[str] = None, write_mode: str = "wb") -> uuid.UUID:
        video_url, audio_url = self._get_url(avid, cid, cdn_host)
        file_id = uuid.uuid4()
        video_filename = os.path.join(tmp_dir, "{}.{}".format(str(file_id), self._CONST_.DASH_VIDEO_EXTENSION))
        audio_filename = os.path.join(tmp_dir, "{}.{}".format(str(file_id), self._CONST_.DASH_AUDIO_EXTENSION))
        self.download_url(video_url, video_filename, chunk_size, write_mode=write_mode, _tag="video")
        self.download_url(audio_url, audio_filename, chunk_size, write_mode=write_mode, _tag="audio")
        return file_id

    def download_url(self, url: str, filename: str, chunk_size: int = 4096,
                     write_mode: str = "wb", _tag: Optional[str] = None):
        import requests
        import time
        stream = requests.get(url, headers=self.headers, cookies=self.cookies, stream=True)
        progress = self._model.DownloadProgress(
            total_bytes=int(stream.headers['content-length']),
            start=time.time(),
            slice_size=chunk_size,
            tag=_tag,
            url=url
        )
        with open(filename, write_mode) as f:
            for chunk in stream.iter_content(chunk_size=chunk_size):
                if chunk:
                    progress.update_time()
                    f.write(chunk)
                    if not self._call_back_funcs(progress):
                        raise self._error.CallbackAbortError()
        progress.finished = True
        self._call_back_funcs(progress)

    def _call_back_funcs(self, progress: _model.DownloadProgress) -> bool:
        for callback in self.callbacks:
            result = callback(progress)
            if (result is not None) and (not result):
                return False
        return True

    def _get_url(self, avid: int, cid: int, cdn_host: Optional[str] = None) -> Tuple[str, str]:
        import requests
        url = "https://api.bilibili.com/x/player/playurl?avid={avid}&cid={cid}&fnver=0&fnval=16&fourk=1".format(
            avid=avid, cid=cid
        )
        res = requests.get(url, headers=self.headers, cookies=self.cookies)
        if res.status_code != 200:
            raise self._error.HTTPError(url, res.status_code)
        res_json = res.json()
        if res_json["code"] != 0:
            raise self._error.ResponseCodeError(url, res_json["code"])
        video_url = self._parse_url(res_json, "video", cdn_host)
        audio_url = self._parse_url(res_json, "audio", cdn_host)
        return video_url, audio_url

    @staticmethod
    def _parse_url(json: Dict, key: Union[Literal["video"], Literal["audio"]], cdn_host: Optional[str] = None) -> str:
        medias = json["data"]["dash"][key]
        medias.sort(key=(lambda x: x["id"]), reverse=True)
        url = medias[0]["baseUrl"]
        if cdn_host is None:
            return url
        import urllib.parse as urllib
        # Don't lines below until end of this function!
        url = urllib.urlparse(url)._replace(netloc=cdn_host)
        return urllib.urlunparse(url)
