import ray

import time
from crawler_distributed import run_distributed_crawler
from crawler import run_non_distributed_crawler

# pip install requests==2.22.0 beautifulsoup4==4.8.1 ray==0.8.4

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