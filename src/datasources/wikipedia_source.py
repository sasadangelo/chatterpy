import wikipediaapi
from urllib.parse import urlparse, parse_qs
from datasources.data_source import Source

class WikipediaSource(Source):
    def __init__(self, source):
        self.source = source
        self.pages = []

    def extract_title_from_url(self):
        # Extract the page title from the Wikipedia URL
        parsed_url = urlparse(self.source)
        path = parsed_url.path
        if path.startswith('/wiki/'):
            return path[len('/wiki/'):]
        else:
            raise ValueError("The URL does not seem to be a valid Wikipedia URL.")

    def load_data(self):
        # Initialize the Wikipedia API
        user_agent = "DataWaeve CLI"
        wiki_wiki = wikipediaapi.Wikipedia(user_agent, "en")

        # Extract the page title from the URL
        try:
            title = self.extract_title_from_url()
            page = wiki_wiki.page(title)

            if not page.exists():
                print(f"Page not found: {self.source}")
                return []

            # Return the page content as a list of documents
            self.pages = [page.text]
            print(f"Loaded content from Wikipedia page: {self.source}")
        except Exception as e:
            print(f"An error occurred while loading Wikipedia data: {e}")

    def get_text(self):
        if self.pages:
            return self.pages[0]
        else:
            return ""
