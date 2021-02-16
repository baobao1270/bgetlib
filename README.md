# bgetlib
bgetlib is a bilibili API library.

**This is not an official library. Abuse of this library may cause your bilibili account banned.**

This repository is not _bget_. _bget_ is a command line bilibili video downloader tool developed by the same developer of this library, and it uses bgetlib as its core. If you want an _out-of-the-box_ tool or don't know how to code, please see the _bget_ project: https://github.com/baobao1270/bget

## Install
```shell
pip install bgetlib
```

## Usage
```python
import bgetlib;

agent = bgetlib.BilibiliAgent();
agent.LoginWithCookies("cookies.txt");
favs = agent.GetFavorites(467191862);
for fav in favs:
    print("av{}: {}".format(fav.avid, fav.title));
    video = agent.GetVideoInfo(fav.avid);
    for part in video.parts:
        with open("av{}-cid{}-danmaku.xml".format(video.avid, part.cid), "w+", encoding="utf-8") as f:
	    f.write(agent.GetRecentDanmaku(part.cid).GetForamttedString());
```

## References
```python
# <module bgetlib>
class BilibiliAgent:
	def __init__()
	def LoginWithCookies(cookieFileName:str, ignoreDiscard:bool = True, ignoreExpires:bool = True) -> None
	def GetFavoritesPaged(collectionId:int, pageNumber:int = 1) -> list[FavoritesData]
	def GetFavorites(collectionId:int) -> list[FavoritesData]
	def GetFavoritesNotBefore(collectionId:int, notBeforeTimestamp:int) -> list[FavoritesData]
	def GetVideoInfo(avid:int) -> list[Video]
	def GetRecentDanmaku(cid:int) -> Danmaku
	def GetVideoCover(avid:int) -> VideoCoverPicture
class DownloadAgent:
	def __init__(
		cookiesFile:str,
		cookiesIgnoreDiscard = True,
		cookiesIgnoreExpires = True,
		userAgent:str = "Bilibili Freedoooooom/MarkII")
	def GetDownloadUrl(avid:int, cid:int, forceCdn:Union[bool, CDNList] = False) -> Tuple[str, str]
	def GetDownloader(url:str) -> requests.Response
	def GetSizeBytes(requestsInstance:requests.Response) -> int
	def GetContentBinary(url:str) -> bytes
	def GetContentIterated(
		url:str,
		stateUpdateFunc:Callable[
			args:[
				isEnded:bool,
				passthroughData:Any,
				receivedBytes:bytes,
				Tuple[timeUsedSecond:float, downloadedSizeByte:float, downloadSpeedBytePerSecond:float]
			],
			returns:None
		],
		passthroughData:Any = None,
		chunkSize:int = 1024) -> None		
	def SaveToFileByUrl(
		url:str,
		destFilename:str,
		stateUpdateFunc:Union[
			None,
			Callable[
				args:Tuple[timeUsedSecond:float, downloadedSizeByte:float, downloadSpeedBytePerSecond:float],
				returns:None
			]
		] = None,
		chunkSize:int = 1024) -> None
class ConvertAgent:
	def ConvertAgent(ffmpegLocation:str = "ffmpeg", logFile:Union[str, None] = None, downloadedVideoExtName:str = "m4sv", downloadedAudioExtName:str = "m4sa")
	def MergeDash(downloadPathWithoutExt:str, destPathWithoutExt:str, destForamt:str = "mp4") -> subprocess.CompletedProcess
	def AudioToMp3(srcPath:str, destPath:str, bitRateKbps:int = 320) -> subprocess.CompletedProcess
	def AudioToFlac(srcPath:str, destPath:str) -> subprocess.CompletedProcess
	def AudioToAiff(srcPath:str, destPath:str) -> subprocess.CompletedProcess
class Mappers:
	@staticmethod def DictKeysCamelCaseToTomlStyleSnakeCase(srcDictReference:dict) -> dict
class CDNList(Enum):
	SuzhouTencent    = "upos-sz-mirrorcos.bilivideo.com"
	SuzhouQiniu      = "upos-sz-mirrorkodo.bilivideo.com"
	SuzhouKingsoft   = "upos-sz-mirrorks3.bilivideo.com"
	SuzhouHuawei     = "upos-sz-mirrorhw.bilivideo.com"
	SuzhouAkamai     = "upos-sz-mirrorakam.akamaized.net"

# <module bgetlib.Data>
class BaseDataClass(xyz.josephcz.dict2class.DictStdClass):
	def ToDict()
class FavoritesData(BaseDataClass):
	avid:int,
	bvid:str,
	title:str,
	favoritedAt:int[timestamp]
class Video(BaseDataClass):
	avid:int,
	bvid:str,
	title:str,
	category:str,
	createdAt:int[timestamp],
	publishedAt:int[timestamp],
	descBase64:str,
	uploader:VideoUploader,
	staff:list[VideoStaff],
	parts:list[VideoParts],
	snapshot:VideoSnapshot
class VideoUploader(BaseDataClass):
	uid:int, name:str
class VideoStaff(BaseDataClass):
	uid:int, name:str, title:str
class VideoParts(BaseDataClass):
	cid:int, name:str, length:int, resolution:str
class VideoSnapshot(BaseDataClass):
	snapshotBy:str,
	snapshotedAt:int[timestamp],
	playsCount:int,
	danmakusCount:int,
	likesCount:int,
class VideoCoverPicture(BaseDataClass):
	avid:str, sourceUrl:str, data:bytes
class Danmaku:
	cid:str
	def AsStr() -> str
	def AsStrFormatted(indent=" "*4) -> str
	def AsXml() -> xml.etree.ElementTree

# <module bgetlib.Errors>
class OperationNotAllowedError(Exception):
	operation:str, on:str
	def __str__() -> str
class ExternalCallError(Exception):
	cmd:str, exitcode:str, stdout:str, stderr:str
	def __str__() -> str
class NetworkError(Exception):
	def __str__() -> str
class HTTPError(NetworkError):
	status:int, url:str
```

# License
MIT
