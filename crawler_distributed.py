import ray
import requests
from bs4 import BeautifulSoup
from typing import List

MAX_ITERATION_CNT = 10

class Scraper:
    def __init__(self):
        pass

    def parse(self, url) -> List[str]:
        """
        - parse HTML
        - print word count of ray
        - return links from the page.
        """
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        new_links = []
        for link_tag in soup.find_all('a'):
            new_link = self._get_url(link_tag.get('href'), url)
            if new_link is not None:
                new_links.append(new_link)
        return new_links

    def _get_url(self, path, root_url) -> str:
        """
        [http|https]://something.com -> Just return
        /tag/user -> return https://[root_url]/tag/user
        """
        if path is None:
            return None

        if path.startswith("http"):
            return path
        elif path.startswith("/"):
            if root_url[-1] == "/":
                root_url = root_url[:-1]
            return f"{root_url}{path}"
        else:
            return None


@ray.remote
class LinkQueue:
    def __init__(self):
        self.queue = []
        self.visited = set()

    def add(self, link):
        if not self._is_visited(link):
            self.queue.append(link)
            self.visited.add(link)

    def pop(self):
        """
        Pop the first link in the queue.
        """
        return self.queue.pop(0)
    
    def size(self):
        return len(self.queue)

    def get_visited(self):
        return self.visited

    def _is_visited(self, link):
        return link in self.visited


@ray.remote
def crawl(initial_url, link_queue):
    scraper = Scraper()

    iteration_cnt = 0
    link_queue_size = ray.get(link_queue.size.remote())
    while link_queue_size != 0 and iteration_cnt < MAX_ITERATION_CNT and link_queue_size < 300:
        url = ray.get(link_queue.pop.remote())
        # This will print word count of ray from the page.
        new_links = scraper.parse(url)
        for new_link in new_links:
            link_queue.add.remote(new_link)
        
        iteration_cnt += 1
        link_queue_size = ray.get(link_queue.size.remote())


def run_distributed_crawler():
    first_url = "http://quotes.toscrape.com/"
    second_url = "http://toscrape.com/"
    third_url = "https://www.qq.com/"

    link_queue = LinkQueue.remote()
    link_queue.add.remote(first_url)
    link_queue.add.remote(second_url)
    link_queue.add.remote(third_url)
    ray.get([
        crawl.remote(first_url, link_queue),
        crawl.remote(second_url, link_queue),
        crawl.remote(third_url, link_queue)
    ])
    visited = ray.get(link_queue.get_visited.remote())
    return len(visited)
