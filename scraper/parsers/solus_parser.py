class SolusParser(object):
    """Superclass for parsing data from Solus BeatifulSoup"""

    def __init__(self, soup):
        self.soup = soup