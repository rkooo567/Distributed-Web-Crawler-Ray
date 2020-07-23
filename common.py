import requests
from collections import defaultdict
from bs4 import BeautifulSoup
from typing import List
from urllib.parse import urlparse

MAX_REVISIT = 30000
MAX_PAGES_CRAWL = 5000
BATCH_SIZE = 10


class Throttler:
    def __init__(self, max_visit=MAX_REVISIT):
        self.history = defaultdict(int)
        self.max_visit = max_visit
        # Do not scrape these websites
        self.banned_hosts = ["scrapinghub", "goodreads", "wikimedia"]

    def record(self, url):
        site = self._get_hostname(url)
        self.history[site] += 1

    def is_banned(self, url):
        for host in self.banned_hosts:
            if host in url:
                return True

        if "44.233.155.0" not in url:
            return True

        return False

    def is_throttled(self, url):
        site = self._get_hostname(url)
        return self.history[site] >= self.max_visit

    def _get_hostname(self, url):
        return urlparse(url).hostname


class Scraper:
    def __init__(self):
        self.exception_ctn = 0

    def parse(self, url) -> List[str]:
        if not url:
            return []

        try:
            html_text = requests.get(url, timeout=0.7).text
            soup = BeautifulSoup(html_text, "html.parser")
            new_links = []
            for link_tag in soup.find_all("a"):
                new_link = self._get_url(link_tag.get("href"), url)
                if new_link is not None:
                    new_links.append(new_link)
        except Exception as e:
            print(e)
            self.exception_ctn += 1
            return []

        return new_links

    def _get_url(self, path, root_url) -> str:
        if path is None:
            return None
        url_info = urlparse(path)
        host = url_info.netloc
        path = url_info.path
        scheme = url_info.scheme
        # We don't care protocols other than http/https
        if scheme != "http" and scheme != "https":
            scheme = "http"

        if host == "":
            return f"{root_url}/{path}"
        return f"{scheme}://{host}{path}"


class LinkQueue:
    def __init__(self):
        self.queue = []
        self.visited = set()
        self.throttler = Throttler()

    def add_batch(self, links):
        for link in links:
            if self.throttler.is_throttled(link) or self.throttler.is_banned(link):
                return

            if not link in self.visited:
                self.queue.append(link)
                self.visited.add(link)
                self.throttler.record(link)

    def pop_batch(self):
        """
        Pop the first link in the queue.
        """
        if self.size() == 0:
            return []

        if self.size() < BATCH_SIZE:
            links = self.queue[:]
            self.queue = []
            return links
        else:
            links = [self.queue.pop(0) for _ in range(BATCH_SIZE)]
            return links

    def size(self):
        return len(self.queue)

    def get_visited(self):
        return self.visited

    def get_throttler_info(self):
        return self.throttler.history
