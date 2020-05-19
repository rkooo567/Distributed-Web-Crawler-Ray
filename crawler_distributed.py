import os

import ray
from common import LinkQueue, Scraper, MAX_ITERATION_CNT, MAX_PAGES_CRAWL


@ray.remote
def crawl(initial_url, link_queue):
    scraper = Scraper()

    links_ctn = 0
    iteration_cnt = 0
    link_queue_size = ray.get(link_queue.size.remote())
    while (
        link_queue_size != 0
        and iteration_cnt < MAX_ITERATION_CNT
        and link_queue_size < MAX_PAGES_CRAWL
    ):
        url = ray.get(link_queue.pop.remote(), timeout=5)
        # This will print word count of ray from the page.
        new_links = scraper.parse(url)
        links_ctn += len(new_links)
        for new_link in new_links:
            link_queue.add.remote(new_link)

        iteration_cnt += 1
        link_queue_size = ray.get(link_queue.size.remote(), timeout=5)

    print(f"{str(os.getpid())}: URL: {initial_url}, Links #: {links_ctn}")


def run_distributed_crawler():
    urls = [
        "http://quotes.toscrape.com/",
        "http://toscrape.com/",
        "https://naver.com/",
        "https://www.daum.net/",
        "https://namu.wiki/w/%EB%82%98%EB%AC%B4%EC%9C%84%ED%82%A4:%EB%8C%80%EB%AC%B8",
        "https://www.coupang.com/",
        "https://www.11st.co.kr/html/main.html",
        "fc2.com",
        "livejasmin.com",
        "popads.net",
        "soundcloud.com",
    ]

    link_queue = ray.remote(LinkQueue).remote()
    for url in urls:
        link_queue.add.remote(url)

    ray.get([crawl.remote(url, link_queue) for url in urls])
    visited = ray.get(link_queue.get_visited.remote(), timeout=5)
    history = ray.get(link_queue.get_throttler_info.remote())
    print(f"History: {len(history)}")
    print(history)
    return len(visited)
