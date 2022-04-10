import os
import copy
import requests
import subprocess
from typing import Tuple, Optional, List
from .models import QualityOptions, StreamCallback
from .streamer import BasicStreamer
from . import utils


class BilibiliAPI:
    def __init__(self, cookie_filename: Optional[str] = None) -> None:
        if cookie_filename is not None:
            import http.cookiejar as cookiejar
            self.cookies = cookiejar.MozillaCookieJar()
            self.cookies.load(cookie_filename, ignore_discard=True, ignore_expires=True)
        else:
            self.cookies = None

    def _request(self, url: str, **kwargs) -> requests.Response:
        if self.cookies is not None:
            kwargs["cookies"] = self.cookies
        return requests.get(url, **kwargs)

    def _interface_request(self, path, **kwargs) -> dict:
        return self._request("https://api.bilibili.com" + path, **kwargs).json()

    def get_favorites(self, favorite_id: int, page: int = 1) -> list:
        path = "/x/v3/fav/resource/list?media_id={}&pn={}&ps=20&order=mtime".format(favorite_id, page)
        favourites = self._interface_request(path)["data"]["medias"]
        return favourites or []

    def get_favorites_all(self, favorite_id: int) -> List[dict]:
        page = 1
        favorites = []
        while True:
            page_favorites = self.get_favorites(favorite_id, page)
            if len(page_favorites) == 0:
                break
            favorites += page_favorites
            page += 1
        return favorites

    def get_favorites_since(self, favorite_id: int, from_timestamp: int) -> List[dict]:
        page = 1
        favorites = []
        while True:
            page_favorites = self.get_favorites(favorite_id, page)
            if len(page_favorites) == 0:
                break
            for fav in page_favorites:
                if fav["fav_time"] < from_timestamp:
                    break
                favorites.append(fav)
            page += 1
        return favorites

    def list_user_favourite_folders(self, uid: int) -> List[dict]:
        path = "/x/v3/fav/folder/created/list-all?up_mid={}".format(uid)
        folders = self._interface_request(path)["data"]["list"]
        return folders or []

    def get_video(self, aid: int) -> dict:
        path = "/x/web-interface/view?aid={}".format(aid)
        return self._interface_request(path)["data"]

    def get_live_danmaku(self, cid: int) -> bytes:
        url = "https://comment.bilibili.com/{}.xml".format(cid)
        return self._request(url).content

    def get_archive(self, category_id: int, tag_id: Optional[int] = None, page: int = 1) -> Tuple[int, List[dict]]:
        if tag_id is not None:
            path = "/x/tag/ranking/archives?ps=20&pn={}&rid={}&tag_id={}".format(page, category_id, tag_id)
        else:
            path = "/x/web-interface/newlist?ps=20&pn={}&rid={}".format(page, category_id)
        response = self._interface_request(path)
        videos = response["data"]["archives"]
        count = response["data"]["page"]["count"]
        return count, videos

    def list_stickers(self) -> List[dict]:
        path = "/x/emote/setting/panel?business=reply"
        packages = self._interface_request(path)["data"]["all_packages"]
        return packages or []

    def get_sticker(self, sticker_id: int) -> dict:
        url = "/x/emote/package?business=reply&ids={}".format(sticker_id)
        sticker = self._interface_request(url)["data"]["packages"]
        return sticker or sticker

    def get_cover_picture(self, aid) -> Tuple[str, bytes]:
        url = self.get_video(aid)["pic"]
        basename = os.path.basename(url)
        stream = requests.get(url).content
        return basename, stream

    def get_stream_url(self, aid: int, cid: int, quality_options: QualityOptions) -> dict:
        path = f"/x/player/playurl?avid={aid}&cid={cid}&fnver=0&fnval={quality_options.quality_flag}&fourk=1"
        stream_urls = self._interface_request(path)["data"]["dash"]
        audio = stream_urls["audio"][0]
        video = stream_urls["video"][0]
        result_quality = copy.deepcopy(quality_options)

        if quality_options.h265:
            h265_streams = list(filter(lambda stream: stream["codecid"] == 12, stream_urls["video"]))
            if len(h265_streams) > 0:
                video = h265_streams[0]
                result_quality.h265 = True

        result_quality.dolby_vision = (video["id"] == 126)
        result_quality.dolby_audio = (stream_urls.get("dolby", None) is not None)
        if result_quality.dolby_audio:
            audio = stream_urls["dolby"]["audio"][0]
        return {"audio": audio["base_url"], "video": video["base_url"], "quality": result_quality}

    def get_stream(self, url: str, tag: str = "", chunk_size: int = 8192, callback: StreamCallback = None) -> bytes:
        headers = {
            "User-Agent": "Bilibili Freedoooooom/MarkII",
            "Referer": "https://www.bilibili.com/",
            "Accept": "*/*",
            "Icy-MetaData": "1"
        }
        kwargs = {"tag": tag, "chunk_size": chunk_size, "callback": callback, "cookies": self.cookies}
        streamer = BasicStreamer(url, headers, **kwargs)
        return streamer.start()

    def save_stream(self, aid: int, cid: int, quality_options: QualityOptions, dest_file: str,
                    audio_only: bool = False, host: Optional[str] = None,
                    chunk_size: int = 8192, callback: StreamCallback = None) -> subprocess.CompletedProcess:
        from . import codec
        stream_url = self.get_stream_url(aid, cid, quality_options)
        if host is not None:
            stream_url["audio"] = utils.replace_host(stream_url["audio"], host)
            stream_url["video"] = utils.replace_host(stream_url["video"], host)
        audio_stream = self.get_stream(stream_url["audio"], "audio", chunk_size, callback)
        if not audio_only:
            video_stream = self.get_stream(stream_url["video"], "video", chunk_size, callback)
            return codec.merge(audio_stream, video_stream, dest_file)
        quality: QualityOptions = stream_url["quality"]
        return codec.extract_audio(audio_stream, dest_file, quality.dolby_audio)
