from collections import defaultdict
from trie import Trie

class Homework(Trie):
    def __init__(self):
        super().__init__()
        self._words = set()
        self._suffix_count = defaultdict(int)

    def put(self, key, value=None):
        super().put(key, value)
        if isinstance(key, str) and key not in self._words:
            self._words.add(key)
            for i in range(len(key)):
                self._suffix_count[key[i:]] += 1
            self._suffix_count[""] += 1

    def delete(self, key):
        if isinstance(key, str) and key in self._words:
            for i in range(len(key)):
                s = key[i:]
                self._suffix_count[s] -= 1
                if self._suffix_count[s] == 0:
                    del self._suffix_count[s]
            self._suffix_count[""] -= 1
            if self._suffix_count[""] == 0:
                del self._suffix_count[""]
            self._words.remove(key)
        return super().delete(key)

    def count_words_with_suffix(self, pattern) -> int:
        if not isinstance(pattern, str):
            raise TypeError("pattern must be a string")
        if not self._words:
            return 0
        return self._suffix_count.get(pattern, 0)

    def has_prefix(self, prefix) -> bool:
        if not isinstance(prefix, str):
            raise TypeError("prefix must be a string")
        if not self._words:
            return False
        if prefix == "":
            return True
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        if node.value is not None:
            return True
        stack = [node]
        while stack:
            cur = stack.pop()
            if cur.value is not None:
                return True
            stack.extend(cur.children.values())
        return False

    
if __name__ == "__main__":
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    # Перевірка кількості слів, що закінчуються на заданий суфікс
    assert trie.count_words_with_suffix("e") == 1  # apple
    assert trie.count_words_with_suffix("ion") == 1  # application
    assert trie.count_words_with_suffix("a") == 1  # banana
    assert trie.count_words_with_suffix("at") == 1  # cat

    # Перевірка наявності префікса
    assert trie.has_prefix("app") == True  # apple, application
    assert trie.has_prefix("bat") == False
    assert trie.has_prefix("ban") == True  # banana
    assert trie.has_prefix("ca") == True  # cat
