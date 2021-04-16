import hashlib
import uuid
from unittest import TestCase

from _common import *
from bgetlib.model import DownloadProgress


def download_show(progress: DownloadProgress):
    if progress.finished:
        output("\nFinished download {}\n".format(progress.url))
        return None
    output(" "*60, end="\r")
    output(
        "{}: {:.2f}/{:.2f}MB, avg={:.2f}MB/s, diff={:.2f}MB/s".format(
            progress.tag,
            progress.downloaded_bytes / 1024 / 1024,
            progress.total_bytes / 1024 / 1024,
            progress.avg_speed() / 1024 / 1024,
            progress.speed() / 1024 / 1024
        ),
        end="\r"
    )


class DownloadTranscodeTestCase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        v = get_api(login=True).get_video(V_ID_NORMAL)
        create_temp_dir()
        dl = get_dl()
        output("=" * 60)

        @dl.callback_func
        def _callback(progress: DownloadProgress):
            download_show(progress)
        file_id = dl.download(v.avid, v.parts[0].cid, DOWNLOAD_TEMP_DIR)
        output("file_id={}".format(file_id))
        cls.transcoder = bgetlib.Transcoder(DOWNLOAD_TEMP_DIR, file_id)
        output("=" * 60)

    def test_merge(self) -> None:
        filename = "{}/av{}.mp4".format(DOWNLOAD_TEMP_DIR, V_ID_NORMAL)
        self.transcoder.save_dash(filename)
        with open(filename, "rb") as f:
            file_hash = hashlib.sha1(f.read()).hexdigest()
            output("hash={}".format(file_hash))
            self.assertEqual(file_hash, DOWNLOAD_DASH_ASSERT_HASH)

    def test_conv_aiff(self) -> None:
        filename = "{}/av{}.aiff".format(DOWNLOAD_TEMP_DIR, V_ID_NORMAL)
        self.transcoder.to_aiff(filename)
        with open(filename, "rb") as f:
            file_hash = hashlib.sha1(f.read()).hexdigest()
            output("hash={}".format(file_hash), end="...")
            self.assertEqual(file_hash, CONVERT_AIFF_ASSERT_HASH)

    def test_conv_flac(self) -> None:
        filename = "{}/av{}.flac".format(DOWNLOAD_TEMP_DIR, V_ID_NORMAL)
        self.transcoder.to_flac(filename)
        with open(filename, "rb") as f:
            file_hash = hashlib.sha1(f.read()).hexdigest()
            output("hash={}".format(file_hash), end="...")
            self.assertEqual(file_hash, CONVERT_FLAC_ASSERT_HASH)

    def test_conv_mp3(self) -> None:
        filename = "{}/av{}.mp3".format(DOWNLOAD_TEMP_DIR, V_ID_NORMAL)
        self.transcoder.to_mp3(filename)
        with open(filename, "rb") as f:
            file_hash = hashlib.sha1(f.read()).hexdigest()
            output("hash={}".format(file_hash), end="...")
            self.assertEqual(file_hash, CONVERT_MP3_ASSERT_HASH)

    def test_conv_flv(self) -> None:
        filename = "{}/av{}.flv".format(DOWNLOAD_TEMP_DIR, V_ID_NORMAL)
        dash_temp = "{}/av{}-temp.mp4".format(DOWNLOAD_TEMP_DIR, V_ID_NORMAL)
        self.transcoder.save_dash(dash_temp)
        self.transcoder.to_flv(filename)
        with open(filename, "rb") as f:
            file_hash = hashlib.sha1(f.read()).hexdigest()
            output("hash={}".format(file_hash), end="...")
            self.assertEqual(file_hash, CONVERT_FLV_ASSERT_HASH)
