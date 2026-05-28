## Step1
- 1文字違いの単語をたどってスタートからゴールまで道をつくるときの最短経路を求める問題
最短経路を導いてくださいと言われたら樹形図を使って調べると思うのでそれをコードにしていく
- 文字シーケンスは必ずwordList順に並んでいないといけないと勘違いしていた


- 1 <= beginWord.length <= 10
- endWord.length == beginWord.length
- 1 <= wordList.length <= 5000
- wordList[i].length == beginWord.length
- beginWord, endWord, and wordList[i] consist of lowercase English letters.
- beginWord != endWord
- All the words in wordList are unique

以下のようにBFSを用いて解いた. 隣接行列を用いているのと同じような実装
wordListの長さ: N, 各文字の最大長さ: 10
時間計算量: O(N^2 * 10), 空間計算量: O(N)
```py
class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if not (endWord in wordList):
            return 0
        
        def judge_valid_pair(word1, word2):
            if len(word1) != len(word2):
                return False
            
            num_different_letters = 0
            for i in range(len(word1)):
                c1 = word1[i]
                c2 = word2[i]
                if c1 == c2:
                    continue
                
                num_different_letters += 1
            
            return num_different_letters == 1

        frontiers = deque()
        # height starts with 1
        height = 1
        visited = set()
        frontiers.append((beginWord, height))
        while frontiers:
            word, height = frontiers.popleft()
            if word == endWord:
                return height

            for i in range(len(wordList)):
                if wordList[i] in visited:
                    continue

                if judge_valid_pair(word, wordList[i]):
                    frontiers.append((wordList[i], height + 1))
                    visited.add(wordList[i])
            
        return 0
```
Runtimeは8000ms超え. 平均より1 ~ 2桁ほど遅いので計算量を1/100 ~ 1/10にしないといけない.
考えてもわからなかったのでClaudeにヒントをもらう
- 上記の実装 => 各単語について現在の単語と1文字違いのものを探す => O(N * 10)
- 発想を転換して, 現在の単語について1文字を別のアルファベットに変えた単語がwordListの中にあるか？を調べる => O(M * 26), M: 各単語の長さ (最大10). 単語を調べるときにsetを用いる.

トータルの時間計算量：O((N + N × 26 × L) × L) = O(N * L^2)、空間計算量：O(N * L)

- 上記のコードで根からの深さの意図で`height`と命名していたが, `distance`や`depth`のほうが良さそう
```py
class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if not (endWord in wordList):
            return 0
        
        word_set = set(wordList)
        lowercase_letters = string.ascii_lowercase
        frontiers = deque()
        distance = 1
        visited = set()
        frontiers.append((beginWord, distance))
        while frontiers:
            word, distance = frontiers.popleft()
            if word == endWord:
                return distance
            
            for i in range(len(word)):
                for c in lowercase_letters:
                    candidate = word[:i] + c + word[i+1: ]
                    if candidate not in word_set or candidate in visited:
                        continue

                    frontiers.append((candidate, distance + 1))
                    visited.add(candidate)
            
        return 0
```

追記
- 以下のようにレベル別に処理するとqueueに距離を入れなくて良くなる
```py
class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        def generate_neighbors(word):
            for i in range(len(word)):
                for c in string.ascii_lowercase:
                    candidate = word[:i] + c + word[i + 1: ]
                    yield candidate

        word_set = set(wordList)
        if endWord not in word_set:
            return 0

        queue = [beginWord]
        visited = set()
        num_of_words = 1
        while queue:
            next_level = []
            for word in queue:
                if word == endWord:
                    return num_of_words

                for candidate in generate_neighbors(word):
                    if candidate not in visited and candidate in word_set:
                        next_level.append(candidate)
                        visited.add(candidate)

            queue = next_level
            num_of_words += 1
            
        return 0
```

## Step2 他の人のコード・コメントなどを見る
- https://github.com/hayashi-ay/leetcode/pull/42#discussion_r1515769872
予め, 1文字違いの単語間に辺を張って無向グラフ(隣接リスト)を作るやり方. 計算量は張るがシンプル.

- https://github.com/hayashi-ay/leetcode/pull/42/changes
    - ワイルドカードパターンによるグルーピング
    - "hot" → ["*ot", "h*t", "ho*"]のように1文字を`*`で置き換えた組を作る. 同じパターンを持つ単語は1文字違いになる. 計算量がO(N * M^2)になる. 
    - パターンあたりの単語数が平均で26を超えていない限り, 小文字アルファベットすべてについてパターンを探索するよりも効率的
    - こちらも隣接リストと近い考え方

```py
class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if not (endWord in wordList):
            return 0
        # ワイルドカードパターン
        pattern_to_word = defaultdict(list)
        for word in wordList:
            for i in range(len(word)):
                pattern = f"{word[:i]}*{word[i+1:]}"
                pattern_to_word[pattern].append(word)
 
        frontiers = deque()
        distance = 1
        visited = set()
        frontiers.append((beginWord, distance))
        while frontiers:
            word, distance = frontiers.popleft()
            if word == endWord:
                return distance
            
            for i in range(len(word)):
                pattern = f"{word[:i]}*{word[i+1:]}"
                for candidate in pattern_to_word[pattern]:
                    if candidate in visited:
                        continue

                    frontiers.append((candidate, distance + 1))
                    visited.add(candidate)
            
        return 0
```
- https://discord.com/channels/1084280443945353267/1200089668901937312/1215921060411871232
> そうですね、4th ははじめに距離を全部計算しています。たぶん、探索中に隣接を探すと、時間をオーバーするので前に計算しているのかと思います。ただ、全部使うとは限らないので、ここを遅延評価するというのも選択です。そのためには、hamming_distance に @cache をつけて、adj[word] を @cache def adj(word): に変えるとかどうですか。あと、一度、lru_cache に cache_clear があるなどを見ておいてもらえると。

- https://discord.com/channels/1084280443945353267/1200089668901937312/1216123084889788486
> 頭から半分または尻尾から半分が一致しているはずなので、それでバケットを作ってバケット内でのみ比較すればいいというやりかたもありますね。(編集距離が1であるかの確認に、頭から何文字一致していて、尻尾から何文字一致しているかを足してやればいいという方法をどっかで使ったことあります。)

- https://github.com/Yusan1234/arai60/pull/1#discussion_r1841942827
> new_state_of_word = word[:i] + "*" + word[i+1:]
> うーん、上のコードが二箇所あってあまり好みではないです。
> WordNeighbors クラスを定義して、add_word(word) と get_neighbors(word) を定義し、get_neighbors が generator を返すとかにしたいですね。
> Python ならば、ペアをキーにする (word[:i], word[i+1:]) ほうがいいかもしれません。

以下のような感じになる
```py
class WordNeighbors:
    def __init__(self):
        self._pattern_to_words = defaultdict(list)

    def to_key(self, word):
        for i in range(len(word)):
            yield (word[:i], word[i+1:])

    def add_word(self, word):
        for key in self.to_key(word):
            self._pattern_to_words[key].append(word)
    
    def get_neighbors(self, word):
        for key in self.to_key(word):
            for w in self._pattern_to_words[key]:
                yield w

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0

        neighbors = WordNeighbors()
        for word in wordList:
            neighbors.add(word)

        distance = 1
        words = [beginWord]
        seen = set()
        while words:
            next_words = []
            for word in words:
                if word == endWord:
                    return distance

                for neighbor in neighbors.get_neighbors(word):
                    if neighbor in seen:
                        continue

                    seen.add(neighbor)
                    next_words.append(neighbor)
            words = next_words
            distance += 1
        return 0
```


- https://github.com/tarinaihitori/leetcode/pull/20#discussion_r1852651357
> "*" が来ると動かなくなるのが気になり、Python の場合は、タプルも dict の Key にできるのでそれも一つかなと思います。

アルファベット小文字だけという制約があるので大丈夫だが, そうではない場合も考慮しないといけない.

### フォローアップ
- 最短経路の単語列をすべて返す => バックトラック
- wordListが非常に長い場合 => 1つのパターンあたりの要素数が平均して多くなるので, 小文字アルファベット26文字を総当りするほうが良くなるかもしれない

## Step3

```py
class WordNeighbors():
    def __init__(self):
        self.pattern_to_words = defaultdict(list)

    def to_key(self, word):
        for i in range(len(word)):
            yield (word[:i], word[i+1:])

    def add_word(self, word):
        for key in self.to_key(word):
            self.pattern_to_words[key].append(word)
    
    def get_neighbors(self, word):
        for key in self.to_key(word):
            for w in self.pattern_to_words[key]:
                yield w

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0
        
        neighbors = WordNeighbors()
        for word in wordList:
            neighbors.add_word(word)

        frontiers = deque()
        distance = 1
        frontiers.append((beginWord, distance))
        visited = set()
        while frontiers:
            word, distance = frontiers.popleft()
            if word == endWord:
                return distance

            for candidate in neighbors.get_neighbors(word):
                if candidate in visited:
                    continue

                frontiers.append((candidate, distance + 1))
                visited.add(candidate)

        return 0
```