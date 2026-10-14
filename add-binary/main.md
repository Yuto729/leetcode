# Add Binary

Given two binary strings a and b, return their sum as a binary string.

Ex.
Input: a = "11", b = "1"
Output: "100"

## Step1

両方のstringsの末尾にポインタをおき、先頭に向かって動かしながら数字と桁上がりを足していく。
ループの終了条件は、aもbも桁が尽き、桁上がりも0であるとき

### 間違えたところ

- intへの変換忘れ
- 最後のmap忘れ

Time: O(max(len(a), len(b)))
Space: O(n)

```py
class Solution:
    def addBinary(self, a: str, b: str) -> str:
        i = len(a) - 1
        j = len(b) - 1
        carry = 0
        result = []
        while i >= 0 or j >= 0 or carry:
            digit_a = int(a[i]) if i >= 0 else 0
            digit_b = int(b[j]) if j >=0 else 0
            added_digit = (digit_a + digit_b + carry) % 2
            carry = (digit_a + digit_b + carry) // 2
            result.append(added_digit)
            i -= 1
            j -= 1

        return "".join(map(str, result[::-1]))
```

AI Review

> コードの細かい点

> 1. result[::-1] でスライスによる反転コピーを作ってから join していますが、added_digit は既に文字化できる値なので、素直に result.append(str(added_digit)) としておけば map(str, ...) が不要になり、最後は "".join(reversed(result)) とシンプルにできます（意味は同じですが余計な変換が減る）。
> 2. digit_a = int(a[i]) if i >= 0 else 0 のパターンが2回繰り返されています。今回は2箇所だけなので許容範囲ですが、3つ以上の文字列を扱うような拡張が将来あるならヘルパー関数に切り出す価値があります（今は過剰設計になるので不要）。
> 3. 変数名は carry, digit_a, digit_b, added_digit など意味が明確で良いです。i, j はポインタとして慣用的なので問題なし。

### 発展

- 一般化するとどうなる
  - 10進数までなら元のコードの2進数部分だけ変えることで書くことができるが、例えば16進数だと10以上はA~になるためその変換を実装しないといけない

```py
def add(self, a: str, b: str, base: int) -> str:
    i = len(a) - 1
    j = len(b) - 1
    carry = 0
    result = []
    while i >= 0 or j >= 0 or carry:
        digit_a = int(a[i]) if i >= 0 else 0
        digit_b = int(b[j]) if j >=0 else 0
        total = (digit_a + digit_b + carry) % base
        carry = (digit_a + digit_b + carry) // base
        result.append(str(total))
        i -= 1
        j -= 1

    return "".join(map(str, result[::-1]))
```

    - `ord(c) - ord('A') + 10` で数字に変換し、数字は`chr(num - 10 + ord('A'))`で戻す。
    - 入力文字が数字かアルファベットかは, `str.isdecimal`で判定

- 減算の場合はどうなるか

## Step2

https://github.com/huyfififi/coding-challenges/pull/2
https://github.com/kazuki-official/leetcode/pull/88

- 他の人の解法を見ると、足した桁は`total`と表現するとわかりやすそう
- `digit`か`bit`か

## Step3

```py
class Solution:
    def addBinary(self, a: str, b: str) -> str:
        i = len(a) - 1
        j = len(b) - 1
        carry = 0
        result = []
        while i >= 0 or j >= 0 or carry:
            digit_a = int(a[i]) if i >= 0 else 0
            digit_b = int(b[j]) if j >=0 else 0
            total = (digit_a + digit_b + carry) % 2
            carry = (digit_a + digit_b + carry) // 2
            result.append(str(total))
            i -= 1
            j -= 1

        return "".join(result[::-1])
```
