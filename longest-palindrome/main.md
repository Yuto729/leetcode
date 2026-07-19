Given a string s which consists of lowercase or uppercase letters, return the length of the longest palindrome that can be built with those letters.

Letters are case sensitive, for example, "Aa" is not considered a palindrome.

Example 1:
Input: s = "abccccdd"
Output: 7
Explanation: One longest palindrome that can be built is "dccaccd", whose length is 7.

## Step1

例をみるとソートされているように見えるけど問題文には指定がない

方針
まずどの文字が何回登場するかをカウントしておくと使えそうなのでカウントをする。
abccccddを例とすると、
counter = {
a: 1
b: 1
c: 4
d: 2
}

となる。longest palindromeはdccaccdでもdccbccdでも良さそうだが、aとbを両方使うことはできない。palindromeの各文字をカウントした時、奇数回登場する文字が多くとも1つしかないとわかるので、上記例でカウンターの要素を見てlongest palindromeを構成する時、

1. aをとる。長さは1
2. 奇数回登場するaを全て取ったので、bは偶数個しか取れない。1を超えない最大の偶数は0なので0を加算
3. cは偶数回登場するので全部取って対象に配置できる. +4
4. dも同じ +2
   よって、長さの最大値は7

counter = {
a: 3
b: 5
c: 4
d: 2
}
こうなった場合でも考えてみる

1. aは奇数回登場し、まだpalindromeには奇数回登場する文字がないので、3個全部とる。+3
2. aが奇数個とったので、bは奇数個取れない。+4
3. c,dは全部取れる。

トータルの長さは13。あってそう

Time: O(n)
Space: O(1) 大文字小文字合わせて52種類しかないため

```py
class Solution:
    def longestPalindrome(self, s: str) -> int:
        char_to_freq = Counter(s)
        max_length = 0
        is_first_odd_freq = True
        for c, freq in char_to_freq.items():
            if freq % 2 == 1:
                if is_first_odd_freq:
                    max_length += freq
                    is_first_odd_freq = False
                else:
                    max_length += freq - 1
            else:
                max_length += freq

        return max_length
```

フラグを使いたくないので、トータルの長さが奇数か偶数かで場合分けするようにしてみる

```py
class Solution:
    def longestPalindrome(self, s: str) -> int:
        char_to_freq = Counter(s)
        max_length = 0
        for c, freq in char_to_freq.items():
            if freq % 2 == 1:
                if max_length % 2 == 0:
                    max_length += freq
                else:
                    max_length += freq - 1
            else:
                max_length += freq

        return max_length
```

### AIレビュー

1. 命名: char_to_freqよりfreq_by_charや単にcountsの方がPythonでは一般的。is_first_odd_freqは「奇数長の塊をまだ使っていない」という意味なので、has_used_odd_centerのような名前の方が意図が伝わります。

- has_used_odd_centerの方が確かに良さそう

2. 2つ目の実装のロジックが少しトリッキー: max_length % 2 == 0で「まだ奇数を使っていないか」を判定するのは正しいですが、これは「トータルが偶数=まだセンター未使用」という数学的事実に依存していて、読み手が一瞬で理解しにくいです。フラグ版の方が意図は明確なので、可読性重視ならフラグ版、簡潔さ重視なら2つ目、とトレードオフがあります。実務的には前者(フラグ版)の方が「なぜ動くか」を考えずに読めるので好まれることが多いです。

3. もっとシンプルな別解: 実は「奇数回登場する文字の種類数」を数えるだけで解けます。

```py
class Solution:
    def longestPalindrome(self, s: str) -> int:
        char_to_freq = Counter(s)
        odd_freq_char_count = 0
        for c, freq in char_to_freq.items():
            if freq % 2 == 1:
                odd_freq_char_count += 1

        max_length = len(s)
        if odd_freq_char_count > 0:
            # 1つだけ全部使える
            max_length -= odd_freq_char_count - 1

        return max_length
```

これは「全部使って、奇数個文字は1個ずつ余らせる(ただし中央に1個だけ使える)」という発想で、ループ内条件分岐が不要になります。どちらのアプローチも面接では良いですが、この形の方がコードレビューでは「本質を突いている」と評価されやすいです。

### フォローアップ

1. もし1文字の出現回数の合計ではなく、「実際にpalindrome文字列を構築せよ」と言われたら、アルゴリズムをどう変更しますか？(構築まで求められると、実装の難易度が上がる)
2. 文字種が大文字小文字含めてASCII 52種ではなく、Unicode全体だったら計算量・空間計算量はどう変わりますか？
3. ストリーミング入力(文字が1文字ずつ送られてきて、いつでも「今の時点でのlongest palindrome length」を聞かれる)だったらどう設計しますか？(カウンターの更新はO(1)だが、奇数カウントの追跡をどう効率化するか)
4. なぜこの問題は「使われる文字数」の問題であって、実際に部分文字列やpalindromeの並び方を考える必要がないのか説明できますか？(順序に依存しない、という問題の性質の見抜きを確認)

実際にpalindromeを構築する実装

```py
class Solution:
    def longestPalindrome(self, s: str) -> str:
        char_to_freq = Counter(s)
        half_palindrome = ""
        has_first_odd_center = False
        for c, freq in char_to_freq.items():
            if freq % 2 == 1:
                if not has_first_odd_center:
                    half_palindrome += c * (freq // 2 + 1)
                    has_first_odd_center = True
                else:
                    half_palindrome = c * (freq - 1) / 2 + half_palindrome
            else:
                half_palindrome = c * (freq / 2) + half_palindrome

        if has_first_odd_center:
            return half_palindrome[:-1] + half_palindrome[-1] + reversed(half_palindrome[:-1])

        return half_palindrome + reversed(half_palindrome)
```

修正点

- freq / 2だとfloatになるので、str \* floatで型エラーが起きる
- reversedの返り値はイテレーターなので文字列と結合できない
- +で文字列を構築すると計算量が増大
- half_palindromeを構築するときは偶数個ずつ足していって、最初に奇数回登場する文字を記録しておいてそれを最後に足すほうがロジックが簡潔になる

```py
class Solution:
    def longestPalindrome(self, s: str) -> str:
        char_to_freq = Counter(s)
        half_parts = []
        center = "" # 空文字で初期化
        for c, freq in char_to_freq.items():
            half_parts.append(c * (freq // 2))
            if freq % 2 == 1 and not center:
                center = c # 最初に奇数回登場する文字を真ん中に配置する.

        half_palindrome = "".join(half_parts)
        return half_palindrome + center + half_palindrome[::-1]
```

4. 「使われる文字数」だけ考えれば良い理由

- palindromeは「前半」と「前半の逆順」、奇数長であれば中心1文字という構造を持つ
- この構造が成立するための必要十分条件は、「各文字の出現回数が中心を除いて全て偶数であること」
- 上記の条件を満たす集合であれば文字をどの順番で並べても後半を逆順にすればpalindromeを構成できる。よって集合について考えればよく、順序は必須条件ではない

## Step3

```py
class Solution:
    def longestPalindrome(self, s: str) -> int:
        char_to_freq = Counter(s)
        odd_freq_char_count = 0
        for c, freq in char_to_freq.items():
            if freq % 2 == 1:
                odd_freq_char_count += 1

        max_length = len(s)
        if odd_freq_char_count > 0:
            max_length -= odd_freq_char_count - 1

        return max_length
```

こう書けたりもする

```py
class Solution:
    def longestPalindrome(self, s: str) -> int:
        char_to_freq = Counter(s)
        max_length = 0
        has_odd_freq_char = False
        for c, freq in char_to_freq.items():
            if freq % 2 == 0:
                max_length += freq
            else:
                has_odd_freq_char = True
                max_length += freq - 1

        if has_odd_freq_char:
            max_length += 1

        return max_length
```
