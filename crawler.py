from common import LinkQueue, Scraper, MAX_PAGES_CRAWL


def crawl(initial_url, link_queue: LinkQueue):
    scraper = Scraper()
    link_queue.add(initial_url)

    while (
        len(link_queue.get_visited()) < MAX_PAGES_CRAWL
        and link_queue.size() != 0
        and iteration_cnt < MAX_PAGES_CRAWL * 2
    ):
        url = link_queue.pop()
        new_links = scraper.parse(url)
        for new_link in new_links:
            link_queue.add(new_link)


def run_non_distributed_crawler():
    urls = [
        "http://toscrape.com/",
    ]
    link_queue = LinkQueue()
    for url in urls:
        crawl(url, link_queue)
    return len(link_queue.visited)
