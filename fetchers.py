from core import Fetcher, FetchError, Site
import requests

class RequestsFetcher(Fetcher):

    def fetch(self, url: str) -> Site:
        r = requests.get(url)
        if "text/html" not in r.headers["Content-Type"]:
            raise FetchError()
        content = r.content
        if "charset" in r.headers["Content-Type"]:
            for field in r.headers["Content-Type"].split(";"):
                if "charset" in field:
                    coding = field.split("=")[-1]
                    break
            try:
                content = content.decode(coding)
            except UnicodeDecodeError:
                raise FetchError()
        return Site(content, url)