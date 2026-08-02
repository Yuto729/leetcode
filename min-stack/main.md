# Min Stack

Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

Implement the MinStack class:

MinStack() initializes the stack object.
void push(int value) pushes the element value onto the stack.
void pop() removes the element on the top of the stack.
int top() gets the top element of the stack.
int getMin() retrieves the minimum element in the stack.
You must implement a solution with O(1) time complexity for each function.

## Step1

要素のpush, pop, top自体は普通のスタックを使えば良いが、問題は最小値をO(1)で取ってくるためのデータ構造を別で持っておく必要があること。

最小値を継続的に更新できるデータ構造としては、

- ヒープ
- 小さい順に並べた数字のインデックスの配列, 更新にO(logn)
- 最小値だけを常に追跡する -> pop後の新しい最小値はどうする？O(n)でまた計算するか. 平均O(1)にならない
- 前の最小値の参照を記録する -> スタックの構造を考えるとこれで良さそう。正確にはインデックスを記録する

最小値のインデックスの更新履歴を持っておくと、今の最小値がpopされたとして、その値が挿入される前の最小値をO(1)で参照することができる。スタックのpopは必ず挿入順と逆順にしかできないのでこれで問題なさそう

Space: O(N)

```py
class MinStack:

    def __init__(self):
        self.stack = []
        self.min_value_indices = []

    def push(self, value: int) -> None:
        self.stack.append(value)
        if not self.min_value_indices or value < self.stack[self.min_value_indices[-1]]:
            self.min_value_indices.append(len(self.stack) - 1)

    def pop(self) -> None:
        if len(self.stack) - 1 == self.min_value_indices[-1]:
            self.min_value_indices.pop()

        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.stack[self.min_value_indices[-1]]
```

test

push 2 -> stack=[2], min_value_indices=[0]
push 3 -> stack=[2,3], min... =[0]
push 4 -> stack=[2,3,4]
pop -> stack=[2,3]
top -> 3
getMin -> 2
pop -> stack=[2]
push 1 -> stack=[2,1] min_value_indices=[0,1]
pop -> min_value_indices=[0], stack=[2]
getMin -> 2

edge case

- 空のスタックへのpop, top, getMin
- 同じ最小値が連続でpushされる時 -> 今の実装だとエラーのはず 更新ではないのでmin_value_indicesには先に出てきた方しか記録されないが、後に出てきた方がpopされても最小値は変わらないので問題がない

最小値を記録する方のスタックは値を入れて単調スタックにしてもできそう。この場合は広義単調減少にしないといけない

```py
class MinStack:

    def __init__(self):
        self.stack = []
        self.min_values = []

    def push(self, value: int) -> None:
        self.stack.append(value)
        if not self.min_values or value <= self.min_values[-1]:
            self.min_values.append(value)

    def pop(self) -> None:
        if self.top() == self.min_values[-1]:
            self.min_values.pop()

        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_values[-1]
```

スタックを１つにして各要素を(value, その時点での最小値)で持つ方法もある。空間計算量は増大するがわかりやすい

## Step3

空スタックへの操作はエラーで統一

```py
class MinStack:

    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, value: int) -> None:
        self.stack.append(value)
        if not self.min_stack or value <= self.min_stack[-1]:
            self.min_stack.append(value)

    def pop(self) -> None:
        if not self.stack:
            raise ValueError("stack is empty")

        if self.min_stack and self.stack[-1] == self.min_stack[-1]:
            self.min_stack.pop()

        self.stack.pop()

    def top(self) -> int:
        if not self.stack:
            raise ValueError("stack is empty")

        return self.stack[-1]

    def getMin(self) -> int:
        if not self.min_stack:
            raise ValueError("stack is empty")

        return self.min_stack[-1]
```
