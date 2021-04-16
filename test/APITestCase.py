import hashlib
import xml.etree.ElementTree
from unittest import TestCase

from _common import *


class APITestCase(TestCase):
    def test_get_fav_folders(self) -> None:
        fav_folders = get_api().list_favourite_folders(UID_LUOTIANYI).keys()
        self.assertIn(FAV_ID_LUOTIANYI, fav_folders)

    def test_get_fav_folders_login(self) -> None:
        fav_folders = get_api(login=True).list_favourite_folders(UID_DEVELOPER).keys()
        self.assertIn(FAV_ID_DEVELOPER, fav_folders)

    def test_get_fav_recent(self) -> None:
        fav_list = get_api().get_favorites(FAV_ID_LUOTIANYI)
        self.assertEqual(fav_list[0].avid, FAV_LUOTIANYI_FIRST_AVID)

    def test_get_fav_recent_login(self) -> None:
        fav_list = get_api(login=True).get_favorites(FAV_ID_DEVELOPER)
        self.assertEqual(fav_list[0].avid, FAV_DEVELOPER_FIRST_AVID)

    def test_get_fav_all(self) -> None:
        fav_list = get_api().get_favorites_all(FAV_ID_LUOTIANYI)
        self.assertEqual(len(fav_list), FAV_LUOTIANYI_COUNT)
        fav_list = get_api(login=True).get_favorites_all(FAV_ID_DEVELOPER)
        self.assertEqual(len(fav_list), FAV_DEVELOPER_COUNT)

    def test_get_fav_nbf(self) -> None:
        fav_list = get_api().get_favorites_nbf(FAV_ID_LUOTIANYI, FAV_NBF_2020_LTY_BIRTHDAY)
        self.assertEqual(len(fav_list), FAV_NBF_COUNT)

    def test_get_video_normal(self) -> None:
        v = get_api().get_video(V_ID_NORMAL)
        self.assertEqual(v.avid, V_ID_NORMAL)

    # noinspection DuplicatedCode
    def test_get_video_multi_part(self) -> None:
        v = get_api().get_video(V_ID_MULTIPART)
        self.assertEqual(v.avid, V_ID_MULTIPART)
        output("title={}".format(v.title), end="...")
        self.assertEqual(len(v.parts), len(V_ASSERT_MULTIPART_CIDS))
        ids = [p.cid for p in v.parts]
        for i in V_ASSERT_MULTIPART_CIDS:
            self.assertIn(i, ids)

    # noinspection DuplicatedCode
    def test_get_video_multi_staff(self) -> None:
        v = get_api().get_video(V_ID_MULTISTAFF)
        self.assertEqual(v.avid, V_ID_MULTISTAFF)
        output("title={}".format(v.title), end="...")
        self.assertEqual(len(v.staff), len(V_ASSERT_MULTISTAFF_UIDS))
        ids = [s.uid for s in v.staff]
        for i in V_ASSERT_MULTISTAFF_UIDS:
            self.assertIn(i, ids)

    def test_get_video_cover(self) -> None:
        pic = get_api().get_video(V_ID_NORMAL).cover.download()
        hash_str = hashlib.sha1(pic).hexdigest()
        output("hash={}".format(hash_str), end="...")
        self.assertEqual(hash_str, V_ASSERT_COVER_HASH)

    def test_get_video_danmaku(self) -> None:
        cid = get_api().get_video(V_ID_NORMAL).parts[0].cid
        danmaku_xml = get_api().get_live_danmaku(cid)
        self.assertIsNotNone(xml.etree.ElementTree.fromstring(danmaku_xml))

    # noinspection DuplicatedCode
    def test_get_category(self):
        v_count, v_list = get_api().get_category(CATE_ID_VOCALOID_UTAU)
        _, v_list_2 = get_api().get_category(CATE_ID_VOCALOID_UTAU, page=2)
        v_list = v_list + v_list_2
        output("count={}".format(v_count), end="...")
        for v in v_list:
            self.assertEqual(v.category, CATE_NAME_VOCALOID_UTAU)

    # noinspection DuplicatedCode
    def test_get_category_latest(self):
        v_count, v_list = get_api().get_category_latest(CATE_ID_VOCALOID_UTAU)
        _, v_list_2 = get_api().get_category(CATE_ID_VOCALOID_UTAU, page=2)
        v_list = v_list + v_list_2
        output("count={}".format(v_count), end="...")
        for v in v_list:
            self.assertEqual(v.category, CATE_NAME_VOCALOID_UTAU)

    # noinspection DuplicatedCode
    def test_get_tag(self):
        v_count, v_list = get_api().get_tag(CATE_ID_VOCALOID_UTAU, TAG_ID_LUOTIANYI)
        _, v_list_2 = get_api().get_tag(CATE_ID_VOCALOID_UTAU, TAG_ID_LUOTIANYI, page=2)
        v_list = v_list + v_list_2
        output("count={}".format(v_count), end="...")
        for v in v_list:
            self.assertEqual(v.category, CATE_NAME_VOCALOID_UTAU)

    # noinspection DuplicatedCode
    def test_get_tag_latest(self):
        v_count, v_list = get_api().get_tag_latest(CATE_ID_VOCALOID_UTAU, TAG_ID_LUOTIANYI)
        _, v_list_2 = get_api().get_tag_latest(CATE_ID_VOCALOID_UTAU, TAG_ID_LUOTIANYI, page=2)
        v_list = v_list + v_list_2
        output("count={}".format(v_count), end="...")
        for v in v_list:
            self.assertEqual(v.category, CATE_NAME_VOCALOID_UTAU)

    def test_get_category_hot(self):
        v_list = get_api().get_category_hot(CATE_ID_VOCALOID_UTAU)
        self.assertNotEqual(len(v_list), 0)
        v_list = get_api().get_category_hot(CATE_ID_VOCALOID_UTAU, 3)
        self.assertNotEqual(len(v_list), 0)

    def test_get_tag_hot(self):
        v_list = get_api().get_tag_hot(CATE_ID_VOCALOID_UTAU, TAG_ID_LUOTIANYI)
        self.assertNotEqual(len(v_list), 0)

    def test_list_emote_packages(self):
        packages = get_api(login=True).list_emote_packages()
        self.assertIn(EMOTE_PKG_ID_LTYNSS, packages.keys())

    def test_download_emotes(self):
        emotes = get_api().get_emotes(EMOTE_PKG_ID_LTYNSS)
        hash_list = [hashlib.sha1(v.download()).hexdigest() for k, v in emotes.items()]
        self.assertEqual(len(EMOTE_PAG_LTYNSS_HASHLIST), len(hash_list))
        for i in EMOTE_PAG_LTYNSS_HASHLIST:
            self.assertIn(i, hash_list)
