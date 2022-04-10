import time
from dataclasses import dataclass, field
from typing import Optional, Callable, List, Union, Dict


@dataclass
class DownloadProgress:
    """The download process model, updated to each callback"""

    #: The tag of `DownloadProgress` to identify it
    tag: str

    #: Total bytes to download
    total: int

    #: The f-string to format the percentage of complete
    percent_format: str = field(default="{:.2%}", init=False)

    #: The f-string to format the progress bar
    bar_format: str = field(default_factory=lambda: ("[", 20, "]"), init=False)

    #: Finished bytes
    finished: int = field(init=False)

    #: Timestamp of when the download start
    start_at: float = field(init=False)

    ticks: List[Dict[str, Union[int, float]]] = field(init=False)

    #: Is the download done
    done: bool = field(init=False, default=False)

    def __post_init__(self):
        self.finished = 0
        self.start_at = time.time()
        self.ticks = [{"time": self.start_at, "byte": self.finished}]

    def update(self, finished: int) -> None:
        self.finished = min(self.total, finished)
        self.ticks.append({"time": time.time(), "byte": self.finished})

    #: Bytes left to download
    @property
    def left(self) -> int:
        return min(0, self.total - self.finished)

    #: The percentage of complete, form 0 to 1
    @property
    def frac(self) -> float:
        return self.finished / self.total

    #: The well-formatted percentage string
    @property
    def percent(self) -> str:
        return self.percent_format.format(self.frac)

    #: The progress bar
    @property
    def bar(self) -> str:
        start, length, end = self.bar_format
        bar = '=' * int(self.frac * length - 1) + ">"
        formatter = "{" + f":<{length}" + "}"
        return f"{start}{formatter.format(bar)}{end}"

    #: Average speed in bytes / second
    @property
    def average_speed(self) -> float:
        duration = self.ticks[-1]["time"] - self.start_at
        if duration <= 0:
            return 0
        return self.finished / duration

    #: Speed of last chunk in bytes / second
    @property
    def speed(self) -> float:
        if len(self.ticks) < 2:
            return 0
        t = self.ticks[-1]["time"] - self.ticks[-2]["time"]
        d = self.ticks[-1]["byte"] - self.ticks[-2]["byte"]
        if t <= 0:
            return 0
        return d / t


StreamCallback = Optional[Callable[[DownloadProgress], None]]

QUALITY_FLAG_DASH = 16
QUALITY_FLAG_HDR = 64
QUALITY_FLAG_4K = 128
QUALITY_FLAG_DOLBY_AUDIO = 256
QUALITY_FLAG_DOLBY_VISION = 512
QUALITY_FLAG_8K = 1024


@dataclass
class QualityOptions:
    """Quality options of requesting a video"""

    #: Enable H.265
    h265: bool = field(default=True)

    #: Enable HDR
    hdr: bool = field(default=True)

    #: Enable Dolby Audio (AC-3 or EC-3)
    dolby_audio: bool = field(default=False)

    #: Enable Dolby Vision HDR
    dolby_vision: bool = field(default=False)

    #: Enable 8K QHD
    qhd_8k: bool = field(default=True)

    @property
    def quality_flag(self):
        flag = QUALITY_FLAG_DASH | QUALITY_FLAG_8K
        if self.hdr or self.dolby_vision or self.dolby_vision or self.qhd_8k:
            self.h265 = True
        if self.hdr:
            flag = flag | QUALITY_FLAG_HDR
        if self.dolby_audio:
            flag = flag | QUALITY_FLAG_DOLBY_AUDIO
        if self.dolby_vision:
            flag = flag | QUALITY_FLAG_DOLBY_VISION
        if self.qhd_8k:
            flag = flag | QUALITY_FLAG_8K
        return flag
