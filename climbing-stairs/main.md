# 70. Climbing Stairs

You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

Example
Input: n = 3
Output: 3
Explanation: There are three ways to climb to the top.

1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step

## Step1

単純なフィボナッチを実装。以下の実装だと再計算が発生するのでTLE

```py
class Solution:
    def climbStairs(self, n: int) -> int:
        if n == 0 or n == 1:
            return 1

        return self.climbStairs(n - 2) + self.climbStairs(n - 1)
```

解決方法は２つある

- @cache / @lru_cacheをつけてメモ化再帰にする
- ボトムアップDP

DPのアプローチで最適化する。保持しておくべきメモは高々直近の2つなのでDP配列は必要なく、変数が２つあれば良い

Time: O(N)
Space: O(1)

```py
class Solution:
    def climbStairs(self, n: int) -> int:
        if n == 0 or n == 1:
            return 1

        one_step_before = 1
        two_step_before = 1
        for _ in range(2, n + 1):
            one_step_before, two_step_before = one_step_before + two_step_before, one_step_before

        return one_step_before
```

### Follow Up

- O(n)より速くできるか
- 1, 2段進めるではなく、一般化する。つまり進める段数の集合が与えられている場合を考える

もっと速くする方法
...

後者を考えてみる
進める段数の集合Sが与えられているとする

```py

```
