# minimum-window-substring

Given two strings s and t of lengths m and n respectively, return the minimum window substring of s such that every character in t (including duplicates) is included in the window. If there is no such substring, return the empty string "".

The testcases will be generated such that the answer is unique.

Input: s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
Explanation: The minimum window substring "BANC" includes 'A', 'B', and 'C' from string t.

## Step1

- 文字列はアルファベット大文字と小文字からなる

愚直にインデックスi ~ jまでのsubstringが条件を満たすものであるかを確かめ、さらに最小の長さを更新するものであれば、そのsubstringを記録しておく。
条件を満たすかどうかは、あらかじめ`t`に登場する文字の頻度をカウントしておき、各substringで同じようにカウントしたものと比較することで判定できる。

Time: O(m^2\*k) k: tのdistinctな文字数

```py
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        m, n = len(s), len(t)
        t_set = set(t)
        char_to_count_t = Counter(t)
        def all_char_in_window(char_to_count):
            for char, freq in char_to_count_t.items():
                if char not in char_to_count:
                    return False

                if char_to_count[char] < freq:
                    return False

            return True

        min_window_length = float('inf')
        min_window_substring = ""
        for i in range(m):
            if s[i] not in t_set:
                continue

            # windowの開始
            char_to_count = defaultdict(int)
            for j in range(i, m):
                char_to_count[s[j]] += 1
                if all_char_in_window(char_to_count):
                    if j - i + 1 < min_window_length:
                        min_window_substring = s[i: j + 1]
                        min_window_length = j - i + 1
                        break

        return min_window_substring
```

上記のコードだとTLEになってしまう。考えてもわからなかったのでAIにヒントをもらう。
i, jのTwo Pointerで考え、全体の計算量をO(m), つまり文字列を一回舐めるだけで済むようにアルゴリズムを構成すると良いらしい。この問題にTwo Pointerを適用するとして、windowは右に進んでいくイメージになるので、2つのポインタは最初は0になる。

前提として、「固定したjに対して[i, j]がtの条件を満たす最大のiは単調非減少」となる（j-1で同じようにiを見つけたとすると、jを前に1つ進めた時、[i, j]も条件を満たすので、少なくともiが後戻りすることはない）

上記を踏まえると、jを一つ進めるたびにiを動かせるだけ前に進めて最大のiを見つければ、そのjにおける最小なwindowの左端となる。全てのjについてこの貪欲操作をすればグローバルな最適解がもとまることになる。i, jは後戻りしないので高々m回しか動かない。O(m)となる

実はこれがあの尺取り法らしい. https://qiita.com/drken/items/ecd1a472d3a0e7db8dce

- 頭は常に前にしか動かない
- 尻尾も頭に追いつくために前にしか動かない
- 尻尾が一度離れた地面に再び戻ることはない

尺取り法は、以下のような問題で利用できる。

- 「条件」を満たす区間 (連続する部分列) のうち、最小の長さを求めよ
- 「条件」を満たす区間 (連続する部分列) のうち、最大の長さを求めよ
- 「条件」を満たす区間 (連続する部分列) を数え上げよ

利用できる条件は、以下のいずれかが成り立つ時。今回は2

1. 区間 [left, right) が「条件」を満たすなら、それに含まれる区間も「条件」を満たす
2. 区間 [left, right) が「条件」を満たすなら、それを含む区間も「条件」を満たす

Time: O(m\*k)

```py
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        m, n = len(s), len(t)
        t_set = set(t)
        char_to_count_t = Counter(t)
        def all_char_in_window(char_to_count):
            for char, freq in char_to_count_t.items():
                if char not in char_to_count:
                    return False

                if char_to_count[char] < freq:
                    return False

            return True

        min_window_length = float('inf')
        min_window_substring = ""
        char_to_count = defaultdict(int)
        i = 0
        for j in range(m):
            char_to_count[s[j]] += 1
            while i < m and all_char_in_window(char_to_count):
                if j - i + 1 < min_window_length:
                    min_window_length = j - i + 1
                    min_window_substring = s[i: j + 1]
                char_to_count[s[i]] -= 1
                i += 1

        return min_window_substring
```

上記の解法は、`all_char_in_window`関数内で毎回dictを走査しているので定数倍遅くなる。
Window内のある文字の個数が`t`のその文字の個数と等しくなったら「条件を満たす文字の個数」を管理する変数をインクリメントする。その変数 = tのユニークな文字の個数 となった時にWindowは条件を満たすと言えるので、この判定方法だと常にO(1)で判定できる。
全体を毎回計算するのではなく、差分だけをウォッチして集約カウンタ(必要な部分条件のうち現在満たされている個数)に反映するという微分のような発想。

- **独立した部分条件のAND**で全体条件が書ける
- 1回の操作で変化するのは局所的な状態のうちの1つだけ
- その局所的な変化は自分の閾値をまたいだかどうかをO(1)で判定できる

こんな時に使えそう

```py
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        m, n = len(s), len(t)
        t_set = set(t)
        char_to_count_t = Counter(t)
        required = len(char_to_count_t)
        min_window_length = float('inf')
        min_window_substring = ""
        char_to_count = defaultdict(int)
        i = 0
        formed = 0
        for j in range(m):
            char_to_count[s[j]] += 1
            if s[j] in t_set and char_to_count[s[j]] == char_to_count_t[s[j]]:
                formed += 1

            while i < m and formed == required:
                if j - i + 1 < min_window_length:
                    min_window_substring = s[i: j + 1]
                    min_window_length = j - i + 1
                char_to_count[s[i]] -= 1
                if s[i] in t_set and char_to_count[s[i]] < char_to_count_t[s[i]]:
                    formed -= 1
                i += 1

        return min_window_substring
```

## Step3

条件 = tに含まれる文字が重複を含んで、全て含まれるsubstring
この条件を満たすsubstringを含むsubstringも条件を満たす -> しゃくとり法が使える。
ベース: rightを固定して、条件を満たさなくなるまでleftを動かす。left == rightとなったらrightを進める。

```py
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        m = len(s)
        char_to_count_of_t = Counter(t)
        min_window_length = float('inf')
        min_window_substring = ""
        char_to_count_substring = defaultdict(int)
        left = 0
        formed = 0
        required = len(char_to_count_of_t)
        for right in range(m):
            # s[left: right + 1]がsubstring
            char_to_count_substring[s[right]] += 1
            if s[right] in char_to_count_of_t and char_to_count_substring[s[right]] == char_to_count_of_t[s[right]]:
                formed += 1
            while left <= right and formed == required:
                if right - left + 1 < min_window_length:
                    min_window_length = right - left + 1
                    min_window_substring = s[left: right + 1]

                char_to_count_substring[s[left]] -= 1
                if s[left] in char_to_count_of_t and char_to_count_substring[s[left]] < char_to_count_of_t[s[left]]:
                    formed -= 1
                left += 1

        return min_window_substring
```
