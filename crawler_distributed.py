import os
import time

import ray
from common import LinkQueue, Scraper, MAX_PAGES_CRAWL


@ray.remote(num_cpus=1)
def crawl(initial_url, link_queue):
    scraper = Scraper()

    iteration_cnt = 0
    visited = len(ray.get(link_queue.get_visited.remote()))

    while visited < MAX_PAGES_CRAWL:
        url = ray.get(link_queue.pop.remote())
        # This will print word count of ray from the page.
        new_links = scraper.parse(url)
        for new_link in new_links:
            link_queue.add.remote(new_link)

        iteration_cnt += 1
        visited = len(ray.get(link_queue.get_visited.remote()))


def run_distributed_crawler():
    urls = [
        "http://toscrape.com/",
    ]

    link_queue = ray.remote(LinkQueue).remote()
    for url in urls:
        link_queue.add.remote(url)
    ray.get([crawl.remote(None, link_queue) for _ in range(16)])
    visited = ray.get(link_queue.get_visited.remote(), timeout=5)
    return len(visited)
