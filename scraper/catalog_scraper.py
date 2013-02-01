from solus_scraper import SolusScraper

class CatalogScraper(SolusScraper):
    """Scrapes data for the entire SOLUS site."""

    def scrape_all(self):
        """
        Starts a full scrape of the SOLUS site, following this scraper's configuration.
        """

        print ("Scrape job config:")
        print(self.config_string())
        
        print("Beginning scrape job...")
        
        return

        for letter in self.config.letters:

            print ("--Parsing letter: " + letter)
            s.select_alphanum(letter)

            # Scrapes all the subjects
            self.scrape_alphanum(s)

        self.solus.close_session()