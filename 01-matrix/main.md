542. 01 Matrix
Given an m x n binary matrix mat, return the distance of the nearest 0 for each cell.

The distance between two cells sharing a common edge is 1.

Ex1.
Input: mat = [[0,0,0],[0,1,0],[1,1,1]]
Output: [[0,0,0],[0,1,0],[1,2,1]]

mat
0 0 0
0 1 0
1 1 1

制約
- m == mat.length
- n == mat[i].length
- 1 <= m, n <= 10^4
- 1 <= m * n <= 10^4
- mat[i][j] is either 0 or 1.
- There is at least one 0 in mat.

## Step1
具体例で考える
mat
0 0 0
1 1 1
1 1 1

結果配列の初期化
0 0 0
0 0 0
0 0 0

0 0 0
1 1 1
x x x
0からの距離が1のセルを処理する

0 0 0
1 1 1
2 2 2

距離２のセルも終わり。距離が未定義のセルがないので終了。距離が未確定のセルをキューに入れていけば良さそう

queue = [値が1のセル]
それぞれのセルについて隣が0のものを処理し、キューから消す。キューに残ってるのは距離が2以上のセル。
次に距離が2以上のセルを処理するが、上下左右に距離が1のセルがあれば距離が2のセルとして処理ができる。周りがすべて未確定のセルならキューに戻す。
-> これだと最悪計算量が大きすぎる（O((m + n) * m * n)くらい？）

一旦考え直す
DP的に各セルに対して、左右上下のセルに記録されている0との距離の最小値に1を足せば良いと思ったが、前から走査していくと、右と下のセルは計算済みではないので最適な値が計算できない。よって2D配列の前からと後ろからの2回ループすれば全方向について最小値がわかるので答えが出る

BFSでやろうとしてハマってしまい30分以上かかってしまった
Time: O(m * n)
Space: O(m * n)

```py
class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        m = len(mat)
        n = len(mat[0])
        result = [[float('inf')] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if mat[i][j] == 0:
                    result[i][j] = 0
                else:
                    if i > 0 and j > 0:
                        result[i][j] = min(result[i - 1][j], result[i][j - 1]) + 1
                    elif i == 0 and j > 0:
                        result[0][j] = result[0][j - 1] + 1
                    elif j == 0 and i > 0:
                        result[i][0] = result[i - 1][0] + 1
                      
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if mat[i][j] == 0:
                    continue

                if i < m - 1 and j < n - 1:
                    result[i][j] = min(min(result[i + 1][j], result[i][j + 1]) + 1, result[i][j])
                elif i == m - 1 and j < n - 1:
                    result[i][j] = min(result[i][j + 1] + 1, result[i][j])
                elif j == n - 1 and i < m - 1:
                    result[i][j] = min(result[i + 1][j] + 1, result[i][j])  
        
        return result
```
test case
- 2回目のループで最小値が更新されるケース
- m = 1, n = 1のケース
- 全部ゼロ
- 角だけ1

別の実装を考えてみる。最初に考えたキューを使うBFSっぽい方法の計算量を落とすことを考える。
１のセルを起点にすると、隣が０のセルから順番に距離が更 
  新されていって、周りが1に囲まれているセルに到達するまでに時間が  
  かかってしまう。0を起点にして、隣に1があればそのセルをキューに入 
  れる。キューに入れたセルは距離を１に更新。BFSをレベル別で見て0の 
  セルをフラットにルートだとすると、次に探索するのは隣が1であると  
  ころで距離は1、そこからさらに隣が1であるセルをキューに入れて距離 
  を更新、ここで深さはレベル２になる...と繰り返す。深さの最大値はm 
   + n - 2である。

Time: O(m * n) 各セルは最大1回しかキューに入らないから
Space: O(m * n) result配列の大きさおよびキューに入るセルの総数

```py
class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        m = len(mat)
        n = len(mat[0])
        result = [[float('inf')] * n for _ in range(m)]
        frontier = []
        for i in range(m):
            for j in range(n):
                if mat[i][j] == 0:
                    frontier.append((i, j))
                    result[i][j] = 0
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        distance = 0
        while frontier:
            next_frontier = []
            distance += 1
            for r, c in frontier:
                for dr, dc in directions:
                    new_r = r + dr
                    new_c = c + dc
                    if not (0 <= new_r < m and 0 <= new_c < n):
                        continue
                    
                    if mat[new_r][new_c] == 1 and result[new_r][new_c] == float('inf'):
                        next_frontier.append((new_r, new_c))
                        result[new_r][new_c] = distance
            
            frontier = next_frontier

        return result
```

> いくつかフィードバックします。
1. 冗長な条件
```python
if mat[new_r][new_c] == 1 and result[new_r][new_c] == float('inf'):
```
`result[new_r][new_c] == float('inf')` だけで十分です。0セルは初期化時に`result`を0にセットしているので、`inf`のままのセルは必ず1です。

2. `distance`変数が不要
レベル管理のために`distance`を別で持っていますが、`result[r][c] + 1`で代替できます。これにより`next_level_frontier`も不要になり、通常のdequeを使ったシンプルなBFSになります。

```python
from collections import deque

queue = deque(frontier)
while queue:
    r, c = queue.popleft()
    for dr, dc in directions:
        ...
        if result[new_r][new_c] == float('inf'):
            result[new_r][new_c] = result[r][c] + 1
            queue.append((new_r, new_c))
```

## Step2

### `INF`変数の命名と定数の使い方

[docto-rin#73](https://github.com/docto-rin/leetcode/pull/73) 

> この変数はinfiniteではなくINFと名付けるのはやや誤解を招くので、`max_dist`などの方が意図が伝わりやすい気がします。
> また、固定の数字 (constant) という意味で大文字を使用されているものと予想しますが、関数への入力によって変化する数字なのでconstantではなく、この場合は小文字を使用するパターンの方をよく見るかなと思います。

`max_dist = num_cols + num_rows`の方がいい 

### 収束ループアプローチ（第3の解法）

[huyfififi#27](https://github.com/huyfififi/coding-challenges/pull/27)

> DFS ではなく、収束するまで row と column でループを回すという方法もあります。
> ただし、O(mn(m+n)) となり、C++ 等高速な言語を使用しないと TLE となります。

```python
updated = True
while updated:
    updated = False
    for row in range(num_rows):
        for col in range(num_cols):
            for dr, dc in directions:
                if distances[neighbor_row][neighbor_col] > distances[row][col] + 1:
                    distances[neighbor_row][neighbor_col] = distances[row][col] + 1
                    updated = True
```

Bellman-Fordに似ている「緩和を収束するまで繰り返す」アプローチ
Two-passのDPが2回で収束できるのは走査方向を工夫しているためであり、この方法はその工夫をせず収束まで繰り返している

### BFSのキューに何を入れるか

[huyfififi#27](https://github.com/huyfififi/coding-challenges/pull/27)

> 私はqueueに「最短距離未更新のセル」を入れていたが、ぱっと眺めてみると、全ての解法が、queueに「最短距離更新済みのセル」を入れていた。確かにこれなら、`while`文に入る前にqueueにセルを入れる操作が簡単になっているし、queueに追加されるセルの数も抑えられる。

未更新のセルをキューに入れるアプローチだと、あるセルに対してより短いパスが見つかるたびにキューに再追加されるので、計算量が最悪ケースでO((m + n) * mn)になる。ベルマンフォード法と本質的に同じで緩和を繰り返すアプローチになる。
一方で最短距離更新済みのセルを入れると、距離ごとに各セルが一回しかキューに入らないのでO(mn)で済む。

## Step3

BFSで練習
```py
class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        if not mat:
            return [[]]
        
        m = len(mat)
        n = len(mat[0])
        max_dist = m + n
        result = [[max_dist] * n for _ in range(m)]
        frontier = [] # (r, c)
        for i in range(m):
            for j in range(n):
                if mat[i][j] == 0:
                    frontier.append((i, j))
                    result[i][j] = 0

        directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        while frontier:
            next_frontier = []
            for r, c in frontier:
                for dr, dc in directions:
                    next_r = r + dr
                    next_c = c + dc
                    if not (0 <= next_r < m and 0 <= next_c < n):
                        continue
                    
                    if result[next_r][next_c] != max_dist:
                        continue

                    result[next_r][next_c] = result[r][c] + 1
                    next_frontier.append((next_r, next_c))
                    
            frontier = next_frontier

        return result
```

ついでにTwo Pass解法のリファクタリング
- i > 0, j > 0, i < n - 1,j < m - 1を個別にチェックし、境界条件の分岐を全て無くす

```py
class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        m = len(mat)
        n = len(mat[0])
        result = [[float('inf')] * n for _ in range(m)]
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for i in range(m):
            for j in range(n):
                if mat[i][j] == 0:
                    result[i][j] = 0
                    continue
                
                min_distance_of_neighbors = float('inf')
                if i > 0:
                    min_distance_of_neighbors = result[i - 1][j]
                if j > 0:
                    min_distance_of_neighbors = min(min_distance_of_neighbors, result[i][j - 1])

                result[i][j] = min_distance_of_neighbors + 1
        
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if mat[i][j] == 0:
                    continue
                    
                min_distance_of_neighbors = float('inf')
                if i < m - 1:
                    min_distance_of_neighbors = result[i + 1][j]
                if j < n - 1:
                    min_distance_of_neighbors = min(min_distance_of_neighbors, result[i][j + 1])

                result[i][j] = min(min_distance_of_neighbors + 1, result[i][j])

        return result
```

こっちの方が良いかも
```py
class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        m = len(mat)
        n = len(mat[0])
        result = [[float('inf')] * n for _ in range(m)]
        for r in range(m):
            for c in range(n):
                if mat[r][c] == 0:
                    result[r][c] = 0
                    continue
                
                # 上と左について距離を緩和する
                for dr, dc in [(-1, 0), (0, -1)]:
                    next_r, next_c = r + dr, c + dc
                    if not (0 <= next_r < m and 0 <= next_c < n):
                        continue

                    result[r][c] = min(result[r][c], result[next_r][next_c] + 1)

        for r in range(m - 1, -1, -1):
            for c in range(n - 1, -1, -1):
                if mat[r][c] == 0:
                    continue

                # 下と右について距離を緩和する
                for dr, dc in [(1, 0), (0, 1)]:
                    next_r, next_c = r + dr, c + dc
                    if not (0 <= next_r < m and 0 <= next_c < n):
                        continue

                    result[r][c] = min(result[r][c], result[next_r][next_c] + 1)
            
        return result
```

### 類題

- [flood-fill](../flood-fill/)
- [number-of-islands](../number-of-islands/)
- [max-area-of-island](../max-area-of-island/)