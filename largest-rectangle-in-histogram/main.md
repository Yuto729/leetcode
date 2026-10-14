---
tags:
  - leetcode
date: 2026-08-31
url: https://leetcode.com/problems/largest-rectangle-in-histogram/
difficulty: Hard
---

# 84. Largest Rectangle in Histogram

Given an array of integers `heights` representing the histogram's bar height where the width of each bar is `1`, return the area of the largest rectangle in the histogram.

Example 1:

Input: heights = [2,1,5,6,2,3]
Output: 10
Explanation: The above is a histogram where width of each bar is 1.
The largest rectangle is shown in the red area, which has an area = 10 units.

Example 2:

Input: heights = [2,4]
Output: 4

## Step1

長方形の定義から、
インデックスiとjに囲まれる長方形の面積 = min(heightsのiからjまで) \* (j - i + 1)
となるので、上記を各i, jについて最大化する
ナイーブに実装するとO(n^2)になるが、長さの最大値は10^5オーダーなのでおそらくTLEする。もっと効率的な解法を考える。

部分配列の問題と考えるとわかりやすい。つまり、heights配列内の任意の部分配列 heights[i: j + 1]に対して、その最小値に部分配列の長さをかけたものが面積となる

例

heights = [2,1,5,6,2,3]
部分配列 [5,6,2]について、最小値は2, 長さは3なので、面積は6となる。これは前にどこかで解いたパターンに似ていて、配列を先頭から見ていってそれぞれのheights[i]が最小値となる部分配列を求めれば解ける。iに対して左右に配列を伸ばしていって、heights[i]を超えたところで打ち切る

上記は単調スタックを用いて解ける。具体的には以下

- heights[i]以下となる初めてのi - k
- heights[i]未満となる初めてのi + l
  を求めると、条件を満たす部分配列の長さはl + k - 1で計算できる。片方を「未満」にしているのは、同じ高さが連続するとき、幅を取りこぼさないようにするため。部分配列は、heights[i - k + 1: i + l]となる。

トータルで30分くらいかかった。久しぶりなのでなまっている
time: O(N)
space: O(N)

```py
class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        stack = []
        n = len(heights)
        first_left_less_than_or_equal = [-1] * n
        first_right_less_than = [-1] * n
        for i in range(n):
            while stack and heights[stack[-1]] > heights[i]:
                stack.pop()
            first_left_less_than_or_equal[i] = stack[-1] if stack else -1
            stack.append(i)
        stack = []
        for i in range(n - 1, -1, -1):
            while stack and heights[stack[-1]] >= heights[i]:
                stack.pop()
            first_right_less_than[i] = stack[-1] if stack else n
            stack.append(i)

        max_area = 0
        for i in range(n):
            max_area = max(max_area, heights[i] * (first_right_less_than[i] - first_left_less_than_or_equal[i] - 1))

        return max_area
```

test cases

- [2] → 2（スタックが空のまま終わる）
- [2,2] → 4（等値の run）
- [1,2,3] → 4（単調増加、番兵でまとめて吐く）
- [3,2,1] → 4（単調減少、毎回 pop）
- [2,1,5,6,2,3] → 10
- [0,1] → 1（高さ 0 が混じる）

### AIレビュー

- first_left_less_than_or_equal / first_right_less_than は、長い上に「left/right が方向なのか位置なのか」が読み取りづらい
  - prev_smaller_or_equal / next_smallerなどが考えられる

- [-1] \* n の初期値が死んでいる
  - 必ず初期値を上書きするので、[0]\*nで十分。なぜ-1なのかを考えなくて良い

- 面積計算の行が長いので、一旦widthなどの変数に幅を格納する
- (発展) 1パスで解くことができる
  - ループを分ける方がわかりやすい

- heights[i]に対して、(strict, strict) / (strict, <=) / (<=, strict)はOK。(<=, <=)だけが壊れる

### 関連問題

- [[sum-of-subarray-minimums/main|907. Sum of Subarray Minimums]]
- [[trapping-rain-water/main|42. Trapping Rain Water]]
- [[min-stack/main|155. Min Stack]]
- [[container-with-most-water/main|11. Container With Most Water]]
- [[notes/部分配列系問題のパターン|部分配列系問題のパターン]]
- [[notes/不変条件と境界条件の設計|不変条件と境界条件の設計]]

## Step2

## Step3
