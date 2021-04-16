class CanLogin:
    def __init__(self):
        self.cookies = None

    def login(self, cookie_filename: str, ignore_discard: bool = True, ignore_expires: bool = True) -> None:
        import http.cookiejar as cookiejar
        self.cookies = cookiejar.MozillaCookieJar()
        self.cookies.load(cookie_filename, ignore_discard=ignore_discard, ignore_expires=ignore_expires)
