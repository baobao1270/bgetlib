import os.path
import shutil
from subprocess import CompletedProcess
from typing import Union
from uuid import UUID


class Transcoder:
    import bgetlib.error as _error
    import bgetlib.consts as _CONST_

    def __init__(self, temp_dir: str, file_id: UUID, ffmpeg_location: str = "ffmpeg") -> None:
        self.file_id = file_id
        self.temp_dir = temp_dir
        self.ffmpeg = ffmpeg_location

    def save_dash(self, dest: str) -> None:
        args = '-i "{file_id}.{v_ext}" -i "{file_id}.{a_ext}" -c copy "{file_id}.{m_ext}"'.format(
            file_id=self.file_id,
            v_ext=self._CONST_.DASH_VIDEO_EXTENSION,
            a_ext=self._CONST_.DASH_AUDIO_EXTENSION,
            m_ext=self._CONST_.DASH_MERGE_EXTENSION
        )
        self._run(args)
        self._copy(self._CONST_.DASH_MERGE_EXTENSION, dest)

    def encode_audio_to(self, dest_format: str, dest: str, options: str = "") -> None:
        self._encode_to(self._CONST_.DASH_AUDIO_EXTENSION, dest_format, dest, options)

    def encode_video_to(self, dest_format: str, dest: str, options: str = "") -> None:
        self._encode_to(self._CONST_.DASH_MERGE_EXTENSION, dest_format, dest, options)

    def to_mp3(self, dest: str, bitrate_kbps: int = 320) -> None:
        self.encode_audio_to("mp3", dest, "-ab {}".format(bitrate_kbps))

    def to_flac(self, dest: str) -> None:
        self.encode_audio_to("flac", dest)

    def to_aiff(self, dest: str) -> None:
        self.encode_audio_to("aiff", dest)

    def to_flv(self, dest: str) -> None:
        self.encode_video_to("flv", dest, "-c copy")

    def _copy(self, dest_format: str, dest: str) -> None:
        src = os.path.join(self.temp_dir, "{}.{}".format(self.file_id, dest_format))
        shutil.copy2(src, dest)

    def _encode_to(self, src_format: str, dest_format: str, dest: str, options: str = "") -> None:
        if dest_format != src_format:
            self._convert(src_format, dest_format, options)
        self._copy(dest_format, dest)

    def _convert(self, src_format: str, dest_format: str,
                 options: str = "") -> Union[CompletedProcess, CompletedProcess[bytes]]:
        args = '-i "{file_id}.{src_format}" {options} "{file_id}.{dest_format}"'.format(
            file_id=self.file_id,
            src_format=src_format,
            dest_format=dest_format,
            options=options
        )
        return self._run(args)

    def _run(self, args: str) -> Union[CompletedProcess, CompletedProcess[bytes]]:
        cmd = '"{ffmpeg}" -y -hide_banner {args}'.format(ffmpeg=self.ffmpeg, args=args)
        import subprocess
        result = subprocess.run(cmd, cwd=self.temp_dir, capture_output=True)
        self._write_log(args, result)
        if result.returncode != 0:
            raise self._error.ExternalCallError(
                cmd, result.returncode,
                result.stdout.decode("utf-8"),
                result.stderr.decode("utf-8")
            )
        return result

    def _write_log(self, args: str, result: Union[CompletedProcess, CompletedProcess[bytes]]) -> None:
        import time
        log_prefix = "{}-{}".format(self.file_id, time.strftime("%Y-%m-%d-%H-%M-%S"))
        log_prefix = os.path.join(self.temp_dir, log_prefix)
        with open("{}-{}.log".format(log_prefix, "stderr"), "ab+") as logfile:
            logfile.write("COMMAND: {}\r\n\r\n".format(args).encode("utf-8"))
            logfile.write(result.stderr)
        with open("{}-{}.log".format(log_prefix, "stdout"), "ab+") as logfile:
            logfile.write("COMMAND: {}\r\n\r\n".format(args).encode("utf-8"))
            logfile.write(result.stdout)
