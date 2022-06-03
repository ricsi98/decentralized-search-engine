import sys
sys.path.append("./src")

from exploration import HostnameWhitelistExplorationStrategy, UniformExplorationStrategy
from fetchers import RequestsFetcher
from utils import *
from core import *
from processors import *

if __name__ == '__main__':
    context = WalkerContext()
    class PrintProcessor(Processor):

        def process(self, site: Site) -> None:
            print(site.url)

    


    start_url = "https://en.wikipedia.org/wiki/Okapi_BM25"
    strategy = HostnameWhitelistExplorationStrategy(context, [urlparse(start_url).hostname])
    walker = WebWalker(RequestsFetcher(), start_url, context, strategy)
    walker.register_processor(PrintProcessor())
    pp = ParagraphPrinter()
    walker.register_processor(pp)
    try:
        for i in range(1000):
            print(i)
            walker.step()
    finally:
        with open("output.txt", "w") as f:
            f.write("\n".join(list(context._sites_visited)))


"""
python -m pyserini.index.lucene --collection JsonCollection --input output --index index --threads 1 --generator DefaultLuceneDocumentGenerator --storePositions --storeDocvectors --pretokenized
"""