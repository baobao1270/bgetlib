from xyz.josephcz.dict2class import DictStdClass as __DictStdClass__;

class BaseDataClass(__DictStdClass__):
    def ToDict(self):
        import copy;
        rdict = copy.deepcopy(self).__dict__.copy();
        for k, v in rdict.items():
            if isinstance(v, __DictStdClass__):
                rdict[k] = v.ToDict();
            if isinstance(v, list):
                for i in range(len(v)):
                    if isinstance(v[i], __DictStdClass__):
                        rdict[k][i] = v[i].ToDict();
        return rdict;

class Video(BaseDataClass):
    pass;
#end class Video

class VideoUploader(BaseDataClass):
    pass;
#end class VideoUploader

class VideoStaff(BaseDataClass):
    pass;
#end class VideoStaff

class VideoParts(BaseDataClass):
    pass;
#end class VideoParts

class VideoSnapshot(BaseDataClass):
    pass;
#end class VideoSnapshot

class FavoritesData(BaseDataClass):
    pass;
#end class FavoritesData

class VideoCoverPicture(BaseDataClass):
    def __init__(self, avid:int, sourceUrl:str, data:bytes):
        extensionName = sourceUrl.split(".")[-1];
        args = locals().copy();
        del args["self"];
        args["extensionName"] = extensionName;
        super().__init__(args);
#end class VideoCoverPicture

class Danmaku:
    import xml.etree.ElementTree as xmlet;
    def __init__(self, cid:int, xmlString:str):
        self.xmlString  = xmlString;
        self.xml  = self.xmlet.fromstring(xmlString);
        self.cid = cid;
    def GetString(self) -> str:
        return self.xmlString;
    def GetForamttedString(self, indent="    ") -> str:
        import copy;
        xml = copy.deepcopy(self.xml);
        self.xmlet.indent(xml, indent);
        return self.xmlet.tostring(xml, encoding="utf-8").decode("utf-8");
    def GetXml(self) -> xmlet.Element:
        return self.xml;
#end class Danmaku
