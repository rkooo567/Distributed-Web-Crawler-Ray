from common import LinkQueue, Scraper, MAX_PAGES_CRAWL


def crawl(initial_url, link_queue: LinkQueue):
    scraper = Scraper()

    while len(link_queue.get_visited()) < MAX_PAGES_CRAWL and link_queue.size() != 0:
        urls = link_queue.pop_batch()
        for url in urls:
            new_links = scraper.parse(url)
            link_queue.add_batch(new_links)


def run_non_distributed_crawler():
    urls = [
        "http://toscrape.com/",
    ]
    link_queue = LinkQueue()
    link_queue.add_batch(urls)
    crawl(None, link_queue)
    return len(link_queue.visited)
