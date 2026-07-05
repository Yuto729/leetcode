# 150. Evaluate Reverse Polish Notation

You are given an array of strings tokens that represents an arithmetic expression in a Reverse Polish Notation.

Evaluate the expression. Return an integer that represents the value of the expression.

Note that:

- The valid operators are '+', '-', '\*', and '/'.
- Each operand may be an integer or another expression.
- The division between two integers always truncates toward zero.
- There will not be any division by zero.
- The input represents a valid arithmetic expression in a reverse polish notation.
- The answer and all the intermediate calculations can be represented in a 32-bit integer.

Example 1:
Input: tokens = ["2","1","+","3","*"]
Output: 9
Explanation: ((2 + 1) \* 3) = 9

Example 2:
Input: tokens = ["4","13","5","/","+"]
Output: 6
Explanation: (4 + (13 / 5)) = 6

Example 3:
Input: tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
Output: 22
Explanation: ((10 _ (6 / ((9 + 3) _ -11))) + 17) + 5
= ((10 _ (6 / (12 _ -11))) + 17) + 5
= ((10 _ (6 / -132)) + 17) + 5
= ((10 _ 0) + 17) + 5
= (0 + 17) + 5
= 17 + 5
= 22

## Step1

- 数字は負もありえる
- 0除算はない前提でよいか？
- 丸める際は、0の方向に丸める

オペレーターに遭遇するまで、オペランドをスタックに積む。オペレーターに遭遇したら、スタックから２つ値をpopして左のオペランドと右のオペランドとする。演算結果はスタックに書き戻す。

Time: O(N)
割り算の時に、Python組み込みの`//`を使うとうまくいかない -> なぜか？

```py
class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        operands = []
        operators = ["+", "-", "*", "/"]

        def calculate(left: int, right: int, operand: str):
            if operand == "+":
                return left + right
            elif operand == "-":
                return left - right
            elif operand == "*":
                return left * right
            elif operand == "/":
                return int(left / right)
            else:
                raise ValueError("invalid operand")

        for token in tokens:
            if token in operators:
                right = operands.pop()
                left = operands.pop()
                operands.append(calculate(left, right, token))
                continue

            operands.append(int(token))

        return operands.pop()
```

basic case

- tokens = ["4","13","5","/","+"]
  // s = []
  in for loop
  // s = [4]
  // s = [4, 13]
  // s = [4, 13, 5]
  // token = / -> left = 13, right = 5 -> s = [4, 2] (13 // 5)
  // token = + -> 6 (4 + 2)

edge case

- tokens = ["1"]
- 数字が全部負

AI review

- `int(a / b)`の問題点

### follow up

Q. 入力に不正な式が入ってくる場合、どう改善する？

A.

- calculate関数は、割り算で0がrightに入ってこないかのチェックがまず必要。
- トークンの処理で、有効なオペレータである場合、有効な数字である場合、無効なtokenの場合で分ける必要がある
- さらにpopをする際にガードをつけてたりない場合はエラーを出す。
- 最後にループを抜けた後で、operandsに２つ以上値が入っている場合も無効になる
- 有効な数字であることをどうやって調べるかだが, tryブロック内でint関数で変換する。例えば、int("3.5")といった場合は例外が発生するので`ValueError`を返す。int("-11")などは通らないといけない

- `operator`モジュールを使うと以下のように分岐そのものを消すことができる
  つまり、演算記号に対して関数の対応表を先に作っておく。関数はlambda関数に統一もできる

```py
import operator
OPERATORS = {
    "+": operator.add, # lambda a, b: a + b と同じ
    "-": operator.sub,
    "*": operator.mul,
    "/": lambda a, b: int(a / b),
}

if token in OPERATORS:
    right = operands.pop()
    left = operands.pop()
    operands.append(OPERATORS[token](left, right))
else:
    operands.append(int(token))
```

## Step3

エラーハンドリング版
気をつけるところ

- 割り算の定義で、`//`ではなくて`int`を使う

```py
class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        operands = []
        OPERATORS = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: int(a / b)
        }
        for token in tokens:
            if token in OPERATORS:
                if len(operands) < 2:
                    raise ValueError(f"operator {token!r} requires 2 operands, stack has {len(operands)}")

                right = operands.pop()
                left = operands.pop()
                if token == "/" and right == 0:
                    raise ValueError(f"division by zero in {left!r} / {right!r}")

                operands.append(OPERATORS[token](left, right))
                continue

            try:
                value = int(token)
                operands.append(value)
            except ValueError:
                raise ValueError(f"invalid token: {token!r}")

        if len(operands) != 1:
            raise ValueError(f"expression did not reduce to a single value: {operands!r}")

        return operands.pop()
```
