import datetime
import sys
import os
import time

import bgetlib

REQUEST_TIME_WAIT_SEC     = 1
LOGIN_COOKIE_PATH         = os.path.join(os.path.dirname(__file__), "bilibili.com_cookies.txt")
DOWNLOAD_TEMP_DIR         = os.path.join(os.path.dirname(__file__), "temp")
UID_DEVELOPER             = 2266062
UID_LUOTIANYI             = 36081646
FAV_ID_DEVELOPER          = 62058462
FAV_DEVELOPER_COUNT       = 165
FAV_DEVELOPER_FIRST_AVID  = 470455
FAV_ID_LUOTIANYI          = 976082846
FAV_LUOTIANYI_COUNT       = 100
FAV_LUOTIANYI_FIRST_AVID  = 927444053
FAV_NBF_2020_LTY_BIRTHDAY = int(time.mktime(datetime.datetime.strptime("20200712", "%Y%m%d").timetuple()))
FAV_NBF_COUNT             = 43
V_ID_NORMAL               = 60660066
V_ID_MULTIPART            = 12660426
V_ID_MULTISTAFF           = 456845628
V_ASSERT_MULTIPART_CIDS   = [20825525, 20847187, 20825521, 20825523, 20847188, 20825527, 20847185, 20825529]
V_ASSERT_MULTISTAFF_UIDS  = [5009841, 11218480, 529083, 281804983]
V_ASSERT_COVER_HASH       = "88cce64afd7d6cc69855194da2c34aaa4a66eb23"
CATE_ID_VOCALOID_UTAU     = 30
CATE_NAME_VOCALOID_UTAU   = "VOCALOID·UTAU"
TAG_ID_LUOTIANYI          = 8564
EMOTE_PKG_ID_LTYNSS       = 166
EMOTE_PAG_LTYNSS_HASHLIST = [
    "bbeb9d231773a168397697072a11373893d7c01a",
    "55bdcf04316ed0d805a15131b57b35b6cbd0d887",
    "659efad4a6aa25ed6a98efe611564c26f497f436",
    "730e0d30a6556f433fa317f8468ce7229e4c7872",
    "35ab588061c32f07743b07f1ac3f62a16f34438c",
    "152d7bd6d4096ebb89974d591b9c305b29a89166",
    "3159931d9afa243c6cf5939753e3c82acb69a554",
    "6b4f86c6a21265addc8bc3fb511e5569af454237",
    "4a7550236996e1cb329974c58b751ac462007338",
    "d1202872850a335b357e702adaf3d2a79db72e13",
    "2513203daab74688cea2c9a595e051f53fbcaa94",
    "55c633884ca8405aade71d05fbaa687ab6fedd4a",
    "5455abac01a22978b20ec0b365c214a872a0fd14",
    "ec1dd6e3c004a40ac809347a02728624339cd435",
    "80d5195ee966465f5f338db26f2faba51afcd217"
]
DOWNLOAD_DASH_ASSERT_HASH = "7f38e6fb5fa1d3f9d523dc1d0c9f03dcb436719d"
CONVERT_AIFF_ASSERT_HASH  = "19835c4a417a3ac9d264b3c3477b91e3b0c551a1"
CONVERT_FLAC_ASSERT_HASH  = "078e3e7bfcf7555a342b736753115cab064912dd"
CONVERT_FLV_ASSERT_HASH   = "428480c544db8c7243b167b13e762f4e35409c83"
CONVERT_MP3_ASSERT_HASH   = "6cb3939c9c10fa6ec47897161cfc7b2d066e6559"


def create_temp_dir():
    if not os.path.exists(DOWNLOAD_TEMP_DIR):
        os.makedirs(DOWNLOAD_TEMP_DIR)


def get_api(login: bool = False):
    api = bgetlib.BilibiliAPI()
    if login:
        api.login(LOGIN_COOKIE_PATH)
    time.sleep(REQUEST_TIME_WAIT_SEC)
    return api


def get_dl():
    dl = bgetlib.Downloader()
    dl.login(LOGIN_COOKIE_PATH)
    return dl


def output(*values, **kwargs):
    print(*values, **kwargs, file=sys.stderr)
