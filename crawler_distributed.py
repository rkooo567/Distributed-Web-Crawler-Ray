import time

import ray

from common import LinkQueue, Scraper, MAX_PAGES_CRAWL


@ray.remote(num_cpus=1)
def crawl(initial_url, link_queue):

    scraper = Scraper()

    visited = len(ray.get(link_queue.get_visited.remote()))

    while visited < MAX_PAGES_CRAWL:
        urls = ray.get(link_queue.pop_batch.remote())
        if len(urls) == 0:
            time.sleep(0.1)

        for url in urls:
            new_links = scraper.parse(url)
            link_queue.add_batch.remote(new_links)

        visited = len(ray.get(link_queue.get_visited.remote()))


def run_distributed_crawler():
    urls = [
        "http://toscrape.com/",
    ]

    link_queue = ray.remote(LinkQueue).remote()
    link_queue.add_batch.remote(urls)
    ray.get([crawl.remote(None, link_queue) for _ in range(16)])
    visited = ray.get(link_queue.get_visited.remote(), timeout=5)
    return len(visited)
