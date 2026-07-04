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

## Step2

まとめ

### 各命令が何クロックかかるかは公式ドキュメントにある（が目安）

[huyfififi#32](https://github.com/huyfififi/coding-challenges/pull/32#discussion_r2315641683)

> それぞれの命令に何クロックかかるかは、公式のドキュメントに記載されています。ただ…パイプライン、アウトオブオーダー命令実行、複数の計算ユニットによる同時実行等…複雑です。目安程度に考えておくのが良いと思います。

実行時間の見積もり（1命令 = 1〜10ns、1秒で10^8〜10^9命令）を検証する話。Intelの命令スループット/レイテンシ表が紹介されている。マニュアルの「シナリオ2/3」の見積もりの議論と直結する内容。

### `dict.get(key, default)` は default を常に評価する

[tom4649#65](https://github.com/tom4649/Coding/pull/65)

> `dict.get(key, default)` はデフォルト値を**常に評価**するため、`Node(...)` のような生成コストがある場合は `if key not in dict` で分岐するほうがよい

`original_to_copy.get(child, Node(val=child.val))` だとヒットしても毎回 `Node` を生成してしまい無駄（かつ捨てられるオブジェクトが出る）。`if child in ...` で分岐するのが正解。Python の引数評価タイミングに関わる落とし穴。

### ユーザー定義クラスのインスタンスは id ベースでハッシュされる

[tom4649#65](https://github.com/tom4649/Coding/pull/65)

> ユーザー定義のクラスのインスタンスであるようなオブジェクトはデフォルトでハッシュ可能です。それらは全て (自身を除いて) 比較結果は非等価であり、ハッシュ値は id() より得られます。

`{node: copy}` のように **Node オブジェクトそのものを辞書のキー**にできる理由。同じ val・neighbors でも別インスタンスなら別キーになる。kazuki/huyfififi の解法が `val` ではなく Node 参照をキーにしている（重複 val が無くても安全）根拠。

### `copy.deepcopy` でも解けるが内部で同じことをしている

[tom4649#65](https://github.com/tom4649/Coding/pull/65)

> deepcopyでも解けることに気が付く: sol4.py / 内部で同様のメモ化付き再帰トラバーサルを行っており、汎用性のための型チェック・pickle プロトコルのオーバーヘッドがある

`return copy.deepcopy(node)` の1行で AC する。CPython の `copy.py` を読み、atomic はそのまま返す・memo 辞書で循環参照を防ぐという、まさに今回手書きした構造そのものが実装されていることを確認している。面接では使えないが本質理解として良い。

### DFS再帰 / BFS反復 / スタックに1要素だけ積む版、の解法バリエーション

[kazuki-official#96](https://github.com/kazuki-official/leetcode/pull/96)

> Code2-2 (iterative) … neighbor_unresolved に積みながら、未訪問なら新規生成・訪問済みなら再利用

「スタックにはノードだけ積み、コピー生成と隣接接続をループ内で行う」形

## Step2

ループで解く。キューに入れるのは元のノードのみ

```py
class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if node is None:
            return None

        node_to_copy = {node: Node(node.val)}
        queue = deque()
        queue.append(node)
        while queue:
            original = queue.popleft()
            node_copy = node_to_copy[original]
            for neighbor in original.neighbors:
                if neighbor not in node_to_copy:
                    node_to_copy[neighbor] = Node(neighbor.val)
                    queue.append(neighbor)

                neighbor_copy = node_to_copy[neighbor]
                node_copy.neighbors.append(neighbor_copy)

        return node_to_copy[node]
```

### 過去に解いた類題（本リポジトリ）

- `number-of-islands/` — グリッド上の DFS/BFS 探索
- `max-area-of-island/` — 同上、訪問管理
- `course-schedule/` — 有向グラフの探索（サイクル検出）
- `binary-tree-level-order-traversal/` — BFS キューの基本
- `construct-binary-tree-from-preorder-and-inorder-traversal/` — 再帰での木の再構築
- `convert-sorted-array-to-binary-search-tree/` — 再帰での木の生成
