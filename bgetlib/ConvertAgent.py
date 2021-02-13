class ConvertAgent:
    from typing import Union;
    from .Errors import ExternalCallError;

    def __init__(self, ffmpegLocation:str = "ffmpeg", logFile:Union[str, None] = None, downloadedVideoExtName = "m4sv", downloadedAudioExtName = "m4sa"):
        self.ffmpeg = ffmpegLocation;
        self.log = logFile;
        self.extnameVideo = downloadedVideoExtName;
        self.extnameAudio = downloadedAudioExtName;

    def MergeDash(self, downloadPathWithoutExt:str, destPathWithoutExt:str, destForamt = "mp4"):
        args = '-i "{v}.{m4sv}" -i "{a}.{m4sa}" -c copy "{dest}.{mp4}"'.format(
            ffmpeg=self.ffmpeg, v=downloadPathWithoutExt, a=downloadPathWithoutExt, dest=destPathWithoutExt,
            m4sv=self.extnameVideo, m4sa=self.extnameAudio, mp4=destForamt);
        return self.RunFFMpeg(args);

    def Convert(self, srcPath:str, srcFormat:str, destPath:str, destFormat:str, options:str = ""):
        args = '-i "{src}.{srcf}" {options} "{dest}.{destf}"'.format(src=srcPath, dest=destPath, srcf=srcFormat, destf=destFormat, options=options);
        return self.RunFFMpeg(args);

    def AudioToMp3(self, srcPath:str, destPath:str, bitRateKbps:int = 320):
        return self.Convert(srcPath, self.extnameAudio, destPath, "mp3", "-ab {}".format(bitRateKbps));

    def AudioToFlac(self, srcPath:str, destPath:str):
        return self.Convert(srcPath, self.extnameAudio, destPath, "flac");

    def AudioToAiff(self, srcPath:str, destPath:str):
        return self.Convert(srcPath, self.extnameAudio, destPath, "aiff");

    def RunFFMpeg(self, args:str):
        cmd = '"{ffmpeg}" -y -hide_banner {args}'.format(ffmpeg=self.ffmpeg, args=args);
        import subprocess;
        result = subprocess.run(cmd, capture_output=True);
        if self.log != None:
            import time;
            ms = (str(int((time.time() - int(time.time())) * 100000000))).zfill(8);
            stderrlog = self.log + time.strftime("-%Y-%m-%d-%H-%M-%S-") + ms + "-stderr.log";
            stdoutlog = self.log + time.strftime("-%Y-%m-%d-%H-%M-%S-") + ms + "-stdout.log";
            with open(stderrlog, "ab+") as logfile:
                logfile.write("COMMAND: {}\r\n\r\n".format(args).encode("utf-8"));
                logfile.write(result.stderr);
            with open(stdoutlog, "ab+") as logfile:
                logfile.write("COMMAND: {}\r\n\r\n".format(args).encode("utf-8"));
                logfile.write(result.stdout);
        if result.returncode != 0:
            raise self.ExternalCallError(cmd, result.returncode, result.stdout.decode("utf-8"), result.stderr.decode("utf-8"));
        return result;
#end class ConvertAgent