from ast import walk
from urllib.parse import urlparse
from core import ExplorationStrategy, WalkerContext
import random
from typing import List, Union

class UniformExplorationStrategy(ExplorationStrategy):

    def __init__(self, walker_context: WalkerContext) -> None:
        self.walker_context = walker_context

    @property
    def _sites_visited(self):
        return self.walker_context._sites_visited

    def _filter_urls(self, urls: List[str]) -> List[str]:
        return urls

    def sample_next_url(self, urls: Union[List[str], None]) -> str:
        if urls is None:
            choice = random.choice(list(self._sites_visited))
        else:
            possible_urls = self._filter_urls(list(set(urls).difference(self._sites_visited)))
            if len(possible_urls) > 0:
                choice = random.choice(possible_urls)
            else:
                choice = random.choice(list(self._sites_visited))
        return choice


class HostnameWhitelistExplorationStrategy(UniformExplorationStrategy):

    def __init__(self, walker_context: WalkerContext, allowed_hostnames: List[str]) -> None:
        super().__init__(walker_context)
        self._allowed_hostnames = allowed_hostnames

    def _allowed(self, url: str):
        p = urlparse(url)
        if p.hostname is None:
            return False
        return p.hostname in self._allowed_hostnames

    def _filter_urls(self, urls: List[str]) -> List[str]:
        return list(filter(self._allowed, urls))