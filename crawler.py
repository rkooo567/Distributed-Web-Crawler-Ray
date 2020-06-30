from common import LinkQueue, Scraper, MAX_PAGES_CRAWL


def crawl(initial_url, link_queue: LinkQueue):
    scraper = Scraper()

    while len(link_queue.get_visited()) < MAX_PAGES_CRAWL:
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
        link_queue.add(url)
    crawl(None, link_queue)
    return len(link_queue.visited)
