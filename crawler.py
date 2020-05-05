from common import MAX_ITERATION_CNT, LinkQueue, Scraper

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

