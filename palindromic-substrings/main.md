Given a string s, return the number of palindromic substrings in it.
A string is a palindrome when it reads the same backward as forward.
A substring is a contiguous sequence of characters within the string.

Example 1:
Input: s = "abc"
Output: 3
Explanation: Three palindromic strings: "a", "b", "c".

Example 2:
Input: s = "aaa"
Output: 6
Explanation: Six palindromic strings: "a", "a", "a", "aa", "aa", "aaa".
 
Constraints:
- 1 <= s.length <= 1000
- s consists of lowercase English letters.

## Answer

Two Pointer解法
配列を走査し、それぞれを中心とする。そして中心から回文になるうちは左右に引き伸ばす。一度回文にならなかったら、左右に引き伸ばしても回文ではないのでそこでストップする。注意することとしては、奇数長の回文と偶数長の回文で処理を分けること

各要素を起点に左右に伸ばせる距離を計算する操作は、"Sum of Subarray Minimums"に似ている。
Subarray系で使えるパターンかもしれない

Time: O(N^2)
Space: O(1)
```py
class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        count = 0
        for i in range(n):
            l = r = i
            while l >= 0 and r < n and s[l] == s[r]:
                # 不変条件: s[l: r + 1]が回文になる
                count += 1
                l -= 1
                r += 1
            
            l, r = i, i + 1
            while l >= 0 and r < n and s[l] == s[r]:
                count += 1
                l -= 1
                r += 1

        return count
```

ex. "aaa"
// i=0 奇数: count=1 偶数: count=2
// i=1 奇数: count=4 偶数: count=5
// i=2 奇数: count=6 偶数なし


DP解法
Time: O(N^2)
Space: O(N^2)
```py
class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        # dp[i][j]: s[i: j + 1]がpalindromeかどうか
        dp = [[False] * n for _ in range(n)]
        for i in range(n):
            dp[i][i] = True
            if i < n - 1:
                dp[i][i + 1] = s[i] == s[i + 1]

        for length in range(2, n):
            # 長さを外側で固定する。そうしないとまだ計算していないエントリを参照することになってしまう
            for i in range(n - length):
                j = i + length
                if dp[i + 1][j - 1] and s[i] == s[j]:
                    dp[i][j] = True
        
        return sum(sum(row) for row in dp)
```