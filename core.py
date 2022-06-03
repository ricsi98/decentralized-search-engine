from typing import Union, List
from bs4 import BeautifulSoup
import random

from utils import link_from_href, tag_visible


class Site:
    
    def __init__(self, html: str, url: str):
        self.html = html
        self.url = url
        self._soup = None
        self._links = None

    @property
    def soup(self) -> BeautifulSoup:
        if self._soup is None:
            self._soup = BeautifulSoup(self.html, "html.parser")
        return self._soup

    @property
    def links(self):
        if self._links is None:
            links = []
            for atag in self.soup.find_all('a', href=True):
                href = atag["href"]
                link = link_from_href(self.url, href)
                if link is None: continue
                links.append(link)
            self._links = links
        return self._links

    @property
    def paragraphs(self):
        return " ".join(t.strip() for t in filter(tag_visible, self.soup.findAll(text=True)))


class FetchError(Exception):
    pass


class Fetcher:

    def fetch(self, url: str) -> Site:
        raise NotImplementedError


class Processor:

    def process(self, site: Site) -> None:
        raise NotImplementedError


class ExplorationStrategy:

    def sample_next_url(self, urls: Union[List[str], None]) -> str:
        raise NotImplementedError


class WalkerContext(Processor):

    def __init__(self):
        self._sites_visited = set()

    def process(self, site: Site) -> None:
        if site is None or site.url is None: 
            return
        self._sites_visited.add(site.url)


class WebWalker:

    def __init__(self, fetcher: Fetcher, start_url: str, walker_context: WalkerContext, strategy: ExplorationStrategy):
        self._fetcher = fetcher
        self._url = start_url
        self._processors = []
        self._walker_context = walker_context
        self._strategy = strategy
        self.register_processor(walker_context)

    def register_processor(self, proc: Processor):
        self._processors.append(proc)

    def step(self):
        try:
            site = self._fetcher.fetch(self._url)
            for proc in self._processors:
                proc.process(site)
            self._url = self._strategy.sample_next_url(site.links)
        except FetchError:
            print("Encountered fetch error, relocating...")
            self._url = self._strategy.sample_next_url(None)