---
tags:
  - leetcode
date: 2026-08-09
url: https://leetcode.com/problems/basic-calculator/
---

# 224. Basic Calculator

Given a string `s` representing a valid expression, implement a basic calculator to evaluate it, and return the result of the evaluation.

Note: You are not allowed to use any built-in function which evaluates strings as mathematical expressions, such as `eval()`.

Example 1:
Input: s = "1 + 1"
Output: 2

Example 2:
Input: s = " 2-1 + 2 "
Output: 3

Example 3:
Input: s = "(1+(4+5+2)-3)+(6+8)"
Output: 23

## Step1

+, -だけなので単純化して()内の計算の優先順位を一旦無視する。アキュムレーターと左右の引数に該当する変数を持っておき、左右の引数に演算子を適用 -> アキュムレーターに蓄積といった形で更新する

- 1桁の整数だけではない
  - 連続する数字を内側のwhileループで処理できるようにする
- マイナスで始まる場合
  - 初期値0に対してデフォルト+で演算子を持っておく。そうすると最初がマイナスの場合は演算子がマイナスに更新され、うまく計算される
- "1-( -2)"というケースに対応するため、演算子をintで持つようにした
  - +を1, -を-1で表す
  - 前の演算子にかけることで演算子を更新する
    - "-(-2)"がプラスとして解釈されるようになる
    - 数字の足し込み後に演算子を1に戻す

- "- (3 + (4 + 5))" というケースで、()を無視してはいけないことがわかる
  - かっこ単位で再帰的に計算するヘルパーを実装し、"("が現れたら再帰関数にかっこ内を計算させ、アキュムレーターに足す。

以上様々なコーナーケースに引っかかり50分くらいかかった

time: O(n)
space: O(n)

```py
class Solution:
    def calculate(self, s: str) -> int:
        accumulator = 0
        operator = 1
        def helper(i):
            """
                かっこ単位で計算する
            """
            accumulator = 0
            operator = 1
            while i < len(s):
                c = s[i]
                if c == ' ':
                    i += 1
                    continue

                if c == ')':
                    # 次に見るべきインデックスを返す
                    return accumulator, i + 1

                if c == '(':
                    num, i = helper(i + 1)
                    accumulator += num * operator
                    operator = None
                    continue

                if c == '+':
                    if operator is not None:
                        operator *= 1
                    else:
                        operator = 1
                if c == '-':
                    if operator is not None:
                        operator *= -1
                    else:
                        operator = -1

                if c.isdigit():
                    num = int(c)
                    while i < len(s) - 1 and s[i + 1].isdigit():
                        num = num * 10 + int(s[i + 1])
                        i += 1
                    accumulator += num * operator
                    operator = None
                i += 1

            return accumulator, i
        result, _ = helper(0)
        return result
```

ちょっと簡略化

```py
class Solution:
    def calculate(self, s: str) -> int:
        accumulator = 0
        operator = 1
        def helper(i):
            """
                かっこ単位で計算する
            """
            accumulator = 0
            operator = 1
            while i < len(s):
                c = s[i]
                if c == ' ':
                    i += 1
                    continue

                if c == ')':
                    # 次に見るべきインデックスを返す
                    return accumulator, i + 1

                if c == '(':
                    num, i = helper(i + 1)
                    accumulator += num * operator
                    operator = 1
                    continue

                if c == '+':
                    operator *= 1
                if c == '-':
                    operator *= -1
                if c.isdigit():
                    num = int(c)
                    while i < len(s) - 1 and s[i + 1].isdigit():
                        num = num * 10 + int(s[i + 1])
                        i += 1
                    accumulator += num * operator
                    operator = 1
                i += 1

            return accumulator, i
        result, _ = helper(0)
        return result
```

### 🤖レビュー

- `operator`より`sign`(符号)の方が意味があっている
- 数値読み取りの部分はインラインではなく、ヘルパ関数化した方が良い
- `if c == '+': operator *= 1` は事実上no-opなのでコメントを書いて処理は書かない方がいいのでは？
- ()を再帰的に処理できるようにしたことで、`1-(-2)`のようなケースに対応できるようになったので、マイナス符号の反転処理は必要ないかも

改善

- デフォルトの符号を正にして、`-`が出てきたとき、反転させるようにする

```py
class Solution:
    def calculate(self, s: str) -> int:
        def parse_numbers_from(i):
            num = 0
            while i < len(s) and s[i].isdigit():
                num = num * 10 + int(s[i])
                i += 1
            return num, i

        def calculate_from(i):
            """
                現在位置から)もしくは末尾まで評価をする
            """
            accumulator = 0
            sign = 1
            while i < len(s):
                c = s[i]
                if c == ')':
                    return accumulator, i + 1

                elif c == '(':
                    num, i = calculate_from(i + 1)
                    accumulator += num * sign
                    sign = 1
                    continue

                elif c == '-':
                    sign *= -1
                elif c.isdigit():
                    num, i = parse_numbers_from(i)
                    accumulator += num * sign
                    sign = 1
                    continue

                i += 1  # ')' '(' 以外(スペース, '+', '-'を処理した直後)はここで1つ進める

            return accumulator, i

        result, _ = calculate_from(0)
        return result
```

本問の制約条件は、1 <= s.length <= 3 \* 10^5なので、()が非常に多い式ではスタックオーバーフローのリスクがある。スタックでも書いてみる

### 実装2 スタック

- accumulatorと符号をセットでスタックに格納する
  - 再帰関数においてローカル変数・戻り値として引き継ぎが必要だったのはaccumulator, 符号, インデックスだったが、iterativeの場合はインデックスは順番通りに更新されるので状態としてスタックに保持する必要はない
  - 1回の再帰呼び出しで生きていたローカル変数をそのまま積む

```py
def calculate_from(i):
    accumulator = 0   # このスコープの「今までの合計」
    operator = 1       # このスコープで「次に足す値」にかける符号
    ...
    if c == '(':
        num, i = calculate_from(i + 1)   # ← 新しいローカル変数一式を持つ新フレームへ
        accumulator += num * operator     # 戻ってきたら"自分の"accumulator/operatorはそのまま生きている
```

( に入った瞬間、Pythonは新しい呼び出しフレームを作り、そこに真新しい accumulator=0, sign=1 を積む。しかし、元のフレームの accumulator と sign は消えずにコールスタック上に残っている。) で return すると、呼び出し元のフレームに戻り、その生き残っていた sign（( の直前に確定していた符号）を使って num を合体させる。
-> 「スタックに積む単位」が (accumulator, sign) になる

```py
class Solution:
    def calculate(self, s: str) -> int:
        def parse_numbers_from(i):
            num = int(s[i])
            while i < len(s) - 1 and s[i + 1].isdigit():
                num = num * 10 + int(s[i + 1])
                i += 1
            return num, i

        stack = [(0, 1)]
        i = 0
        while i < len(s):
            c = s[i]
            if c == ')':
                num, _ = stack.pop()
                accumulator, sign = stack[-1]
                accumulator += num * sign
                stack[-1] = (accumulator, 1)
            elif c == '(':
                stack.append((0, 1))
            elif c == '-':
                accumulator, sign = stack[-1]
                stack[-1] = (accumulator, sign * -1)
            elif c.isdigit():
                num, i = parse_numbers_from(i)
                accumulator, sign = stack[-1]
                accumulator += num * sign
                stack[-1] = (accumulator, 1)
            i += 1
        return stack[-1][0]
```

### 実装3 スタックを用いた別の実装

- accumulatorとsignをタプルではなく、別々のスタックのエントリとして保存する
  - (が始まるときに格納した順番と逆に取り出す

- +-が現れたときに、前の演算を確定できる
  - 最後に工夫が必要
  - 数字を読んでいる間はnumを組み立てるだけ

- whileからforにする

```py
class Solution:
    def calculate(self, s: str) -> int:
        stack = []
        result, num, sign = 0, 0, 1
        for c in s:
            if c.isdigit():
                num = num * 10 + int(c)
            elif c in '+-':
                result += sign * num
                num = 0
                sign = 1 if c == '+' else -1
            elif c == '(':
                stack.append(result)
                stack.append(sign)
                result, sign = 0, 1
            elif c == ')':
                result += sign * num
                num = 0
                prev_sign = stack.pop()
                prev_result = stack.pop()
                result = prev_result + prev_sign * result
        return result + sign * num
```

- +-だけなので、符号だけをスタックに入れることもできる
  - `-(a + b) = -a - b`分配法則を使うと、今の項に最終的にどんな符号を掛けるべきか」という符号の掛け算だけをスタックで管理すれば良くなる
  - `*/`を追加するとこの方法は使えなくなる。かっこ内の演算結果も含めてスタックに積んでいく方が素直で読みやすい

- 逆ポーランド記法に変換して評価する
  - 実は一番最初に思いついたが、明らかにめんどくさそうだったのでやめた

## Step2

- https://github.com/tom4649/Coding/pull/129
  - `s = s.replace(" ", "")`で空白を最初に消してしまう
  - BNF文法
  - 再帰下降構文解析、LL(k)文法、左再帰... (トップダウン vs ボトムアップ構文解析)
  - `int(c)`を使わない
    - 制約上グレーなら`ord(c) - ord("0")`

- https://github.com/fhiyo/leetcode/pull/8/
  - プッシュダウンオートマトンで解く
  - パーサーのエラーハンドリング
    - Leetcode上では必要ないが、フォローアップとして重要

ここら辺の話はちゃんとやったことがないので、まとめてみる
[アーティファクト（自分用）](https://claude.ai/code/artifact/9cb1986a-9cc5-4d72-94e3-b2ffc671235b)

### 実装4 再帰下降パーサー

```py
class Solution:
    def calculate(self, s: str) -> int:
        """
        expr   := term (('+' | '-') term)*
        term   := ('-')? factor
        factor := '(' expr ')' | number
        number := digit+
        """
        s = s.replace(" ", "")
        index = 0

        def expr():
            nonlocal index
            result = term()
            while index < len(s) and s[index] in "+-":
                op = s[index]
                index += 1
                result = result + term() if op == "+" else result - term()
            return result

        def term():
            nonlocal index
            if index < len(s) and s[index] == "-":
                index += 1
                return -factor()
            return factor()

        def factor():
            nonlocal index
            if index < len(s) and s[index] == "(":
                index += 1
                result = expr()
                index += 1  # ")" を読み飛ばす
                return result
            return number()

        def number():
            nonlocal index
            result = 0
            while index < len(s) and s[index].isdigit():
                result = result * 1
                index += 1
            return result

        return expr()
```

## Step3

- stackの命名
