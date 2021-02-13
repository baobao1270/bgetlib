class BilibiliAgent:
    import http.cookiejar as cookielib;
    import requests as req;
    from . import Errors as Errors;
    from .Data import FavoritesData, Video, Danmaku, VideoCoverPicture, Mappers;

    def __init__(self):
        self.cookies=None;
    
    def HttpGet(self, url: str, exceptedSatatusCode:int = 200):
        res = self.req.get(url) if (self.cookies == None) else self.req.get(url, cookies=self.cookies);
        if (res.status_code != exceptedSatatusCode):
            raise self.Errors.HTTPError(res.status_code, url, exceptedSatatusCode);
        return res;
    
    def LoginWithCookies(self,
        cookieFileName:str,
        ignoreDiscard:bool = True,
        ignoreExpires:bool = True) -> None:
            self.cookies = self.cookielib.MozillaCookieJar();
            self.cookies.load(
                cookieFileName, ignore_discard=ignoreDiscard, ignore_expires=ignoreExpires);
    
    def GetFavoritesPaged(self, collectionId:int, pageNumber:int = 1) -> list[FavoritesData]:
        url = "https://api.bilibili.com/x/v3/fav/resource/list?media_id={fav_id}&pn={page}&ps=20&order=mtime"
        url = url.format(fav_id=collectionId, page=pageNumber);
        res = self.HttpGet(url).json();
        if (res["code"] != 0):
            raise self.Errors.ResponseCodeError(res["code"], url);
        resultDict = res["data"]["medias"];
        if resultDict == None:
            return [];
        result = self.Mappers.FavoritesDataMapper.MapFrom(resultDict).ToClass(self.FavoritesData);
        return result;

    def GetFavorites(self, collectionId:int) -> list[FavoritesData]:
        page = 1;
        returns = [];
        while page > 0:
            favs = self.GetFavoritesPaged(collectionId, page);
            if len(favs) == 0:
                page = -0x114514; # Can be any value < 0, but I choose a `sodayo` one just for fun.
                break;
            returns += favs;
            page += 1;
        return returns;

    def GetFavoritesNotBefore(self, collectionId:int, notBeforeTimestamp:int) -> list[FavoritesData]:
        page = 1;
        returns = [];
        while page > 0:
            favs = self.GetFavoritesPaged(collectionId, page);
            if len(favs) == 0:
                page = -0x114514;
                break;
            for fav in favs:
                if (fav.favoritedAt < notBeforeTimestamp):
                    page = -0x114514;
                    break;
                returns.append(fav);
            page += 1;
        return returns;
    
    def GetVideoInfo(self, avid:int) -> Video:
        url = "https://api.bilibili.com/x/web-interface/view?aid={}".format(avid);
        res = self.HttpGet(url).json();
        if (res["code"] != 0):
            raise self.Errors.ResponseCodeError(res["code"], url);
        result = self.Mappers.VideoMapper.MapFrom(res["data"]).ToClass(self.Video);
        return result;
    
    def GetRecentDanmaku(self, cid:int) -> Danmaku:
        url = "https://comment.bilibili.com/{}.xml".format(cid);
        res = self.HttpGet(url);
        return self.Danmaku(cid, res.content.decode("utf-8"));
    
    def GetVideoCover(self, avid:int) -> VideoCoverPicture:
        url = "https://api.bilibili.com/x/web-interface/view?aid={}".format(avid);
        res = self.HttpGet(url).json();
        if (res["code"] != 0):
            raise self.Errors.ResponseCodeError(res["code"], url);
        url = res["data"]["pic"];
        res = self.HttpGet(url);
        return self.VideoCoverPicture(avid, url, res.content);
#end class BilibiliAgent
