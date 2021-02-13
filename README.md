## Install
```shell
pip install bgetlib
```

## Usage
```python
import bgetlib as BGet;

agent = BGet.BilibiliAgent();
agent.LoginWithCookies("cookies.txt");
favs = agent.GetFavorites(12345678);
first_video = GetVideoInfo(favs[0].avid);
danmaku = GetRecentDanmaku(first_video.avid);
cover_pic_bytes = GetVideoCover(first_video.avid).data;
```

## References
```python
class BilibiliAgent:
	def BilibiliAgent()
	def LoginWithCookies(cookieFileName:str, ignoreDiscard:bool = True, ignoreExpires:bool = True) -> None
	def GetFavoritesPaged(collectionId:int, pageNumber:int = 1) -> list[FavoritesData]
	def GetFavorites(collectionId:int) -> list[FavoritesData]
	def GetFavoritesNotBefore(collectionId:int, notBeforeTimestamp:int) -> list[FavoritesData]
	def GetVideoInfo(avid:int) -> list[Video]
	def GetRecentDanmaku(cid:int) -> Danmaku
	def GetVideoCover(avid:int) -> VideoCoverPicture
class DownloadAgent:
	def DownloadAgent(cookiesFile:str, cookiesIgnoreDiscard = True, cookiesIgnoreExpires = True, userAgent:str = "bili-hd2/3100010 Cronet/81.4044.156 Darwin/20.2.0")
	def GetDownloadUrl(avid:int, cid:int, forceCdn:Union[bool, CDNList] = False) -> Tuple[str, str]
	def GetDownloader(url:str) -> requests.Response
	def GetSizeBytes(requestsInstance:requests.Response) -> int
	def GetContentBinary(url:str) -> bytes
	def GetContentIterated(self, url:str, stateUpdateFunc:Callable[[bool, Any, bytes, Tuple[float, float, float]], None], passthroughData:Any = None, chunkSize:int = 1024) -> None
		stateUpdateFunc(isEnded:bool, passthroughData:Any, (timeUsedSecond, downloadedSizeByte, downloadSpeedBytePerSecond))
	def SaveToFileByUrl(self, url:str, destFilename:str, stateUpdateFunc:Union[None, Callable[[float, float, float], None]] = None, chunkSize:int = 1024) -> None
		stateUpdateFunc(timeUsedSecond, downloadedSizeByte, downloadSpeedBytePerSecond)
class ConvertAgent:
	def ConvertAgent(ffmpegLocation:str = "ffmpeg", logFile:Union[str, None] = None, downloadedVideoExtName = "m4sv", downloadedAudioExtName = "m4sa")
	def MergeDash(downloadPathWithoutExt:str, destPathWithoutExt:str, destForamt = "mp4") -> subprocess.CompletedProcess
	def AudioToMp3(srcPath:str, destPath:str, bitRateKbps:int = 320) -> subprocess.CompletedProcess
	def AudioToFlac(srcPath:str, destPath:str) -> subprocess.CompletedProcess
	def AudioToAiff(srcPath:str, destPath:str) -> subprocess.CompletedProcess
class Mappers:
	def "static" DictKeysCamelCaseToTomlStyleSnakeCase(srcDictReference:dict) -> dict
class CDNList(Enum):
    SuzhouTencent    = "upos-sz-mirrorcos.bilivideo.com"
    SuzhouQiniu      = "upos-sz-mirrorkodo.bilivideo.com"
    SuzhouKingsoft   = "upos-sz-mirrorks3.bilivideo.com"
    SuzhouHuawei     = "upos-sz-mirrorhw.bilivideo.com"
    SuzhouAkamai     = "upos-sz-mirrorakam.akamaized.net"

# Data
class BaseDataClass(xyz.josephcz.dict2class.DictStdClass):
	def ToDict()
	class FavoritesData(BaseDataClass):
		avid:int, bvid:str, title:str, favoritedAt:int[timestamp]
	class Video(BaseDataClass):
		avid:int, bvid:str, title:str, category:str,
		createdAt:int[timestamp], publishedAt:int[timestamp], descBase64:str,
		uploader:VideoUploader,
		staff:list[VideoStaff],
		parts:list[VideoParts],
		snapshot:VideoSnapshot
	class VideoUploader(BaseDataClass):
		uid:int, name:str
	class VideoStaff(BaseDataClass):
		uid:int, name:str, title:str
	class VideoParts(BaseDataClass):
		cid:int, name:str, length:int, resolution:str[regex("^\d+x\d+$")]
	class VideoSnapshot(BaseDataClass):
		snapshotBy:str,
		snapshotedAt:int[timestamp],
		playsCount:int,
		danmakusCount:int,
		likesCount:int, 
		ikesCount:int
	class VideoCoverPicture(BaseDataClass):
		avid:str, sourceUrl:str, data:bytes
class Danmaku:
	cid:str
	def AsStr(self) -> str
	def AsStrFormatted(self, indent=" "*4) -> str
	def AsXml(self)

# Errors:
class OperationNotAllowedError(Exception)
class NetworkError(Exception):
	class HTTPError(NetworkError):
		status:int, url:str
class ExternalCallError(Exception):
    cmd:str, exitcode:str, stdout:str, stderr:str
```

# License
MIT
