import os
from tstree.tstree import TSTree

class TSTreeTester:
    def __init__(self, insert_path, not_insert_path):
        self.insert_path = insert_path
        self.not_insert_path = not_insert_path
        self.tree = TSTree()
        self.inserted_words = []
        self.unique_words = set()

    def load_words(self):
        with open(self.insert_path) as file:
            self.inserted_words = [line.strip() for line in file if line.strip()]
            self.unique_words = set(self.inserted_words)

    def insert_words(self):
        for word in self.inserted_words:
            self.tree.insert(word)

    def test_insert_and_search(self):
        assert len(self.tree) == len(self.unique_words), \
            f'{len(self.tree)} in tree, expected {len(self.unique_words)}'
        for word in self.unique_words:
            assert self.tree.search(word), f"Word '{word}' should be found in the tree."

    def test_non_inserted_words(self):
        with open(self.not_insert_path) as file:
            for line in file:
                word = line.strip()
                if word:
                    assert not self.tree.search(word), f"Word '{word}' should NOT be in the tree."

    def test_all_strings(self):
        all_strings = self.tree.all_strings()
        assert len(all_strings) == len(self.unique_words), \
            f"Expected {len(self.unique_words)} unique words, but got {len(all_strings)}."
        for word in all_strings:
            assert word in self.unique_words, f"Unexpected word '{word}' in tree output."

    def run_all_tests(self):
        print("Running TSTree tests...")
        self.load_words()
        self.insert_words()
        self.test_insert_and_search()
        self.test_non_inserted_words()
        self.test_all_strings()
        print("All tests passed.")

# Run directly as a script
if __name__ == "__main__":
    base = os.path.dirname(__file__)
    insert_file = os.path.join(base, "..", "data", "insert_words.txt")
    not_insert_file = os.path.join(base, "..", "data", "not_insert_words.txt")

    tester = TSTreeTester(insert_file, not_insert_file)
    tester.run_all_tests()
