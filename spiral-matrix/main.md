---
date: 2026-08-06
tags:
  - leetcode
url: https://leetcode.com/problems/spiral-matrix/
---

# Spiral Matrix

Given an m x n matrix, return all elements of the matrix in spiral order.

Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
Output: [1,2,3,6,9,8,7,4,5]

## Step1

1 2 3
4 5 6
7 8 9
上記の例で考えてみる。まず(0,0) -> (0,1) -> (0,2)と右方向に進む。3にきた時、すでに通ったセルを除くと(1,2)にしか進めないので6に進む。方向を転換したので今度は(1,2) -> (2,2)と進む。
9にきた時、同じくすでに通ったセルを除くと(2,1)にしか進めないので8に進む。方向転換をしたので今度は7まで進む。
例によって4にしか進めないので、(2,0) -> (1,0)へと進む。4にきたとき、1,7はすでに通ったので5にしか進めず、他に訪れていないセルがないためここで終了。

1. 同じ方向に進む
2. 同じ方向に進めない、もしくはもう訪れている場合は訪れていないセルに進み、方向を更新する

Time: O(mn)
Space: O(mn)

```py
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        visited = set()
        m, n = len(matrix), len(matrix[0])
        stack = [(0, 0)]
        visited.add((0, 0))
        direction = (0, 1)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        result = []
        while stack:
            r, c = stack.pop()
            result.append(matrix[r][c])
            nr = r + direction[0]
            nc = c + direction[1]
            if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in visited:
                stack.append((nr, nc))
                visited.add((nr, nc))
                continue

            for dr, dc in directions:
                nr = r + dr
                nc = c + dc
                if not (0 <= nr < m and 0 <= nc < n):
                    continue

                if (nr, nc) in visited:
                    continue

                stack.append((nr, nc))
                visited.add((nr, nc))
                direction = (dr, dc)
                break

        return result
```

### AIレビュー

- 「進めなくなった地点で未訪問かつ範囲内の隣接セルは高々一つしか存在しない」という性質のおかげでうまく動いてるが、スパイラルの回転順ではない
  - 回転順を[右, 下, 左, 上]にして(i + 1) % 4で回せば良い

- stackが意味をなしていない
  - その通り
  - 最初は変数に格納していたがコードが複雑になりそうだったので一旦やめた

### 実装2

仕様に沿った実装は、

- 方向を維持して次に進むと範囲外もしくはすでに訪れているセルとなるとき、
  - 次のロジックで方向を切り替えることで対応する
    - 右 -> 下 -> 左 -> 上の順に切り替える
- whileループではなくforループでループの回数を指定する
  - 無理やりstackという配列を使わなくてもよくなる

```py
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        rows, cols = len(matrix), len(matrix[0])
        DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 右, 下, 左, 上

        visited = [[False] * cols for _ in range(rows)]
        row = col = direction_index = 0
        result = []

        # 高々rows * cols回ループすれば全てのセルを訪問できる
        for _ in range(rows * cols):
            result.append(matrix[row][col])
            visited[row][col] = True

            dr, dc = DIRECTIONS[direction_index]
            next_row, next_col = row + dr, col + dc
            if not (0 <= next_row < rows and 0 <= next_col < cols) or visited[next_row][next_col]:
                direction_index = (direction_index + 1) % 4
                dr, dc = DIRECTIONS[direction_index]

            row, col = row + dr, col + dc

        return result
```

### 実装3

空間計算量をO(1)にする方法
不変条件: matrixのうち、まだ出力していないセルは常に[top, bottom] x [left, right]の長方形にぴったり一致する

```
top  → ┌─────────────┐
       │ 1  2  3  4  │  ① left→right で上辺を出力 → top += 1
       │             │
       │ 5  6  7  8  │  ② top→bottom で右辺を出力 → right -= 1
       │             │
       │ 9 10 11 12  │  ③ right→left で下辺を出力 → bottom -= 1
bottom→└─────────────┘  ④ bottom→top で左辺を出力 → left += 1
        ↑           ↑
       left       right
```

1つのループの中で、長方形の外周を1週分はぎ取り、はぎ取った分だけ境界を内側に詰める。長方形が空になったらループを終了する。
注意点

- 下辺と左辺については、厚さ1の長方形において同じ点を2回出力しないためにガードを入れる必要がある。
- 空rangeとなるケースについては、Pythonでは何も出力しないのでガードは不要。
- 境界更新のタイミングを間違えてもデバッグがしづらいコード

```py
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1
        result = []

        while top <= bottom and left <= right:
            for col in range(left, right + 1):
                result.append(matrix[top][col])
            top += 1

            for row in range(top, bottom + 1):
                result.append(matrix[row][right])
            right -= 1

            if top <= bottom:
                for col in range(right, left - 1, -1):
                    result.append(matrix[bottom][col])
                bottom -= 1

            if left <= right:
                for row in range(bottom, top - 1, -1):
                    result.append(matrix[row][left])
                left += 1

        return result
```

## Step2

- https://github.com/huyfififi/coding-challenges/pull/53/changes
  - 90度曲がることを`dx, dy = -dy, dx`と表現する
    - 回転行列だ

- https://github.com/thonda28/leetcode/pull/13/changes#r1643615710
  > 再帰を書くときには、深さがどれくらいになるかとそれを使うことのメリットがどれくらいあるかを気にしてください。

> コメントありがとうございます。うずまきを何本の直線で書けるかがそのまま再帰の深さになっているので、サイズが m x n の行列の場合だと、深さは 2 \* min(m, n) くらいですかね？今回の制約だと 1 <= m, n <= 10 なので、最大で20程度になりそうです。
> ここで再帰を使うメリットは正直あまりなさそうです。方向を与える実装をしてみようと match 文を使ったらネストがかなり深くなってしまったので、while 文のネストを取り除くためだけ（＋ while 文以外の実装をしてみたいだけ）で再帰を採用しました。

    - 深さは20程度で、ガードが一つに集約されるならそれなりにメリットはありそう

## Step3

```py
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        m, n = len(matrix), len(matrix[0])
        dr, dc = 0, 1
        r, c = 0, 0
        result = []
        visited = set()
        for _ in range(m * n):
            result.append(matrix[r][c])
            visited.add((r, c))
            next_r, next_c = r + dr, c + dc
            if not (0 <= next_r < m and 0 <= next_c < n) or (next_r, next_c) in visited:
                # 時計回りに90度回転
                dr, dc = dc, -dr
            r += dr
            c += dc

        return result
```

