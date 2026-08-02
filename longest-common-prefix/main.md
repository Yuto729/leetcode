14. Longest Common Prefix

Write a function to find the longest common prefix string amongst an array of strings.
If there is no common prefix, return an empty string "".

Example 1:
Input: strs = ["flower","flow","flight"]
Output: "fl"

Example 2:
Input: strs = ["dog","racecar","car"]
Output: ""
Explanation: There is no common prefix among the input strings.
 
Constraints:
- 1 <= strs.length <= 200
- 0 <= strs[i].length <= 200
- strs[i] consists of only lowercase English letters if it is non-empty.


Approach
i文字目が等しいかどうかを順番に見ていくことにする。基準となる文字列は一番短い文字列にする

```Py
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        shortest_len = len(strs[0])
        shortest_str = strs[0]
        for s in strs:
            if shortest_len > len(s):
                shortest_str = s
                shortest_len = len(s)

        common_prefix = []
        for i, c in enumerate(shortest_str):
            for s in strs:
                if s == shortest_str:
                    continue
                    
                if s[i] != c:
                    return "".join(common_prefix)

            common_prefix.append(c)
        
        return "".join(common_prefix)
```

`strs[0]`基準にした方がわかりやすい
Time: O(NL)
Space: O(L)
```py
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        common_prefix = []
        for i, current_char in enumerate(strs[0]):
            for s in strs:
                if i == len(s) or s[i] != current_char:
                    return "".join(common_prefix)
            
            common_prefix.append(current_char)

        return "".join(common_prefix)
```

test case
- [flower,flow,flight]
- [ice,public,cat] 共通接頭語なし
- [flower,flow,flowing] 末尾に達してearly return
- [flow,flow,flow] 最後のreturnに辿り着く
- [a] 1文字列
- ["",""] -> 外側ループが1回も実行されないケース
([] -> 本問題では想定されていないケース)

### 分割統治法
都度半分に配列を分けてcommon prefixを計算する. 分割統治法は並列化に向いている
- Time: O(NL)
再帰の深さはlog N。一番下のレイヤーの計算について、2つの文字列のcommon prefixを計算するのにO(L), そして、文字列の組数はN/2組。よって、O(L * N/2)
その一個上のレイヤーは、組数が、N/4なので、O(L * N/4)
全体で、L * N * (1/2 + 1/4 + ...+1) = O(LN). 2分木を想像すると良い
- Space: O(Nlog N)

```py
class Solution:
    def get_common_prefix(self, left, right):
        if len(left) > len(right):
            left, right = right, left
        
        for i, c in enumerate(left):
            if right[i] != c:
                return left[:i]

        return left

    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ""
            
        if len(strs) == 1:
            return strs[0]

        n = len(strs)
        prefix_of_left = self.longestCommonPrefix(strs[:n // 2])
        prefix_of_right = self.longestCommonPrefix(strs[n // 2:])
        return self.get_common_prefix(prefix_of_left, prefix_of_right)
```
- スライスのコピーコストが重いので、インデックスを引数にとる再帰関数にすると良い

### 二分探索
答えの長さは、[0, min_len - 1]の間にあるので、二分探索でそのポイントを探す。
述語：「全文字列がstrs[0][:mid]をprefixにもつか」
-> Trueとなる一番最後のインデックスを求めれば良い -> bisect_right

不変条件: left以下では、上記の述語はTrue, rightより後ろではFalseとなる。
探索範囲は(left, right]であり、left=rightとなるところで探索が終了する

Time: O(NLlog L)
Space: O(L)
```py
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ""

        min_len = min(len(s) for s in strs)
        left = 0
        right = min_len
        while left < right:
            # (left, right]が探索範囲
            mid = (left + right + 1) // 2
            if all(s.startswith(strs[0][:mid]) for s in strs):
                left = mid
            else:
                right = mid - 1
        
        return strs[0][:left] # memo: left=0のケースの場合分けはいらない
```
Edge Case
- ["",""] -> ループには入らず、`strs[0][:0]` -> ""となるのでok
    - pythonのスライスは範囲外のインデックスを渡してもエラーにならず補完してくれる
    - GoとかJavaだと無理っぽい

- 探索範囲が左開区間なのがやりづらい。「全文字列がstrs[0][:k]をprefixにもつか」が最初にFalseになるインデックス kを探して、最後に`strs[0][:k - 1]`を返すようにするとbisect leftの挙動になる

### ソート
strsをソートして、最初と最後の文字列のcommon prefixをとればそれが答えになる

### Trie木
strsをデータセットとして、プレフィックス検索クエリが複数個連続で来る場合はTrieを使うと良い
1. 全単語をTrieに挿入する
2. rootから降りていき、次の条件のノードに到達したら停止
    - 子が２つ以上ある（そこで分岐する=それ以上は共通ではない）
    - 子が1つでも現在のノードが単語の終端である
上記の作業で通った文字列がLCPになる

```py
class TrieNode:
    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            
            node = node.children[c]
        node.is_end_of_word = True
    
    def search(self, word: str) -> bool:
        node = self.root
        for c in word:
            if c not in node.children:
                return False
            
            node = node.children[c]
        
        return node.is_end_of_word
    
    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for c in prefix:
            if c not in node.children:
                return False
            
            node = node.children[c]
        
        return True

class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        trie = Trie()
        for s in strs:
            trie.insert(s)
        
        common_prefix = []
        node = trie.root
        while len(node.children) == 1 and not node.is_end_of_word:
            c, next_node = next(iter(node.children.items()))
            common_prefix.append(c)
            node = next_node
        
        return "".join(common_prefix)
```
エッジケース
["","flow"]
    - Trieのノードは以下のようになる
        root(end) - f - l - o - w(end)
    - rootに終端マーカーがついているので一回もループに入らず、`""`を返す

[]
    - return節しか通らない

follow up
- str[i]がlower case以外も含む時
    - ASCIIの場合はTrie以外の解法に変化はない
- Unicode全体の場合は次のような問題が出てくる
    - utf-16でエンコーディングする場合、16bitのコードユニット２つで文字を表す場合がある（サロゲートペア）。Unicodeの特別な領域を２つ組み合わせている
        - s[0]だとサロゲートの片方のみ表すのでインデックスと文字が対応しない
        - Pythonではstrはコードポイント列なので問題ないが、Javaなどではutf-16エンコーディングかつ文字列型がバイト列なので問題になる
        - utf-8は、可変長バイト列（1~4byte）をコードポイントに対応させるので上記の問題は起きない
    - Unicodeには、同じ見た目を複数のコードポイント列で表現できる機能がある。見た目は同じだが、バイト列・コードポイント列としては別物になる ex. "café(NFC)", "café(NFD)"
    -> 入力を正規化する。`unicodedata.normalize("NFC", s)` -> 合成済みになる
    
    - "Grapheme cluster" -> 「が」「❤️」など1文字と認識されるが複数のコードポイントから構成されるもの。同じ１文字でもコードポイント列が異なると上記と同じように問題になるが、正規化では対処できない。`regex`ライブラリで、`\X`がgrapheme clusterにマッチする正規表現らしいのでこれを使ってパースする。Javaなどでは標準でgrapheme clusterイテレーターがあるらしい？

## 練習
Time: O(NL)
```py
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ""

        for i, c in enumerate(strs[0]):
            for s in strs:
                if i == len(s) or s[i] != c:
                    return strs[0][:i]
            
        return strs[0]
```
test case
- ["flower","flow","flight"]
- ["flow"] for s in strs[1:]は通らない return [flow]
- ["flower","flow","flowing"] i = 4でflowの終端に来てreturn
- ["","a"] 外側ループに入らない
- ["a",""] はじめにif i == len(s)でreturn
- ["flow","flow"] 一度もif文に入らない