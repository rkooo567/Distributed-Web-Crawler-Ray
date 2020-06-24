from common import LinkQueue, Scraper, MAX_PAGES_CRAWL

def crawl(initial_url, link_queue: LinkQueue):
    scraper = Scraper()
    link_queue.add(initial_url)

    iteration_cnt = 0
    while (len(link_queue.get_visited()) < MAX_PAGES_CRAWL and link_queue.size() != 0):
        # if iteration_cnt % 10 == 0:
        #     print(f"Iteration count: {iteration_cnt}")
        url = link_queue.pop()
        # This will print word count of ray from the page.
        new_links = scraper.parse(url)
        # from pprint import pprint
        # pprint(new_links)
        for new_link in new_links:
            link_queue.add(new_link)
        
        iteration_cnt += 1


def run_non_distributed_crawler():
    urls = [
        "http://toscrape.com/",
    ]
    link_queue = LinkQueue()
    for url in urls:
        crawl(url, link_queue)
    return len(link_queue.visited)

