Homepage
========

|GitHub| |PyPI| |Documentation| |Version| |Issues| |Coverage| |License|

.. |GitHub| image:: https://img.shields.io/badge/github-baobao1270%2Fbgetlib-66ccff
   :target: https://github.com/baobao1270/bgetlib

.. |PyPI| image:: https://img.shields.io/badge/pypi-bgetlib-blue
   :target: https://pypi.org/project/bgetlib

.. |Documentation| image:: https://img.shields.io/badge/docs-read-success
   :target: https://bgetlib.josephcz.xyz/docs/

.. |Version| image:: https://img.shields.io/pypi/v/bgetlib
   :target: https://pypi.org/project/bgetlib/#history

.. |Issues| image:: https://img.shields.io/github/issues/baobao1270/bgetlib
   :target: https://github.com/baobao1270/bgetlib/issues

.. |Coverage| image:: https://img.shields.io/badge/coverage-97%25-success
   :target: https://bgetlib.josephcz.xyz/cover/

.. |License| image:: https://img.shields.io/github/license/baobao1270/bgetlib
   :target: https://github.com/baobao1270/bgetlib/blob/master/LICENSE

bgetlib is a bilibili API library.

**This is not an official library. Abuse of this library may cause your bilibili account banned.**

This repository is not `bget`.

`bget` is a command line bilibili video downloader tool developed by the same developer of this library,
and it uses bgetlib as its core. If you want an `out-of-the-box` tool or don't know how to code,
please see the `bget` project: https://github.com/baobao1270/bget

**Please note that version 2.x has all API names changed.**


Site Navigation
---------------
.. toctree::
   :maxdepth: 1

   self
   docs/index


Install
-------
.. code:: shell

   pip install bgetlib


Usage
-----
.. code:: python

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


API Reference
-------------
See: `API Reference <./docs>`_


Coverage Report
---------------
See: `Coverage <https://bgetlib.josephcz.xyz/cover/>`_


Change Log
----------
See: `CHANGELOG <https://github.com/baobao1270/bgetlib/CHANGELOG>`_


License
-------
This project is under the MIT License. See: `LICENSE <https://github.com/baobao1270/bgetlib/LICENSE>`_
