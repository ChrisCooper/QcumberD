from solus_scraper import SolusScraper
from alphanum_scraper import AlphanumScraper

class CatalogScraper(SolusScraper):
    """Scrapes data for the entire SOLUS site."""

    def scrape_all(self):
        """
        Starts a full scrape of the SOLUS site, following this scraper's configuration.
        """

        print ("Scrape job config:")
        print(self.config_string())
        
        print("Beginning scrape job...")

        for letter in self.config.letters:

            print ("-- Scraping letter: " + letter)
            AlphanumScraper(self).scrape_alphanum(letter)