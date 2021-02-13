class DownloadAgent:
    from . import Errors as Errors;
    from .CDNList import CDNList;
    from xyz.josephcz.dict2class import DictStdClass;
    from xyz.josephcz.dictmapper import DictMapper;
    from typing import Union, Callable, Any, Tuple;

    def __init__(self, cookiesFile:str, cookiesIgnoreDiscard = True, cookiesIgnoreExpires = True, userAgent:str = "Bilibili Freedoooooom/MarkII"):
        import http.cookiejar as cookielib;
        self.cookies = cookielib.MozillaCookieJar();
        self.cookies = self.cookies.load(cookiesFile, ignore_discard=cookiesIgnoreDiscard, ignore_expires=cookiesIgnoreExpires);
        self.headers = {
            "User-Agent": userAgent,
            "Referer": "https://www.bilibili.com/",
            "Accept": "*/*",
            "Icy-MetaData": "1"
        };

    def GetHighestResolutionDownloadUrlByJson(self, json:str, keyInDash:str, forceCdn:Union[bool, CDNList] = False) -> str:
        medias = json["data"]["dash"][keyInDash];
        medias.sort(key=(lambda x: x["id"]), reverse=True);
        url = medias[0]["baseUrl"];
        if forceCdn == False:
            return url;
        import urllib.parse as urllib;
        parsedUrl = urllib.urlparse(url)
        parsedUrl = parsedUrl._replace(netloc=forceCdn.value);
        url = urllib.urlunparse(parsedUrl);
        return url;

    def GetDownloadUrl(self, avid:int, cid:int, forceCdn:Union[bool, CDNList] = False) -> Tuple[str, str]:
        import requests;
        url = "https://api.bilibili.com/x/player/playurl?avid={avid}&cid={cid}&fnver=0&fnval=16&fourk=1";
        url = url.format(avid=avid, cid=cid);
        res = requests.get(url, headers=self.headers, cookies=self.cookies);
        if res.status_code != 200:
            raise self.Errors.HTTPError(res.status_code, url);
        resJson = res.json();
        if resJson["code"] != 0:
            raise self.Errors.ResponseCodeError(res.json()["code"], url);
        return self.GetHighestResolutionDownloadUrlByJson(resJson, "video", forceCdn), self.GetHighestResolutionDownloadUrlByJson(resJson, "audio", forceCdn);

    def GetDownloader(self, url:str):
        import requests;
        return requests.get(url, headers=self.headers, cookies=self.cookies, stream=True);

    def GetSizeBytes(self, requestsInstance) -> int:
        return int(requestsInstance.headers['content-length']);

    def GetContentBinary(self, url:str) -> bytes:
        import requests;
        return requests.get(url, headers=self.headers, cookies=self.cookies).content;

    def GetContentIterated(self, url:str, stateUpdateFunc:Callable[[bool, Any, bytes, Tuple[float, float, float]], None], passthroughData = None, chunkSize:int = 1024) -> None:
        import time;
        downloader = self.GetDownloader(url);
        timeStart = time.time();
        timeUsed = 0.001;
        downloadedSizeByte = 0;
        for chunk in downloader.iter_content(chunk_size=chunkSize):
            if chunk:
                timeUsed = time.time() - timeStart + 0.001;
                downloadedSizeByte += chunkSize;
                downloadSpeedBytePerSecond = downloadedSizeByte / timeUsed;
                stateUpdateFunc(False, passthroughData, chunk, (timeUsed, downloadedSizeByte, downloadSpeedBytePerSecond,));
        stateUpdateFunc(True, passthroughData, None, (timeUsed, downloadedSizeByte, 0,));

    def SaveToFileByUrl(self, url:str, destFilename:str, stateUpdateFunc:Union[None, Callable[[float, float, float], None]] = None, chunkSize:int = 1024) -> None:
        def saveToFile(isEnded, data, chunk, speedInfoTuple):
            fd, stateUpdater = data;
            stateUpdaterInputTimeUsed, stateUpdaterDownloadedSizeByte, stateUpdaterSpeedBytePerSecond = speedInfoTuple;
            if not isEnded:
                fd.write(chunk);
                if stateUpdater != None:
                    stateUpdater(stateUpdaterInputTimeUsed, stateUpdaterDownloadedSizeByte, stateUpdaterSpeedBytePerSecond);
        with open(destFilename, "wb+") as f:
            self.GetContentIterated(url, saveToFile, (f, stateUpdateFunc));
#end class DownloadAgent
