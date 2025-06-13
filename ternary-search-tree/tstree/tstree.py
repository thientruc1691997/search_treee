class TSTreeNode:
    def __init__(self, char):
        self.char = char
        self.is_end = False
        self.left = None
        self.middle = None
        self.right = None

    def _insert(self, word, index=0):
        char = word[index]
        if char < self.char:
            if self.left is None:
                self.left = TSTreeNode(char)
            self.left._insert(word, index)
        elif char > self.char:
            if self.right is None:
                self.right = TSTreeNode(char)
            self.right._insert(word, index)
        else:
            if index + 1 == len(word):
                self.is_end = True
            else:
                if self.middle is None:
                    self.middle = TSTreeNode(word[index + 1])
                self.middle._insert(word, index + 1)

    def _search(self, word, index=0):
        char = word[index]
        if char < self.char:
            return self.left is not None and self.left._search(word, index)
        elif char > self.char:
            return self.right is not None and self.right._search(word, index)
        else:
            if index == len(word) - 1:
                return self.is_end
            return self.middle is not None and self.middle._search(word, index + 1)

    def _all_words(self, prefix=''):
        words = []
        if self.left:
            words.extend(self.left._all_words(prefix))
        if self.is_end:
            words.append(prefix + self.char)
        if self.middle:
            words.extend(self.middle._all_words(prefix + self.char))
        if self.right:
            words.extend(self.right._all_words(prefix))
        return words

    def _prefix_search(self, prefix, index=0):
        char = prefix[index]
        if char < self.char:
            return self.left._prefix_search(prefix, index) if self.left else []
        elif char > self.char:
            return self.right._prefix_search(prefix, index) if self.right else []
        else:
            if index == len(prefix) - 1:
                result = []
                if self.is_end:
                    result.append(prefix)
                if self.middle:
                    result += self.middle._all_words(prefix)
                return result
            if self.middle:
                return self.middle._prefix_search(prefix, index + 1)
            return []

    def _to_string(self, indent=''):
        repr_str = indent + repr(self) + f" (end={self.is_end})"
        if self.left is not None:
            repr_str += '\n' + self.left._to_string(indent + '  ')
        if self.middle is not None:
            repr_str += '\n' + self.middle._to_string(indent + '  ')
        if self.right is not None:
            repr_str += '\n' + self.right._to_string(indent + '  ')
        return repr_str

    def __repr__(self):
        return f"'{self.char}'"


class TSTree:
    def __init__(self):
        self.root = None

    def insert(self, word):
        if not word:
            return
        if self.root is None:
            self.root = TSTreeNode(word[0])
        self.root._insert(word)

    def search(self, word):
        if not word or self.root is None:
            return False
        return self.root._search(word)

    def all_strings(self):
        if self.root is None:
            return []
        return self.root._all_words()

    def starts_with(self, prefix):
        if not prefix or self.root is None:
            return []
        return self.root._prefix_search(prefix)

    def __len__(self):
        return len(self.all_strings())

    def __repr__(self):
        if self.root is None:
            return 'empty tree'
        else:
            return self.root._to_string()
