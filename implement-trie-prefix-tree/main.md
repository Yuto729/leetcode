# 208. Implement Trie (Prefix Tree)

A trie (pronounced as "try") or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. There are various applications of this data structure, such as autocomplete and spellchecker.

Implement the Trie class:

Trie() Initializes the trie object.
void insert(String word) Inserts the string word into the trie.
boolean search(String word) Returns true if the string word is in the trie (i.e., was inserted before), and false otherwise.
boolean startsWith(String prefix) Returns true if there is a previously inserted string word that has the prefix prefix, and false otherwise.

Example 1:
Input
["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
Output
[null, null, true, false, true, null, true]

Explanation
Trie trie = new Trie();
trie.insert("apple");
trie.search("apple"); // return True
trie.search("app"); // return False
trie.startsWith("app"); // return True
trie.insert("app");
trie.search("app"); // return True

## Step1

- lowercase only

```py

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for c in word:
            if c in node.children:
                node = node.children[c]
                continue

            node.children[c] = TrieNode()
            node = node.children[c]

        node.is_end = True

    def search(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                return False

            node = node.children[c]

        return node.is_end

    def startsWith(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                return False

            node = node.children[c]

        return True
```

AI review

- startsWithの引数はwordというより`prefix`の方がいい
- searchとstartsWithはロジックがほぼ同じなので、共通メソッドを定義する方が良い

共通メソッドの例

```py
def _lookup(self, word):
    node = self.root
    for c in word:
        if c not in node.children:
            return None

        node = node.children[c]

    return node
```

呼び出す時は、Noneかどうかをチェックする

test

- insert("app") -> search("app") -> search("ap")

insert("app")のトレース

root = Node{}

in loop
// root = Node{a: Node{}}
// root = Node{a: Node{p: Node{}}}
// root = Node{a: Node{p: Node{p: Node{is_end=True}}}}

search("app")のトレース
node = Node{a: {p: Node{p: Node{is_end=True}}}}

in loop
// node = Node{p: Node{p: Node{is_end=True}}}}
// node = Node{p: Node{is_end=True}}}
// node = Node{is_end=True}}
node.is_end = TrueなのでTrueを返す

search("ap")のトレース
node = Node{a: {p: Node{p: Node{is_end=True}}}}

in loop
// node = Node{p: Node{p: Node{is_end=True}}}}
// node = Node{p: Node{is_end=True}}}}

node.is_end = FalseなのでFalseを返す

### follow up

- 計算量
  - 時間計算量 insert, search, startsWith -> O(N)
  - 空間計算量 O(N \* insertの回数)

- deleteをサポートするとどうなるか？

再帰でdelete関数を書くのがいい。再帰関数は「部下に、入力のwordの次の文字以降を部分木から削除してもらい、部下自身を削除しても良いかどうかを返してもらう」
削除してよければ削除をする。自身を削除して良い条件は、全ての子も削除してよく、

```py
def delete(self, word):
    def _delete(node, index):
        if index == len(word):
            if not node.is_end:
                return False # そもそも登録されていない単語

            node.is_end = False
            # 子がなければ、このノード自体を親から削除して良い
            return len(node.children) == 0

        c = word[index]
        if c not in node.children:
            return False # 単語が存在しない

        child = node.children[c]
        should_delete_child = _delete(child, index + 1)
        if should_delete_child:
            del node.children[c]
            # 自分自身も子がなく、単語の終端でもないなら親から削除して良い
            return len(node.children) == 0 and not node.is_end

        return False

    _delete(self.root, 0)
```

## Step3

```py
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()

            node = node.children[c]

        node.is_end = True

    def search(self, word: str) -> bool:
        last_character_node = self._lookup(word)
        if last_character_node is None:
            return False

        return last_character_node.is_end

    def startsWith(self, prefix: str) -> bool:
        last_character_node = self._lookup(prefix)
        return last_character_node is not None

    def _lookup(self, word: str) -> TrieNode | None:
        node = self.root
        for c in word:
            if c not in node.children:
                return None

            node = node.children[c]

        return node
```
