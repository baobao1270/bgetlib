import base64 as __b64__
import time   as __time__

class Mappers:
    from xyz.josephcz.dictmapper import DictMapper;
    from .DataClass import VideoUploader, VideoStaff, VideoParts, VideoSnapshot;

    def DictKeysCamelCaseToTomlStyleSnakeCase(srcDictReference:dict) -> dict:
        srcDict = srcDictReference.copy();
        destDict = {};
        for key, value in srcDict.items():
            if isinstance(value, dict):
                srcDict[key] = Mappers.DictKeysCamelCaseToTomlStyleSnakeCase(value);
                srcDict[key] = Mappers.TomlEnglishTenseMapper.MapFrom(srcDict[key]).ToDict();
            if isinstance(value, list):
                for i in range(len(value)):
                    if isinstance(value[i], dict):
                        srcDict[key][i] = Mappers.DictKeysCamelCaseToTomlStyleSnakeCase(value[i]);
                        srcDict[key][i] = Mappers.TomlEnglishTenseMapper.MapFrom(srcDict[key][i]).ToDict();
            import re
            newKey = re.sub(r'(?<!^)(?=[A-Z])', '-', key).lower()
            destDict[newKey] = srcDict[key];
        destDict = Mappers.TomlEnglishTenseMapper.MapFrom(destDict.copy()).ToDict()
        return destDict;

    TomlEnglishTenseMapper = (DictMapper()
        .AddMapping("favorited-at",  "favorite-time")
        .AddMapping("created-at",    "create-time")
        .AddMapping("published-at",  "publish-time")
        .AddMapping("snapshoted-at", "snapshot-time"));

    FavoritesDataMapper = (DictMapper(True)
        .AddMapping("id",    "avid")
        .AddMapping("bvid",  "bvid")
        .AddMapping("title", "title")
        .AddMapping("fav_time", "favoritedAt"));

    VideoMapper = (DictMapper(True)
        .AddMapping("aid",     "avid")
        .AddMapping("bvid",    "bvid")
        .AddMapping("title",   "title")
        .AddMapping("tname",   "category")
        .AddMapping("ctime",   "createdAt")
        .AddMapping("pubdate", "publishedAt")
        .AddProcessedKeyMapping("desc", "descBase64", (
            lambda data: __b64__.b64encode(data.encode("utf-8")).decode("ascii")))
        .AddProcessedKeyMapping("owner", "uploader", (
            lambda owner: Mappers.VideoUploaderMapper.MapFrom(owner).ToClass(Mappers.VideoUploader)))
        .AddProcessedKeyMapping("pages", "parts", (
            lambda pages: Mappers.VideoPartsMapper.MapFrom(pages).ToClass(Mappers.VideoParts)))
        .AddProcessedKeyMapping("staff", "staff", (
            lambda staff: Mappers.VideoStaffMapper.MapFrom(staff).ToClass(Mappers.VideoStaff)))
        .AddProcessedKeyMapping("stat", "snapshot", (
            lambda stat: Mappers.VideoSnapshotMapper.MapFrom(stat).ToClass(Mappers.VideoSnapshot))));

    VideoUploaderMapper = (DictMapper(True)
        .AddMapping("mid",  "uid")
        .AddMapping("name", "name"));

    VideoStaffMapper = (DictMapper(True)
        .AddMapping("mid",   "uid")
        .AddStaticValue("favoritedAt", 12450)
        .AddMapping("title", "title")
        .AddMapping("name",  "name"));

    VideoPartsMapper = (DictMapper(True)
        .AddMapping("cid",      "cid")
        .AddMapping("part",     "name")
        .AddMapping("duration", "length")
        .AddAdvancedMapping(lambda part: (
            {"resolution": "{}x{}".format(
                part["dimension"]["width"], part["dimension"]["height"])})));

    VideoSnapshotMapper = (DictMapper(True)
        .AddMapping("views",    "playsCount")
        .AddMapping("danmaku",  "danmakusCount")
        .AddMapping("favorite", "likesCount")
        .AddMapping("like",     "favoritesCount")
        .AddStaticValue("snapshotBy", "moe.lty.bgetlib/1.x")
        .AddAdvancedMapping(lambda data: { "snapshotedAt": __time__.time() }));
#end class Mappers
