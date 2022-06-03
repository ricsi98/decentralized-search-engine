from exploration import HostnameWhitelistExplorationStrategy, UniformExplorationStrategy
from fetchers import RequestsFetcher
from utils import *
from core import *


if __name__ == '__main__':
    context = WalkerContext()
    class PrintProcessor(Processor):

        def process(self, site: Site) -> None:
            print(site.url)

    class ParagraphPrinter(Processor):

        def process(self, site: Site) -> None:
            print(len(site.paragraphs))

    start_url = "https://index.hu"#"https://en.wikipedia.org/wiki/Okapi_BM25"
    strategy = HostnameWhitelistExplorationStrategy(context, [urlparse(start_url).hostname])
    walker = WebWalker(RequestsFetcher(), start_url, context, strategy)
    walker.register_processor(PrintProcessor())
    walker.register_processor(ParagraphPrinter())
    try:
        for _ in range(20):
            walker.step()
    finally:
        with open("output.txt", "w") as f:
            f.write("\n".join(list(context._sites_visited)))