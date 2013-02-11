class SolusParser(object):
    """Superclass for parsing data from Solus BeatifulSoup"""

    def __init__(self, soup):
        self.soup = soup

    def clean_HTML(self, string):
        return string.replace('&nbsp;',' ').strip()