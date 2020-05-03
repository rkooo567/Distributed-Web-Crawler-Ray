import ray

import requests
import time
from bs4 import BeautifulSoup
from typing import List
from crawler_distributed import run_distributed_crawler, MAX_ITERATION_CNT, Scraper

# pip install requests==2.22.0 beautifulsoup4==4.8.1 ray==0.8.4
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

    def _is_visited(self, link):
        return link in self.visited


def crawl(initial_url, link_queue: LinkQueue):
    scraper = Scraper()
    link_queue.add(initial_url)

    iteration_cnt = 0
    while link_queue.size() != 0 and iteration_cnt < MAX_ITERATION_CNT and link_queue.size() < 300:
        url = link_queue.pop()
        # This will print word count of ray from the page.
        new_links = scraper.parse(url)
        for new_link in new_links:
            link_queue.add(new_link)
        
        iteration_cnt += 1


def run_non_distributed_crawler():
    first_url = "http://quotes.toscrape.com/"
    link_queue = LinkQueue()
    link_queue.add(first_url)
    crawl(first_url, link_queue)

    second_url = "http://toscrape.com/"
    crawl(second_url, link_queue)

    third_url = "https://www.qq.com/"
    crawl(third_url, link_queue)
    return len(link_queue.visited)


if __name__ == '__main__':
    ray.init()
    assert ray.is_initialized()

    start = time.time()
    visited_not_distributed = run_non_distributed_crawler()
    end = time.time()
    print(f"non distributed crawler takes {end - start}")
    
    start = time.time()
    visited_distributed = run_distributed_crawler()
    end = time.time()
    print(f"distributed crawler takes {end - start}")

    # Make sure they return the same result.
    print(f"non distributed crawler crawled {visited_not_distributed} entries")
    print(f"distributed crawler crawled {visited_distributed} entries")


# What should we do with this?
# What features do we need to support?
#  - crawling
#  - interface to scrape
