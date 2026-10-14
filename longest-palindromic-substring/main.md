---
tags:
  - leetcode
date: 2026-08-08
url: https://leetcode.com/problems/longest-palindromic-substring
---

Given a string s, return the longest palindromic substring in s.

Ex.
Input: s = "babad"
Output: "bab"
Explanation: "aba" is also a valid answer.

## Step1

最初は尺取りでいけるかなと考えてみたがどうやら無理そう。使える条件は [[leetcode/minimum-window-substrin/main|Minimum Window Substring]] 参照

Palindromeの問題はどんな解き方したか思い出してみる
s[i]が真ん中（長さが奇数とする場合）もしくは2つある真ん中のうちの左（偶数）になるpalindromeのうち一番長いものを求め、最大値を逐次更新する。
palindrome系のときは真ん中に注目するとうまく解けそう

time: O(n^2)
space: O(1)

```py
class Solution:
    def longestPalindrome(self, s: str) -> str:
        # s[longest_start:longest_end + 1]が最長のpalindrome
        # longest_start = -1
        # longest_end = -1
        # と最初定義していたが、これだとsが一文字で構成されるケースでミスる
        longest_start = 0
        longest_end = -1
        for i in range(len(s)):
            # s[i]が中心
            left, right = i, i
            while (left > 0 and right < len(s) - 1) and s[left - 1] == s[right + 1]:
                # 不変条件: ループの終わりでs[left] == s[right]
                left -= 1
                right += 1
            # s[left: right + 1]はs[i]を中心とするpalindrome
            if longest_end - longest_start + 1 < right - left + 1:
                longest_start = left
                longest_end = right

            # s[i]が2つの中心のうちの左
            # 条件ミス i < len(s) - 1と書いていた
            if i == len(s) - 1 or s[i] != s[i + 1]:
                continue

            left, right = i, i + 1
            while (left > 0 and right < len(s) - 1) and s[left - 1] == s[right + 1]:
                left -= 1
                right += 1
            # s[left: right + 1]はs[i]を中心とするpalindrome
            if longest_end - longest_start + 1 < right - left + 1:
                longest_start = left
                longest_end = right

        if longest_start > longest_end:
            return ""

        return s[longest_start: longest_end + 1]
```

### AIレビュー

- 奇数中心・偶数中心で同じ展開処理が2回書かれているのでヘルパー関数化すべき
- `if longest_start > logest_end`この条件分岐は制約条件からデッドコード

### 実装2 DP

- 走査順に注意
- time, space: O(n^2)

```py
class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        # dp[i][j] = s[i: j + 1]がPalindromeかどうか, boolen
        longest_start = 0
        longest_end = 0
        dp = [[False] * n for _ in range(n)]
        for i in range(n):
            dp[i][i] = True
        for width in range(1, n):
            for i in range(n - width):
                j = i + width
                dp[i][j] = (s[i] == s[j] and (dp[i + 1][j - 1] if j >= i + 2 else True))
                if dp[i][j] and longest_end - longest_start + 1 < j - i + 1:
                    longest_start = i
                    longest_end = j

        return s[longest_start: longest_end + 1]
```

dp[i+1][j-1] しか参照しないことを利用した空間最適化ができる。具体的には外側のループをgap（j - i）で走査し、「2つ前のgapの一次元配列」だけ保持すれば計算できる

### 実装4 DP最適化版

```py
class Solution:
    def longestPalindrome(self, s: str) -> str:
        # gapが0のとき, dp[i] = s[i: i + 1]がpalindromeかどうかを表す
        n = len(s)
        longest_start = 0
        longest_end = 0
        # dp2: gap=0の判定結果
        dp2 = [True] * n
        # dp1: gap=1の判定結果
        dp1 = [False] * n
        for i in range(n - 1):
            j = i + 1
            dp1[i] = s[i] == s[j]
            if dp1[i]:
                longest_start, longest_end = i, j
        for gap in range(2, n):
            dp = [False] * (n - gap)
            for i in range(n - gap):
                j = i + gap
                dp[i] = s[i] == s[j] and dp2[i + 1]
                if dp[i] and j - i + 1 > longest_end - longest_start + 1:
                    longest_start, longest_end = i, j
            dp2 = dp1
            dp1 = dp

        return s[longest_start: longest_end + 1]
```

### フォローアップ

- 計算量をO(n)にできるか？
  - manacherのアルゴリズムというのがあるらしい
    - https://github.com/huyfififi/coding-challenges/pull/56/
    - https://github.com/tom4649/Coding/pull/64
      - 感想をみるとかなりめんどくさそうなのでメモだけ拝借
        > 1. 奇数長の回文候補に変換する
        > 2. すでに分かっている対称位置の半径を借りる
        > 3. 足りない外側だけ追加で確認する
        > 4. より右まで届いたら center/right を更新する
        >    関数の切り出しの方法として、そもそも何に興味があるのかを考えましょう。
        >    今回の場合だと、読んでいる人は、palindromeRadii の構築に興味があるはずなので、何でそれが決まっているのかが大事で、それは残して、後は切り出せばいいように思います。
        >    そうすると、「基本的には、頭から真面目に調べていくのだが、過去の情報から計算できるときがあるのでそれを使い、過去の情報から中途半端に分からないときもあるのでそのときはそこから再開」という部分を残して後は切り出すという話なのかと思います。
        >    読む人が知りたいのは「Manacher がどうやって radius[idx] を構築しているか」なので、メインループにはその構造だけを残す。細かい左右比較や半径計算の詳細は関数に逃がすと読みやすい。

## Step3

```py
class Solution:
    def longestPalindrome(self, s: str) -> str:
        # s[longest_start:longest_end + 1]が最長のpalindrome
        longest_start = 0
        longest_end = 0
        def expand_palindrome(left, right):
            while (left > 0 and right < len(s) - 1) and s[left - 1] == s[right + 1]:
                # 不変条件: ループの各時点でs[left: right + 1]はPalindrome
                left -= 1
                right += 1
            return left, right

        for i in range(len(s)):
            # s[i]が中心
            centers = [(i, i)]
            # s[i]が2つの中心のうちの左
            if i < len(s) - 1 and s[i] == s[i + 1]:
                centers.append((i, i + 1))

            for left, right in centers:
                left, right = expand_palindrome(left, right)
                # s[left: right + 1]はs[i]を中心とするpalindrome
                if longest_end - longest_start + 1 < right - left + 1:
                    longest_start = left
                    longest_end = right

        return s[longest_start: longest_end + 1]
```

### 関連

[[部分配列系問題のパターン]]
[[leetcode/palindrome-number/main|palindrome number]]
[[leetcode/palindromic-substrings/main|palindromic substrings]]
[[leetcode/longest-palindrome/main|longest palindrome]]
[[leetcode/valid-palindrome/main|valid palindrome]]
