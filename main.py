import ray

import time
from crawler_distributed import run_distributed_crawler
from crawler import run_non_distributed_crawler

# pip install requests==2.22.0 beautifulsoup4==4.8.1 ray==0.8.4

if __name__ == "__main__":
    address = ray.init(address="auto", webui_host="0.0.0.0")
    print(address["webui_url"])
    assert ray.is_initialized()

    # warmup
    @ray.remote
    def f():
        return 3

    ray.get([f.remote() for _ in range(1000)])

    non_distributed_start = time.perf_counter()
    total_visited_non_distributed = run_non_distributed_crawler()
    non_distributed_end = time.perf_counter()

    distributed_start = time.perf_counter()
    total_visited_distributed = run_distributed_crawler()
    distributed_end = time.perf_counter()

    # Make sure they return the same result.
    print(
        f"non distributed crawler takes {non_distributed_end - non_distributed_start}"
    )
    print(f"non distributed crawler crawled {total_visited_non_distributed} entries")
    print(f"distributed crawler takes {distributed_end - distributed_start}")
    print(f"distributed crawler crawled {total_visited_distributed} entries")

    time.sleep(100)
