# bgetlib

<a href="https://github.com/baobao1270/bgetlib">
    <img alt="GitHub" src="https://img.shields.io/badge/github-baobao1270%2Fbgetlib-66ccff">
</a>
<a href="https://pypi.org/project/bgetlib">
    <img alt="PyPI" src="https://img.shields.io/badge/pypi-bgetlib-blue">
</a> 
<a href="https://bgetlib.josephcz.xyz/docs/">
    <img alt="Documentation" src="https://img.shields.io/badge/docs-read-success">
</a>
<a href="https://pypi.org/project/bgetlib/#history">
    <img alt="Version" src="https://img.shields.io/pypi/v/bgetlib"></a>
<a href="https://github.com/baobao1270/bgetlib/issues">
    <img alt="Issues" src="https://img.shields.io/github/issues/baobao1270/bgetlib"></a>
<a href="https://bgetlib.josephcz.xyz/cover/">
    <img alt="Coverage" src="https://img.shields.io/badge/coverage-97%25-success">
</a>
<a href="https://github.com/baobao1270/bgetlib/blob/master/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/baobao1270/bgetlib">
</a>

bgetlib is a bilibili API library.

**This is not an official library. Abuse of this library may cause your bilibili account banned.**

This repository is not _bget_.

_bget_ is a command line bilibili video downloader tool developed by the same developer of this library, and it uses bgetlib as its core. If you want an _out-of-the-box_ tool or don't know how to code, please see the _bget_ project: https://github.com/baobao1270/bget

**Please note that version 2.x has all API names changed.**

## Install
```shell
pip install bgetlib
```

## Getting Started
Code below is a simple video downloader.

```python
import bgetlib

bapi = bgetlib.BilibiliAPI()
bapi.login("cookies.txt")
downloader = bgetlib.Downloader()
fav_videos = bapi.get_favorites_all(976082846) # The Luo Tianyi's 2021 new songs collection ID

for fav_video in fav_videos:
    video = bapi.get_video(fav_video.avid)
    for part in video.parts:
        fd = downloader.download(video.avid, part.cid, "tmp/")
        transcoder = bgetlib.Transcoder("tmp/", fd)
        transcoder.save_dash("downloads/av{}.mp4".format(video.avid))
```

## API Reference
See: [API Reference](https://bgetlib.josephcz.xyz/docs)

## Coverage Report
See: [Coverage](https://bgetlib.josephcz.xyz/cover/)

## Change Log
See: [CHANGELOG](https://github.com/baobao1270/bgetlib/CHANGELOG)

## License
This project is under the MIT License. See: [LICENSE](https://github.com/baobao1270/bgetlib/LICENSE)
