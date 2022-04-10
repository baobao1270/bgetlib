# bgetlib
<a href="https://bgetlib.docs.josephcz.xyz/">
    <img alt="Documentation" src="https://img.shields.io/badge/Documentation-66ccff">
</a>
<a href="https://github.com/baobao1270/bgetlib/blob/master/CHANGELOG">
    <img alt="Changelog" src="https://img.shields.io/badge/Changelog-ee0000">
</a>
<a href="https://pypi.org/project/bgetlib/#history">
    <img alt="Version" src="https://img.shields.io/pypi/v/bgetlib"></a>
<a href="https://github.com/baobao1270/bgetlib/issues">
    <img alt="Issues" src="https://img.shields.io/github/issues/baobao1270/bgetlib"></a>
<a href="https://github.com/baobao1270/bgetlib/blob/master/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/baobao1270/bgetlib">
</a>

**bgetlib** is a bilibili API library.

## Install
```shell
pip install bgetlib
```

## Quickstart
```python
import bgetlib
from bgetlib.models import QualityOptions

bapi = bgetlib.BilibiliAPI("bilibili.com_cookies.txt")
# https://space.bilibili.com/36081646/favlist?fid=976082846
videos = bapi.get_favorites_all(976082846)
quality = QualityOptions()

for video in videos:
    video_detail = bapi.get_video(video["id"])
    for part in video_detail["pages"]:
        bapi.save_stream(video_detail["aid"], part["cid"], quality, f"av{video['id']}-P{part['page']}.mp4")
```
