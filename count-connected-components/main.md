## Step1
There is an undirected graph with n nodes. There is also an edges array, where edges[i] = [a, b] means that there is an edge between node a and node b in the graph.
The nodes are numbered from 0 to n - 1.
Return the total number of connected components in that graph.

Constraints:
- 1 <= n <= 100
- 0 <= edges.length <= n * (n - 1) / 2

連結成分を求める問題っぽい. `edges`が扱いづらいので隣接リストに変換してDFSにより解く.
注意点
- ノードは孤立点も含めてn個であるのでn個のノードについてイテレーションをしないといけない.
- 無向グラフなのでエッジは両方向に追加.
- defalutdictの扱いに注意. 辞書のイテレーション中に存在しないキーにアクセスすると新しいエントリが作成されるので辞書のサイズが変わってしまう.(最初は, `for v in vertical_to_neighbors.keys(): traverse_graph(v)`と書いていたので問題が発生)

時間計算量: O(V + E)
空間計算量: O(V + E)
```py
class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        def traverse_graph(vertical):
            stack = [vertical]
            while stack:
                v = stack.pop()
                for neighbor in vertical_to_neighbors[v]:
                    if neighbor in visited:
                        continue

                    stack.append(neighbor)
                    visited.add(neighbor)

            return

        # 隣接リストだが, データ構造的にはListを使っていないのでadjacent_listだと違和感.
        vertical_to_neighbors = defaultdict(list)
        for edge in edges:
            vertical_to_neighbors[edge[0]].append(edge[1])
            vertical_to_neighbors[edge[1]].append(edge[0])
             
        visited = set()
        component_count = 0
        for v in range(n):
            if v in visited:
                continue
            
            component_count += 1
            visited.add(v)
            traverse_graph(v)

        return component_count
```

- Hintに書いてあったやり方だとUnion-Findを使っている.
注意点
- sizeの初期化はすべて1
- 今回はunion find by sizeだがrankを用いた実装もある

時間計算量: O(E * α(V))
空間計算量: O(V)
```py
class UnionFind:
    def __init__(self, n):
        self.parents = list(range(n))
        self.size = [1] * n #注意
    
    def find(self, x):
        if self.parents[x] != x:
            self.parents[x] = self.find(self.parents[x])
        
        return self.parents[x]
    
    def union(self, x, y, component_count):
        parent_x = self.find(x)
        parent_y = self.find(y)
        if parent_x == parent_y:
            return component_count

        if self.size[parent_x] < self.size[parent_y]:
            parent_x, parent_y = parent_y, parent_x
        
        component_count -= 1
        self.parents[parent_y] = parent_x
        self.size[parent_x] += self.size[parent_y]
        return component_count

class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        union_find = UnionFind(n)
        component_count = n
        for edge in edges:
            component_count = union_find.union(edge[0], edge[1], component_count)

        return component_count
```
- component_countはUnionFindのメンバ変数にしてしまったほうが良いかも.

## Step2 他の人のコード・コメントを読む. 他の解法を考察する

- 隣接行列で実装したパターン
- 計算量: O(V^2)
https://github.com/5ky7/arai60/pull/22/changes#diff-0c860cd754249868513e4f9054206317fa33d0f548fc3896ac2b3e11822fd852R56

```py
class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        def traverse_graph(vertical):
            stack = [vertical]
            while stack:
                v = stack.pop()
                for neighbor in range(n):
                    if adjacent_matrix[v][neighbor] == 0:
                        continue

                    if neighbor in visited:
                        continue

                    stack.append(neighbor)
                    visited.add(neighbor)
            return
        
        # 隣接行列
        adjacent_matrix = [[0] * n for _ in range(n)]
        for edge in edges:
            adjacent_matrix[edge[0]][edge[1]] = 1
            adjacent_matrix[edge[1]][edge[0]] = 1
             
        visited = set()
        component_count = 0
        for v in range(n):
            if v in visited:
                continue
            
            component_count += 1
            visited.add(v)
            traverse_graph(v)

        return component_count
```
- 隣接リストをListを用いて実装する
https://github.com/docto-rin/leetcode/pull/28/changes#diff-4f6b01b75cf61fa706e6463e0a6840a6a0685f9f0cfcc46cc7dfb3530e908b18R34
スパースなグラフの場合にDictのほうが良いかも

- visitedをsetではなく, 長さnのリストにするのもあり. アクセスの計算量を考えるとsetを使うメリットはあまりなさそう. スパースであれば最初にn個分メモリを確保するのが無駄になるのでsetのほうがいいかも
```py
# 初期化
visited = [False] * n

# ノードvをvisitedへ追加
visited[v] = True
```

BFS/DFSの違い
- https://github.com/yas-2023/leetcode_arai60/pull/19/changes#r2442600915 
> グラフの構造によりますが、stack/queueに一度に入る要素の数が変わって、必要なメモリが多少変わるケースもあるかもしれません。(例えば、完全にバランスした二分木みたいな構造だと、ノードの数をNとするとBFSでは最後N/2ぐらいの要素が同時に入りますが、DFSだとlogNぐらいで済みそうです。)

逆に1直線上にリンクがつながっている場合だと, DFSだとスタックの最大サイズはNだがBFSだと常に1になる
他にはDFSでは最初に深いパスに入ってしまうとBFSより非効率になることが考えられる

- Union Findの経路圧縮には3つほど方法がある
https://en.wikipedia.org/wiki/Disjoint-set_data_structure#Find
https://github.com/yas-2023/leetcode_arai60/pull/19/changes#r2442539560
    - 完全経路圧縮 (full path compression): 今回の方法
    - Two-passの完全経路圧縮
    - 経路分割 (path splitting): 祖父に付け替える
    - 経路半減 (path having): 上記のPRで実装されているもの, 1つおきに祖父に付け替える

[_, 1, 1, 2, 3] （0は未使用）
に対して,
| 方法 | 結果 | 更新回数 |
|------|------|----------|
| 完全経路圧縮 | `[1,1,1,1]` 全員ルート直結 | 3回 |
| 経路分割 | `[1,1,1,2]` 1段ずつ縮む | 3回 |
| 経路半減 | `[1,1,2,2]` 1つおきに縮む | 2回 |



## Step3
```py
class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        def traverse_graph(start):
            node_to_visit = [start]
            visited.add(start)
            while node_to_visite:
                node = node_to_visite.pop()
                for neighbor in node_to_neighbors[node]:
                    if neighbor in visited:
                        continue
                    
                    node_to_visite.append(neighbor)
                    visited.add(neighbor)
            
            return
        
        node_to_neighbors = defaultdict(list)
        for edge in edges:
            node_to_neighbors[edge[0]].append(edge[1])
            node_to_neighbors[edge[1]].append(edge[0])

        visited = set()
        num_components = 0
        for node in range(n):
            if node in visited:
                continue
            
            num_components += 1
            traverse_graph(node)

        return num_components

```