from dataclasses import dataclass, field
from typing import Dict, Optional

import requests

from .__version__ import __version__


@dataclass
class VideoUploader:
    uid: int
    name: str


@dataclass
class VideoStaff:
    uid: int
    name: str
    title: str


@dataclass
class VideoPart:
    cid: int
    name: str
    duration: int


@dataclass
class VideoSnapshot:
    snapshot_at: int
    plays: int
    danmakus: int
    likes: int
    favorites: int
    snapshot_by: str = "bgetlib/{0}".format(__version__)


@dataclass
class VideoCoverPicture:
    avid: str
    url: str

    def get_extname(self):
        return self.url.split(".")[-1]

    def download(self) -> bytes:
        return requests.get(self.url).content


@dataclass
class VideoBase:
    avid: int
    bvid: str
    title: str


@dataclass
class Video(VideoBase):
    category: str
    created_at: int
    published_at: int
    desc: str
    cover: VideoCoverPicture
    uploader: VideoUploader
    snapshot: VideoSnapshot

    @staticmethod
    def factory(data: Dict, current_time: int):
        return Video(
            avid=data["aid"],
            bvid=data["bvid"],
            title=data["title"],
            category=data["tname"],
            created_at=data["ctime"],
            published_at=data["pubdate"],
            desc=data["desc"],
            cover=VideoCoverPicture(data["aid"], data["pic"]),
            uploader=VideoUploader(uid=data["owner"]["mid"], name=data["owner"]["name"]),
            snapshot=VideoSnapshot(
                snapshot_at=current_time,
                plays=data["stat"]["view"],
                danmakus=data["stat"]["danmaku"],
                likes=data["stat"]["like"],
                favorites=data["stat"]["favorite"]
            )
        )


@dataclass
class VideoWithPart(Video):
    staff: Optional[list[VideoStaff]]
    parts: list[VideoPart]

    def __init__(self, data: Dict, current_time: int):
        vb = Video.factory(data, current_time)
        self.__dict__.update(vb.__dict__)
        self.staff=None if data.get("staff") is None else [
            VideoStaff(
                uid=i["mid"],
                name=i["name"],
                title=i["title"]
            ) for i in data["staff"]
        ]
        self.parts = [
            VideoPart(
                cid=p["cid"],
                name=p["part"],
                duration=p["duration"]
            ) for p in data["pages"]
        ]


@dataclass
class FavoriteItem(VideoBase):
    favorite_at: int


@dataclass
class Emote:
    url: str
    name: str

    def download(self) -> bytes:
        return requests.get(self.url).content


@dataclass
class DownloadProgress:
    total_bytes: int
    start: float
    slice_size: int
    url: str
    slice_start: float = field(init=False)
    end: float = field(init=False)
    downloaded_bytes: int = 0
    tag: Optional[str] = None
    finished = False

    def __post_init__(self) -> None:
        self.slice_start = self.start
        self.end = self.start

    def update_time(self) -> None:
        import time
        self.slice_start = self.end
        self.end = time.time()
        downloaded_bytes = self.downloaded_bytes + self.slice_size
        if downloaded_bytes > self.total_bytes:
            downloaded_bytes = self.total_bytes
        self.downloaded_bytes = downloaded_bytes

    def used_sec(self) -> float:
        used = self.end - self.start
        if used < 0.001:
            return 0.001
        return used

    def avg_speed(self) -> float:
        return self.downloaded_bytes / self.used_sec()

    def speed(self) -> float:
        t = self.end - self.slice_start
        if t < 0.001:
            t = 0.001
        return self.slice_size / t
