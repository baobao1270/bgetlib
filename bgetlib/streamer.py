import re
import copy
import requests
from abc import ABC, abstractmethod
from typing import Dict, Optional, Callable
from .models import StreamCallback, DownloadProgress


class IStreamer(ABC):
    @classmethod
    def __init__(cls, url: str, headers: Dict[str, str], **kwargs):
        cls.url = url
        cls.headers = headers

    @abstractmethod
    def start(self) -> bytes:
        pass


class BasicStreamer(IStreamer):
    def __init__(self, url: str, headers: Dict[str, str], **kwargs):
        super().__init__(url, headers)
        self.tag: str = kwargs.get("tag", "")
        self.callback: StreamCallback = kwargs.get("callback", lambda _: None)
        self.chunk_size: int = kwargs.get("chunk_size", 8192)

    @staticmethod
    def range_slice(size: int, slice_size: int):
        slices = list()
        last_slice = size % slice_size
        integer_slices = size - last_slice
        for i in range(0, integer_slices, slice_size):
            slices.append((i, i + slice_size - 1))
        if last_slice != 0:
            slices.append((integer_slices, size - 1))
        return slices

    def start(self) -> bytes:
        head = requests.head(self.url, headers=self.headers)
        if head.status_code == 404:
            return self.download_legacy()

        size = int(head.headers["content-length"])
        slices = BasicStreamer.range_slice(size, self.chunk_size * 1024)
        stream = bytes()
        process = DownloadProgress(self.tag, size)

        try:
            while len(stream) != size:
                stream = bytes()
                for start, end in slices:
                    stream += self.download_slice(start, end, size, process, len(stream))
                    process.update(len(stream))
                    self.callback(process)
        except (KeyError, AssertionError):
            return self.download_legacy()
        process.done = True
        process.update(len(stream))
        self.callback(process)
        return stream

    def download_legacy(self) -> bytes:
        while True:
            buffer = bytes()
            with requests.get(self.url, headers=self.headers, stream=True) as r:
                size = int(r.headers["content-length"])
                process = DownloadProgress(self.tag, size)
                for chunk in r.iter_content(chunk_size=self.chunk_size):
                    if chunk:
                        buffer += chunk
                        process.update(len(buffer))
                        self.callback(process)
            if len(buffer) != size:
                continue
            process.done = True
            process.update(size)
            self.callback(process)
            return buffer

    def download_slice(self, start: int, end: int, size: int, process: DownloadProgress, base_size: int) -> bytes:
        headers = copy.copy(self.headers)
        headers["range"] = f"bytes={start}-{end}"
        slice_size = end - start + 1
        buffer = bytes()
        while len(buffer) != slice_size:
            buffer = bytes()
            try:
                with requests.get(self.url, headers=headers, stream=True) as r:
                    content_range = re.match(r"^bytes (\d*)-(\d*)/(\d+)$", r.headers["content-range"])
                    assert start == (0 if (content_range.group(1) == '') else int(content_range.group(1)))
                    assert end == (0 if (content_range.group(2) == '') else int(content_range.group(2)))
                    assert size == int(content_range.group(3))
                    for chunk in r.iter_content(chunk_size=self.chunk_size):
                        if chunk:
                            buffer += chunk
                            process.update(base_size + len(buffer))
                            self.callback(process)
            except requests.exceptions.ConnectionError:
                buffer = self.download_slice(start, end, size, process, base_size)
        return buffer


class MultiThreadStreamer(IStreamer):
    def __init__(self, url: str, headers: Dict[str, str], **kwargs):
        super().__init__(url, headers)
        self.threads: int = kwargs.get("threads", 16)
        self.tag: str = kwargs.get("tag", "")
        self.callback: StreamCallback = kwargs.get("callback", None)
        self.chunk_size: int = kwargs.get("chunk_size", 8192)

    def start(self) -> bytes:
        raise NotImplementedError


__names__ = {
    "BasicStreamer": BasicStreamer,
    "MultiThreadStreamer": MultiThreadStreamer
}
