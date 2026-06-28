# 133. Clone Graph

Given a reference of a node in a connected undirected graph.

Return a deep copy (clone) of the graph.

Each node in the graph contains a value (int) and a list (List[Node]) of its neighbors.

class Node {
public int val;
public List<Node> neighbors;
}

Test case format:

For simplicity, each node's value is the same as the node's index (1-indexed). For example, the first node with val == 1, the second node with val == 2, and so on. The graph is represented in the test case using an adjacency list.

An adjacency list is a collection of unordered lists used to represent a finite graph. Each list describes the set of neighbors of a node in the graph.

The given node will always be the first node with val = 1. You must return the copy of the given node as a reference to the cloned graph.

## Step1

入力としてグラフのあるノードの参照が与えられるので、そこからグラフ全体のコピーを作成し、元ノードのコピーを返却する関数を実装する問題

BFSで考える。キューに入れるのは、(元ノード, そのノードのコピー)とする。キューからアイテムを取り出し、隣接ノードを見る。隣接ノードのコピーを作成し、元ノードのコピーの隣接リストに追加する。そして、（隣接ノード, 隣接ノードのコピー）をキューに追加する
すでに訪れたノードはキューに追加したくないが、無向グラフなのでその場合でもコピーを隣接リストに追加する処理は行わないといけない。すでに訪れたノードということは、コピーも存在するので、新しくコピーを作らずにそのノードの参照を単に加えれば良い。ということはすでに訪れたノードの管理をしつつ、そのコピーを取得できる仕組みが必要であるが、ハッシュマップを使えば良さそう。キーは元ノードで、値はコピー。

隣接ノードを見るたびに、ハッシュマップを確認し、

- すでに訪れていれば、ハッシュマップの値（つまりそのノードのコピー）を今見ているコピーノードの隣接リストに追加する
- 訪れていなければ、隣接のコピーを作成し、コピーノードの隣接リストとキューに追加する

Acceptするまでに以下の点で詰まった

- BFSの中で未訪問の隣接ノードだけをコピーの隣接リストに追加するとしていた -> これだとすでに訪問済みの隣接ノードへの辺がコピーされない
- 上記の解決策として隣接ノードを追加する際に、逆向きの辺も追加すれば良いと考えた -> これだとすでに訪れたことでスキップされたノード間の辺が追加されない。（例: {1: [2, 3]}）
- 隣接ノードのコピーを毎回作成していた -> 元ノードに対応するコピーが複数できてしまう
- nodeがNoneの場合

Time: O(V + 2E)
Space: O(V + E)

```py
class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if not node:
            return None

        head = Node(val=node.val)
        queue = deque()
        queue.append((node, head))
        visited = {}
        visited[node] = head
        while queue:
            node, node_copy = queue.popleft()
            for neighbor in node.neighbors:
                if neighbor in visited:
                    # すでにコピーがある
                    node_copy.neighbors.append(visited[neighbor])
                    continue

                neighbor_copy = Node(neighbor.val)
                node_copy.neighbors.append(neighbor_copy)
                queue.append((neighbor, neighbor_copy))
                visited[neighbor] = neighbor_copy

        return head
```

test

- adjList = [[2,4],[1,3],[2,4],[1,3]]

再帰DFSで考えるともっと単純になる

- nodeを渡してコピー済みのnodeを返してもらうという仕事を再帰関数として実装する
- 返してもらったコピー済みの隣接ノードは、自分の隣接リストに追加する

```py
class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if not node:
            return None

        visited = {}
        def clone(node):
            if node in visited:
                # すでにコピーが存在する
                return visited[node]

            node_copy = Node(node.val)
            visited[node] = node_copy
            for neighbor in node.neighbors:
                node_copy.neighbors.append(clone(neighbor))

            return node_copy

        node_copy = clone(node)
        return node_copy
```

(追記)
以下のようにノードではなく、辺を訪れたかどうかのチェックに使う方法もある。

```py
class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if not node:
            return None

        clones = {node: Node(node.val)}
        queue = deque([node])
        seen_edges = set()

        while queue:
            current = queue.popleft()
            for neighbor in current.neighbors:
                if neighbor not in clones:
                    clones[neighbor] = Node(neighbor.val)
                    queue.append(neighbor)

                edge = (current, neighbor) if id(current) < id(neighbor) else (neighbor, current)
                if edge in seen_edges:
                    continue

                clones[current].neighbors.append(clones[neighbor])
                clones[neighbor].neighbors.append(clones[current])
                seen_edges.add(edge)

        return clones[node]
```
