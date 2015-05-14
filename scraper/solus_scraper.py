from scraper.solus_session import SolusSession

class SolusScraper(object):
    """Superclass for scraping data from a SolusSession"""

    def __init__(self, scraper=None, config=None):

        if config:
            # Initialize from scratch
            self.config = config
            self.solus = SolusSession()
        elif scraper:
            # Initialize from a previous scraper
            self.config = scraper.config
            self.solus = scraper.solus

    def config_string(self):
        """Returns a string to display the current configuration"""

        config_string = ''
        for field in self.config._meta.fields:
            config_string = config_string + '\n--{0}: {1}'.format(str(field.name), str(field.value_from_object(self.config)))
        
        return config_string

