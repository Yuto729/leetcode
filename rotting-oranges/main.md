# Rotting Oranges

You are given an m x n grid where each cell can have one of three values:

0 representing an empty cell,
1 representing a fresh orange, or
2 representing a rotten orange.
Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.

Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return -1.

Ex
Input: grid = [[2,1,1],[1,1,0],[0,1,1]]
Output: 4

## Step1

レベル別DFSで処理する。気をつける必要がある点としては

- キューに入るのは「ちょうど今腐ったオレンジ」なので、全てが腐った後も1回余分にループを回してしまう。なので-1からスタートするか最後に引く必要がある。
- 上記の操作をするとき、「一度もループに入らないかつ最初からフレッシュなオレンジが0個」のケースで不整合が生じるのでエッジケースとして処理する

```py
class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        current_level = []
        fresh_count = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 2:
                    current_level.append((i, j))
                elif grid[i][j] == 1:
                    fresh_count += 1
        if fresh_count == 0:
            return 0

        minutes = -1
        direction = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        while current_level:
            next_level = []
            minutes += 1
            for r, c in current_level:
                for dr, dc in direction:
                    next_r, next_c = r + dr, c + dc
                    if not (0 <= next_r < m and 0 <= next_c < n):
                        continue

                    if grid[next_r][next_c] == 2:
                        continue

                    if grid[next_r][next_c] == 1:
                        grid[next_r][next_c] = 2
                        next_level.append((next_r, next_c))
                        fresh_count -= 1

            current_level = next_level

        if fresh_count != 0:
            return -1

        return minutes
```

次のようにするとエッジケースへの対応が必要なくなる。
ループの条件を「直前に腐ったばかりのオレンジが存在する」かつ「まだフレッシュなオレンジが存在する」とすればループから抜けた時点がフレッシュなオレンジがちょうど無くなった時刻となるので、`minutes`をそのままreturnできる

`grid[next_r][next_c] == 2`の分岐はいらない

```py
class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        rotten = []
        fresh_count = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 2:
                    rotten.append((i, j))
                elif grid[i][j] == 1:
                    fresh_count += 1
        minutes = 0
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        while rotten and fresh_count:
            minutes += 1
            next_rotten = []
            for r, c in rotten:
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                        grid[nr][nc] = 2
                        fresh_count -= 1
                        next_rotten.append((nr, nc))
            rotten = next_rotten

        return minutes if fresh_count == 0 else -1
```

## Step2

- https://github.com/kazuki-official/leetcode/pull/102/changes
  - ループ中でearly returnすれば最後に1引いたりループの条件を複雑にする必要がなくなる

```py
while rotten_oranges:
    next_rotten_oranges = []
    minutes += 1
    for r, c in rotten_oranges:
        for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if r + dr < 0 or len(grid) <= r + dr or c + dc < 0 or len(grid[0]) <= c + dc:
                continue
            if grid[r + dr][c + dc] == FRESH:
                grid[r + dr][c + dc] = ROTTEN
                num_fresh_oranges -= 1
                if num_fresh_oranges == 0:
                    return minutes
                next_rotten_oranges.append((r + dr, c + dc))
                continue
    rotten_oranges = next_rotten_oranges
```

- https://github.com/nittoco/leetcode/pull/49/changes
  - `if all(cell == self.EMPTY for row in grid for cell in row):`
  - `if any(cell == self.FRESH for row in rotting_grid for cell in row):`
  - カウントじゃなくて全セルを１行で参照する。allとanyの中身はgenerator

## Step3

Time: O(m\*n)
Space: O(m\*n)

```py
class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        rotten = []
        m, n = len(grid), len(grid[0])
        fresh_count = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    fresh_count += 1
                    continue

                if grid[i][j] == 2:
                    rotten.append((i, j))

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        minutes = 0
        while rotten and fresh_count:
            next_rotten = []
            for r, c in rotten:
                for dr, dc in directions:
                    next_r, next_c = r + dr, c + dc
                    if not (0 <= next_r < m and 0 <= next_c < n):
                        continue

                    if grid[next_r][next_c] == 1:
                        grid[next_r][next_c] = 2
                        next_rotten.append((next_r, next_c))
                        fresh_count -= 1

            rotten = next_rotten
            minutes += 1

        if fresh_count == 0:
            return minutes

        return -1
```
