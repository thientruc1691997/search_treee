import time
import random
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import matplotlib.pyplot as plt
from btree.btree import Btree
from tstree.tstree import TSTree


def load_words(path):
    with open(path) as file:
        return [line.strip() for line in file if line.strip()]


def time_function(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return result, end - start


def prefix_search_plot(words):
    sizes = [100, 500, 1_000, 5_000, 10_000, 20_000, 30_000, 40_000, 50_000]
    samples = [random.sample(words, k=size) for size in sizes]
    insert_sample = random.sample(words, k=20)
    nr_runs = 10
    times = {}

    for sample in samples:
        tstree = TSTree()
        for word in sample:
            tstree.insert(word)
        times[len(sample)] = 0.0
        for _ in range(nr_runs):
            start_time = time.time_ns()
            for word in insert_sample:
                tstree.insert(word)
            end_time = time.time_ns()
            times[len(sample)] += end_time - start_time
        times[len(sample)] /= nr_runs * 1_000_000.0

    plt.plot(times.keys(), times.values())
    plt.title("TSTree Insert Time vs Dataset Size")
    plt.xlabel("Number of Words")
    plt.ylabel("Insert Time (ms)")
    plt.grid(True)
    plt.show()


def compare_with_set(words):
    random.shuffle(words)
    hold_out_sample = words[-100:]
    insert_sample = words[:-100]

    # TSTree insert
    word_tstree = TSTree()
    for word in insert_sample:
        word_tstree.insert(word)

    # Set insert
    word_set = set()
    for word in insert_sample:
        word_set.add(word)

    # Time set search
    _, set_search_time = time_function(lambda: sum(word in word_set for word in hold_out_sample))

    # Time tstree search
    _, tstree_search_time = time_function(lambda: sum(word_tstree.search(word) for word in hold_out_sample))

    print("\nSet vs TSTree Search Time:")
    print(f"Set search:    {set_search_time:.4f}s")
    print(f"TSTree search: {tstree_search_time:.4f}s")


def compare_btree_tstree(insert_sample, hold_out_sample, prefix="car"):
    print(f"\n🔍 Inserting {len(insert_sample)} words...")

    btree = Btree()
    tstree = TSTree()

    # Insert
    _, btree_insert_time = time_function(lambda: [btree.insert(w) for w in insert_sample])
    _, tstree_insert_time = time_function(lambda: [tstree.insert(w) for w in insert_sample])

    # Search
    _, btree_search_time = time_function(lambda: [btree.search(w) for w in hold_out_sample])
    _, tstree_search_time = time_function(lambda: [tstree.search(w) for w in hold_out_sample])

    # All strings
    _, btree_all_time = time_function(btree.all_strings)
    _, tstree_all_time = time_function(tstree.all_strings)

    # Prefix search
    _, tstree_prefix_time = time_function(tstree.starts_with, prefix)

    print("\nPerformance Summary:")
    print(f"{'Operation':<20}{'Btree':>12}{'TSTree':>12}")
    print(f"{'-'*44}")
    print(f"{'Insert':<20}{btree_insert_time:12.4f}{tstree_insert_time:12.4f}")
    print(f"{'Search (100)':<20}{btree_search_time:12.4f}{tstree_search_time:12.4f}")
    print(f"{'All Strings':<20}{btree_all_time:12.4f}{tstree_all_time:12.4f}")
    print(f"{'Prefix Search':<20}{'N/A':>12}{tstree_prefix_time:12.4f}")


if __name__ == "__main__":
    DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'corncob_lowercase.txt')
    words = load_words(DATA_PATH)
    hold_out_sample = words[-100:]
    insert_sample = words[:-100]
    random.shuffle(insert_sample) 
    compare_btree_tstree(insert_sample, hold_out_sample)
    compare_with_set(words)
    prefix_search_plot(words)
