9. Palindrome Number
Given an integer x, return true if x is a palindrome, and false otherwise.

Example 1:
Input: x = 121
Output: true
Explanation: 121 reads as 121 from left to right and from right to left.

Example 2:
Input: x = -121
Output: false
Explanation: From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.

Example 3:
Input: x = 10
Output: false
Explanation: Reads 01 from right to left. Therefore it is not a palindrome.

Constraints:
- -2^31 <= x <= 2^31 - 1
 
Follow up: Could you solve it without converting the integer to a string?

Approach
```py
class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False

        digits = []
        while x > 0:
            digits.append(x % 10)
            x = x // 10
        
        return digits == list(reversed(digits))
```

O(1)の解法があるらしい
xを末尾の桁から半分だけreverseして前半と比較するという方法になる。
ex. 1221
- 末尾から桁をとって、reversed = 0 -> 1 -> 12
- 残った x = 122 -> 12
- x == reversedなので回文
桁の処理をどこで止めるかについて、`reversed >= x`で止めると良い

ex. 12321（長さが奇数）
- reversed = 123, x = 12で終了する
reversedが真ん中の桁を含んでいるので、reversed // 10で落とす。
reversed // 10 == xなら回文

エッジケース
- 10
- 1（一桁）
- -100

```py
class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0 or (x % 10 == 0 and x != 0):
            return False

        reversed_x = 0
        while reversed_x < x:
            reversed_x = reversed_x * 10 + x % 10
            x //= 10

        return x == reversed_x or x == reversed_x // 10
```

follow up
### なぜ整数のまま解くのか？
文字列変換版 `str(x) == str(x)[::-1]` なら1行で済むが、整数版が好ましい場面がある。
- 組み込み機器などメモリが厳しい環境
- ストリーム処理で大量に判定する場面
- 文字列ライブラリのオーバーヘッドを避けたい低レイヤ
整数版は追加メモリ O(1)、文字列版は O(d)。

### 入力が大きい場合の挙動
| 手法 | Time | Space (追加) |
|---|---|---|
| `str(x) == str(x)[::-1]` | O(d) | O(d) |
| 後半 reverse 整数版 | O(d²) ※bignum時 | O(1) |
| 桁を配列に格納する版 | O(d²) ※`//10`が毎回O(d) | O(d) |

- 64-bit 固定長整数 (C++/Java の int64): `reversed_x * 10 + digit` でオーバーフローのリスクあり。Pythonは任意精度なのでOK。
- bignum (例: 1000桁): `x // 10` や `reversed_x * 10` が1回 O(d) かかるため、ループ全体は O(d²)になる。（bignumはPythonでは30bitずつのチャンク配列として保持されているが、1回の算術演算の際にチャンクを操作するため線形時間がかかる）
この領域では 文字列版が時間的に最速

### 他の解法
- 全桁reverseする。ただしC++などではオーバーフローリスクあり

```py
class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False
        
        orignal, reversed_x = x, 0
        while x > 0:
            reversed_x = reversed_x * 10 + x % 10
            x //= 10
        
        return original == reversed_x
```

## 練習
```py
class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0 or (x != 0 and x % 10 == 0):
            return False
        
        reversed_x = 0
        while reversed_x < x:
            reversed_x = reversed_x * 10 + x % 10
            x //= 10
        
        return reversed_x == x or reversed_x // 10 == x
```
test case
- 132231
- 12321
- 123
- 1230
- 0
- -121
- 1