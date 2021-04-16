import time
from typing import List, Tuple, Literal, Union, Optional, Dict

from requests import Response

from ._canlogin import CanLogin


class BilibiliAPI(CanLogin):
    import bgetlib.error as _error
    import bgetlib.model as _model

    def __init__(self) -> None:
        super().__init__()

    def _get(self, url: str, excepted_status: int = 200, excepted_code: Optional[int] = None, **kwargs) -> Response:
        import requests
        if self.cookies is None:
            res = requests.get(url, **kwargs)
        else:
            res = requests.get(url, cookies=self.cookies, **kwargs)
        if res.status_code != excepted_status:
            raise self._error.HTTPError(url, res.status_code, excepted_status)
        if excepted_code is not None:
            if res.json()["code"] != 0:
                raise self._error.ResponseCodeError(url, res.json()["code"])
        return res

    def get_favorites(self, favorite_id: int, page: int = 1) -> list[_model.FavoriteItem]:
        url = "https://api.bilibili.com/x/v3/fav/resource/list?media_id={}&pn={}&ps=20&order=mtime"
        url = url.format(favorite_id, page)
        res_json = self._get(url, excepted_code=0).json()
        medias = res_json["data"]["medias"]
        if medias is None:
            return []
        return [
            self._model.FavoriteItem(
                avid=media["id"],
                bvid=media["bvid"],
                title=media["title"],
                favorite_at=media["fav_time"]
            ) for media in medias
        ]

    def get_favorites_all(self, favorite_id: int) -> list[_model.FavoriteItem]:
        page = 1
        favorites = []
        while True:
            page_favorites = self.get_favorites(favorite_id, page)
            if len(page_favorites) == 0:
                break
            favorites += page_favorites
            page += 1
        return favorites

    def get_favorites_nbf(self, favorite_id: int, from_timestamp: int) -> list[_model.FavoriteItem]:
        page = 1
        favorites = []
        while True:
            page_favorites = self.get_favorites(favorite_id, page)
            if len(page_favorites) == 0:
                break
            for v in page_favorites:
                if v.favorite_at < from_timestamp:
                    break
                favorites.append(v)
            page += 1
        return favorites

    def list_favourite_folders(self, uid: int) -> Dict[int, str]:
        url = "https://api.bilibili.com/x/v3/fav/folder/created/list-all?up_mid={}".format(uid)
        res_json = self._get(url).json()
        return {i["id"]: i["title"] for i in res_json["data"]["list"]}

    def get_video(self, avid: int) -> _model.VideoWithPart:
        url = "https://api.bilibili.com/x/web-interface/view?aid={}".format(avid)
        res_json = self._get(url, excepted_code=0).json()
        return self._model.VideoWithPart(res_json["data"], int(time.time()))

    def get_live_danmaku(self, cid: int) -> str:
        url = "https://comment.bilibili.com/{}.xml".format(cid)
        return self._get(url).text

    def _ranking_factory(self, url: str) -> Tuple[int, List[_model.Video]]:
        res_json = self._get(url, excepted_code=0).json()
        videos = [
            self._model.Video.factory(v, int(time.time())) for v in res_json["data"]["archives"]
        ]
        count = res_json["data"]["page"]["count"]
        return count, videos

    def get_category(self, category_id: int, page: int = 1) -> Tuple[int, List[_model.Video]]:
        url = "https://api.bilibili.com/x/web-interface/newlist?type=0&ps=20&pn={}&rid={}".format(page, category_id)
        return self._ranking_factory(url)

    def get_category_latest(self, category_id: int, page: int = 1) -> Tuple[int, List[_model.Video]]:
        url = "https://api.bilibili.com/x/web-interface/dynamic/region?ps=5&pn={}&rid={}".format(page, category_id)
        return self._ranking_factory(url)

    def get_tag(self, category_id: int, tag_id: int, page: int = 1) -> Tuple[int, List[_model.Video]]:
        url = "https://api.bilibili.com/x/tag/ranking/archives?type=0&ps=20&pn={}&rid={}&tag_id={}".format(
            page, category_id, tag_id
        )
        return self._ranking_factory(url)

    def get_tag_latest(self, category_id: int, tag_id: int, page: int = 1) -> Tuple[int, List[_model.Video]]:
        url = "https://api.bilibili.com/x/web-interface/dynamic/tag?ps=5&pn={}&rid={}&tag_id={}".format(
            page, category_id, tag_id
        )
        return self._ranking_factory(url)

    def get_category_hot(self, category_id: int, day: Union[Literal[3], Literal[7]] = 7) -> List[_model.VideoBase]:
        url = "https://api.bilibili.com/x/web-interface/ranking/region?rid={}&day={}&original=0".format(
            category_id, day
        )
        res_json = self._get(url, excepted_code=0).json()
        return [self._model.VideoBase(v["aid"], v["bvid"], v["title"]) for v in res_json["data"]]

    def get_tag_hot(self, category_id: int, tag_id: int) -> List[_model.VideoBase]:
        url = "https://api.bilibili.com/x/web-interface/ranking/tag?rid={}&tag_id={}".format(
            category_id, tag_id
        )
        res_json = self._get(url, excepted_code=0).json()
        return [self._model.VideoBase(v["aid"], v["bvid"], v["title"]) for v in res_json["data"]]

    def list_emote_packages(self) -> Dict[int, str]:
        url = "https://api.bilibili.com/x/emote/setting/panel?business=reply"
        res_json = self._get(url, excepted_code=0).json()
        return {pkg["id"]: pkg["text"] for pkg in res_json["data"]["all_packages"]}

    def get_emotes(self, pkg_id: int) -> Dict[str, _model.Emote]:
        url = "https://api.bilibili.com/x/emote/package?business=reply&ids={}".format(pkg_id)
        res_json = self._get(url, excepted_code=0).json()
        if len(res_json["data"]["packages"]) < 0:
            return {}
        return {e["text"]: self._model.Emote(e["url"], e["text"]) for e in res_json["data"]["packages"][0]["emote"]}
