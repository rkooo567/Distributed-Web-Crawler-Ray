import ray
from common import LinkQueue, Scraper, MAX_ITERATION_CNT, MAX_PAGES_CRAWL

@ray.remote
def crawl(initial_url, link_queue):
    scraper = Scraper()

    iteration_cnt = 0
    link_queue_size = ray.get(link_queue.size.remote())
    while (link_queue_size != 0
            and iteration_cnt < MAX_ITERATION_CNT
            and link_queue_size < MAX_PAGES_CRAWL):
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

    link_queue = ray.remote(LinkQueue).remote()
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
