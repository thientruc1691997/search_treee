import sys
import os
import time
import random
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
   
from tstree.tstree import TSTree
from btree.btree import Btree




# Helper to simulate time.time_ns() in Python 3.6 (HPC version)
def time_ns():
    return int(time.time() * 1e9)


def load_words(filepath):
    with open(filepath) as file:
        return [line.strip() for line in file if line.strip()]


def benchmark_insert(words, sizes, nr_runs=10, insert_sample_size=20):
    print("\nInsert Performance Benchmark")
    results = {}
    insert_sample = random.sample(words, k=insert_sample_size)

    for size in sizes:
        sample = random.sample(words, k=size)
        tstree = TSTree()
        for word in sample:
            tstree.insert(word)

        total_time = 0.0
        for _ in range(nr_runs):
            start_time = time_ns()
            for word in insert_sample:
                tstree.insert(word)
            end_time = time_ns()
            total_time += end_time - start_time

        avg_time = total_time / (nr_runs * 1_000_000.0)  # in milliseconds
        results[size] = avg_time
        print(f"{size:>8} words → Insert avg: {avg_time:.2f} ms")

    return results


def benchmark_search_fixed_sample(words, sizes, nr_runs=10, search_sample_size=20):
    print("\nSearch Performance (Fixed Sample)")
    results = {}
    search_sample = random.sample(words, k=search_sample_size)

    for size in sizes:
        sample = random.sample(words, k=size)
        tstree = TSTree()
        for word in sample:
            tstree.insert(word)

        total_time = 0.0
        for _ in range(nr_runs):
            start_time = time_ns()
            for word in search_sample:
                tstree.search(word)
            end_time = time_ns()
            total_time += end_time - start_time

        avg_time = total_time / (nr_runs * 1_000_000.0)
        results[size] = avg_time
        print(f"{size:>8} words → Search avg: {avg_time:.2f} ms")

    return results


def benchmark_search_random_sample(words, sizes, nr_runs=10, sample_size=20):
    print("\nSearch Performance (Random from Inserted)")
    results = {}

    for size in sizes:
        sample = random.sample(words, k=size)
        tstree = TSTree()
        for word in sample:
            tstree.insert(word)

        total_time = 0.0
        for _ in range(nr_runs):
            search_sample = random.sample(sample, k=sample_size)
            start_time = time_ns()
            for word in search_sample:
                tstree.search(word)
            end_time = time_ns()
            total_time += end_time - start_time

        avg_time = total_time / (nr_runs * 1_000_000.0)
        results[size] = avg_time
        print(f"{size:>8} words → Search avg (random): {avg_time:.2f} ms")

    return results


def compare_with_set(words):
    print("\n----------------------------------------------")
    print("\nComparing TSTree and Python set for 100-word ")

    random.shuffle(words)
    hold_out_sample = words[-100:]
    insert_sample = words[:-100]

    # Insert into set
    start = time_ns()
    word_set = set()
    for word in insert_sample:
        word_set.add(word)
    set_insert_time = (time_ns() - start) / 1_000_000.0

    # Insert into TSTree
    word_tstree = TSTree()
    start = time_ns()
    for word in insert_sample:
        word_tstree.insert(word)
    tstree_insert_time = (time_ns() - start) / 1_000_000.0

    # Search from hold_out in set
    start = time_ns()
    total = 0
    for word in hold_out_sample:
        if word in word_set:
            total += 1
    set_search_time = (time_ns() - start) / 1_000_000.0

    # Search from hold_out in TSTree
    start = time_ns()
    total = 0
    for word in hold_out_sample:
        if word_tstree.search(word):
            total += 1
    tstree_search_time = (time_ns() - start) / 1_000_000.0

    # Display results
    print(f"Insert time (set):     {set_insert_time:.4f} ms")
    print(f"Insert time (TSTree):  {tstree_insert_time:.4f} ms")
    print(f"Search time (set):     {set_search_time:.4f} ms")
    print(f"Search time (TSTree):  {tstree_search_time:.4f} ms")


def time_function(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return result, end - start


def compare_btree_tstree(insert_sample, hold_out_sample, prefix="ca"):
    print("\n----------------------------------------------")
    print("\nComparing TSTree and BTree")
    print(f"\nInserting {len(insert_sample)} words...")

    btree = Btree()
    tstree = TSTree()

    # Insert
    _, btree_insert_time = time_function(lambda: [btree.insert(w) for w in insert_sample])
    _, tstree_insert_time = time_function(lambda: [tstree.insert(w) for w in insert_sample])

    print(f"Btree insert time:   {btree_insert_time:.4f}s")
    print(f"TSTree insert time:  {tstree_insert_time:.4f}s")

    # Search (using hold-out set)
    _, btree_search_time = time_function(lambda: [btree.search(w) for w in hold_out_sample])
    _, tstree_search_time = time_function(lambda: [tstree.search(w) for w in hold_out_sample])

    print(f"Btree search time:   {btree_search_time:.4f}s")
    print(f"TSTree search time:  {tstree_search_time:.4f}s")


    # Prefix search on TSTree
    _, tstree_prefix_time = time_function(tstree.starts_with, prefix)
    print(f"TSTree prefix search (prefix='{prefix}'): {tstree_prefix_time:.4f}s")

    # Summary
    print("\nSummary:")
    print(f"{'Operation':<20}{'Btree':>12}{'TSTree':>12}")
    print(f"{'-'*44}")
    print(f"{'Insert':<20}{btree_insert_time:12.4f}{tstree_insert_time:12.4f}")
    print(f"{'Search':<20}{btree_search_time:12.4f}{tstree_search_time:12.4f}")
    print(f"{'Prefix Search':<20}{'N/A':>12}{tstree_prefix_time:12.4f}")


if __name__ == "__main__":
    DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'corncob_lowercase.txt')
    words = load_words(DATA_PATH)

    print(f"Total words loaded: {len(words)}")
    print("First 10 words:", words[:10])

    sizes = [100, 500, 1_000, 5_000, 10_000, 20_000, 30_000, 40_000, 50_000]

    insert_results = benchmark_insert(words, sizes)
    fixed_search_results = benchmark_search_fixed_sample(words, sizes)
    random_search_results = benchmark_search_random_sample(words, sizes)

    # Compare with set
    compare_with_set(words)

    # Compare TSTree and BTree
    random.shuffle(words)
    hold_out_sample = words[-100:]
    insert_sample = words[:-100]
    compare_btree_tstree(insert_sample, hold_out_sample, prefix="ca")
