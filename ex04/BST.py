# BST.py
from typing import Optional, List
import urllib.request

class Node:
    def __init__(self, word: str):
        self.word = word
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None


class BST:
    def __init__(self, source: str = None, file: bool = False, url: bool = False, **kwargs):
        self.root: Optional[Node] = None
        self.words: List[str] = []

        if file and url:
            raise ValueError("Cannot use both file and url options at the same time.")
        if source:
            if file:
                self.words = self._read_file(source)
            elif url:
                self.words = self._read_url(source)
            self.words.sort()
            self._build_balanced(self.words)

    def _read_file(self, filename: str) -> List[str]:
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip().lower() for line in f if line.strip()]

    def _read_url(self, url: str) -> List[str]:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode("utf-8")
            return [line.strip().lower() for line in data.splitlines() if line.strip()]

    def _build_balanced(self, words: List[str]):
        if not words:
            return
        mid = len(words) // 2
        self.insert(words[mid])
        self._build_balanced(words[:mid])
        self._build_balanced(words[mid+1:])

    def insert(self, word: str):
        if not self.root:
            self.root = Node(word)
        else:
            self._insert_recursive(self.root, word)

    def _insert_recursive(self, node: Node, word: str):
        if word < node.word:
            if node.left is None:
                node.left = Node(word)
            else:
                self._insert_recursive(node.left, word)
        elif word > node.word:
            if node.right is None:
                node.right = Node(word)
            else:
                self._insert_recursive(node.right, word)

    def _collect(self, node: Optional[Node], prefix: str, results: List[str]):
        if node is None:
            return
        if node.word.startswith(prefix):
            results.append(node.word)
            self._collect(node.left, prefix, results)
            self._collect(node.right, prefix, results)
        elif prefix < node.word:
            self._collect(node.left, prefix, results)
        else:
            self._collect(node.right, prefix, results)

    def autocomplete(self, prefix: str) -> List[str]:
        results: List[str] = []
        self._collect(self.root, prefix, results)
        return results
