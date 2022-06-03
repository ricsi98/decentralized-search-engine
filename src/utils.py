from urllib.parse import urlparse
from bs4 import Comment
import validators

def same_hostname(url1: str, url2: str) -> bool:
    p1, p2 = urlparse(url1), urlparse(url2)
    return p1 is not None and p2 is not None and p1.hostname == p2.hostname

def complete_relative(page_url: str, link: str) -> str:
    if link.startswith("/"):
        p = urlparse(page_url)
        return p.scheme + "://" + p.hostname + link
    return link


def link_from_href(page_url: str, link: str) -> str:
    link = complete_relative(page_url, link)
    if link.startswith("mail") or link.startswith("#"): 
        return None
    if validators.url(link):
        return link


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True