import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tstree.tstree import TSTree 


# Step 1: Load insert_words
with open('/Users/nguyentruc/Desktop/UHasselt/Concept of Data Science/ternary-search-tree/data/insert_words.txt') as file:
    words = [line.strip() for line in file if line.strip()]

# Step 2: Insert into TSTree
tst1 = TSTree()
for word in words:
    tst1.insert(word)

# Step 3: Remove duplicates
unique_words = set(words)

# Step 4: Check number of unique words
assert len(tst1) == len(unique_words), f'{len(tst1)} in tree, expected {len(unique_words)}'

# Step 5: Check that all inserted words are searchable
for word in unique_words:
    assert tst1.search(word), f"Word '{word}' should be found in the tree."

# Step 6: Check all_strings contains only and exactly those words
all_strings = tst1.all_strings()
assert len(all_strings) == len(unique_words), f"Expected {len(unique_words)} unique words, but got {len(all_strings)}"
for word in all_strings:
    assert word in unique_words, f"Word '{word}' is not in the set of unique words"

# Step 7: Check that not_insert_words are NOT found
with open('/Users/nguyentruc/Desktop/UHasselt/Concept of Data Science/ternary-search-tree/data/not_insert_words.txt') as file:
    for line in file:
        word = line.strip()
        if word:  # skip empty lines
            assert not tst1.search(word), f"Word '{word}' should not be found in the tree."
