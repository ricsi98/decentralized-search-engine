from core import Processor, Site
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords # nltk.download("stopwords"); nltk.download("punkts")


class ParagraphPrinter(Processor):

        def __init__(self, stemmer: str = "snowball") -> None:
            self.i = 0
            self.sites = []
            self._stopwords = set(stopwords.words("english"))
            self._stemmer = SnowballStemmer("english") if stemmer == "snowball" else PorterStemmer()

        def _preprocess(self, text: str) -> str:
            text = text.replace("\\", "")
            tokens = word_tokenize(text)
            stems = [self._stemmer.stem(w) for w in tokens if not w.lower() in self._stopwords]
            return " ".join(stems)
            

        def process(self, site: Site) -> None:
            text = self._preprocess(site.paragraphs)
            with open(f"./output/doc{self.i}.json", "w") as f:
                f.write("{\n")
                f.write(f"\t\"id\": \"{site.url}\",\n")
                f.write(f'\t"contents": "{text}"\n')
                f.write("}")
            self.i += 1