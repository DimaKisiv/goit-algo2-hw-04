from trie import Trie 

class Homework(Trie):
    def count_words_with_suffix(self, pattern) -> int:
        if not isinstance(pattern, str):
            raise TypeError("pattern must be a string")
        count = 0
        for w in self.keys():
            if w.endswith(pattern):
                count += 1
        return count

    def has_prefix(self, prefix) -> bool:
        if not isinstance(prefix, str):
            raise TypeError("prefix must be a string")
        if prefix == "":
            return not self.is_empty()

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
