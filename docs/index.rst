Homepage
========

|GitHub| |CHANGELOG| |PyPI| |Issues| |License|

.. |GitHub| image:: https://img.shields.io/badge/github-bgetlib-blue
   :target: https://github.com/baobao1270/bgetlib

.. |CHANGELOG| image:: https://img.shields.io/badge/Changelog-ee0000
   :target: https://github.com/baobao1270/bgetlib/blob/master/CHANGELOG

.. |PyPI| image:: https://img.shields.io/badge/pypi-bgetlib-blue
   :target: https://pypi.org/project/bgetlib

.. |Issues| image:: https://img.shields.io/github/issues/baobao1270/bgetlib
   :target: https://github.com/baobao1270/bgetlib/issues

.. |License| image:: https://img.shields.io/github/license/baobao1270/bgetlib
   :target: https://github.com/baobao1270/bgetlib/blob/master/LICENSE

**bgetlib** is a bilibili API library.

Install
-------
.. code:: shell

   pip install bgetlib


Quickstart
----------
.. code:: python

    import bgetlib

    bapi = bgetlib.BilibiliAPI("bilibili.com_cookies.txt")
    # https://space.bilibili.com/36081646/favlist?fid=976082846
    videos = bapi.get_favorites_all(976082846)

    for video in videos:
        video_detail = bapi.get_video(video["id"])
        for part in video_detail["pages"]:
            bapi.video_stream_to_file(video_detail["aid"], part["cid"],
                                      "av{}-P{}.mp4".format(video_detail["aid"], part["page"]))


Manual
------
.. toctree::
   :maxdepth: 2

   api
   codec
   models
   utils
