from concurrent.futures import thread


BV2AV_TABLE = "fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF"
BV2AV_TABLE_DICT = {'f': 0, 'Z': 1, 'o': 2, 'd': 3, 'R': 4, '9': 5, 'X': 6, 'Q': 7, 'D': 8, 'S': 9, 'U': 10, 'm': 11,
                    '2': 12, '1': 13, 'y': 14, 'C': 15, 'k': 16, 'r': 17, '6': 18, 'z': 19, 'B': 20, 'q': 21, 'i': 22,
                    'v': 23, 'e': 24, 'Y': 25, 'a': 26, 'h': 27, '8': 28, 'b': 29, 't': 30, '4': 31, 'x': 32, 's': 33,
                    'W': 34, 'p': 35, 'H': 36, 'n': 37, 'J': 38, 'E': 39, '7': 40, 'j': 41, 'L': 42, '5': 43, 'V': 44,
                    'G': 45, '3': 46, 'g': 47, 'u': 48, 'M': 49, 'T': 50, 'K': 51, 'N': 52, 'P': 53, 'A': 54, 'w': 55,
                    'c': 56, 'F': 57}
BV2AV_S = [11, 10, 3, 8, 4, 6]
BV2AV_XOR = 177451812
BV2AV_ADD = 8728348608


def bv2av(bvid: str) -> int:
    """Convert bvid to aid"""

    r = 0
    for i in range(6):
        r += BV2AV_TABLE_DICT[bvid[BV2AV_S[i]]] * 58 ** i
    return (r - BV2AV_ADD) ^ BV2AV_XOR


def av2bv(aid: int) -> str:
    """Convert aid to bvid"""

    aid = (aid ^ BV2AV_XOR) + BV2AV_ADD
    r = list("BV1  4 1 7  ")
    for i in range(6):
        r[BV2AV_S[i]] = BV2AV_TABLE[aid // 58 ** i % 58]
    return ''.join(r)


def find_ffmpeg() -> str:
    import shutil
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise RuntimeError("""
        ---------- BGETLIB ERROR ----------
        This program requires ffmpeg to be installed.
        If you have installed ffmpeg, please make sure
        it is in your PATH and named 'ffmpeg'.
        
        If you are user, please install ffmpeg at its
        official website:
            https://www.ffmpeg.org/
        Or you can install it with package manager.

        If you are developer, please add instructions of
        installing ffmpeg in your user guide, or consider
        include ffmpeg in your binary distribuction (if
        your software follows ffmpeg's license).
        --------- END ERROR REPORT --------
        """)
    return "ffmpeg"


NTFS_ESCAPE_TABLE = {"/": "╱", "\\": "＼", "\"": "＂", ":": "：", "*": "🞰",
                     "<": "＜", ">": "＞", "|": "｜", "?": "？"}


def ntfs_escape(filename: str) -> str:
    """Convert any string to a NTFS filename

    On NTFS Filesystem under Windows, some special characters are forbidden in filenames.
    This function replace them with unicode characters with same glyph.
    """

    for search, replace in NTFS_ESCAPE_TABLE.items():
        filename = filename.replace(search, replace)
    return filename


def replace_host(url: str, host: str) -> str:
    import urllib.parse
    return urllib.parse.urlunparse(urllib.parse.urlparse(url)._replace(netloc=host))
