# Diameter of Binary Tree

Given the root of a binary tree, return the length of the diameter of the tree.

The diameter of a binary tree is the length of the longest path between any two nodes in a tree. This path may or may not pass through the root.

The length of a path between two nodes is represented by the number of edges between them.

Ex.

```
    1
   /  \
  2    3
 / \
4   5
```

diameter=3となる。4->2->1->3が該当のパス

## Step1

二分木の直径を求める問題
直径とは: 2つのnode間のエッジの数の最大値

こんな感じの片方に偏った変な二分木のdiameterは7となる。(1->8)

```
       1
      3
     4
    2
  3  4
 5    6
       7
        8
```

再帰で解く方がなんとなく良さそう。
その場合、サブツリーの最大の深さと直径を返してもらうとそれを用いて計算ができそう

ここまで来て思いつかず時間が経ってしまったので。
AIにヒントをもらい、普通に最大の直径をいきなり求めるというより再帰関数の中で更新していけば良いことに気づく

- 「それぞれの頂点を通る最長のパスの長さ」が直径候補となる
- 上記は、ある頂点の部分木の高さの和となる

上記直径候補の最大値を求めれば良い

- 再帰関数で、左右の部分木の高さを求めつつ、直径を更新する

### 細かい点

- ノードがNoneのときだけでなく、葉ノードのときもベースケースに入れないと高さが1ズレる
- 直径を更新するとき、子ノードと現在のノードをつなぐエッジの数も足さないといけないが、左右の子が存在するかで足すべき値が変わる

```py
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        diameter = 0
        def calculate_height(node):
            nonlocal diameter
            if node is None:
                return 0

            if node.left is None and node.right is None:
                return 0

            left_height = calculate_height(node.left)
            right_height = calculate_height(node.right)
            num_of_children = int(bool(node.left)) + int(bool(node.right))
            diameter = max(diameter, left_height + right_height + num_of_children)
            return max(left_height, right_height) + 1

        calculate_height(root)
        return diameter
```

`int(bool(node.left)) + int(bool(node.right))`の部分が強引に感じる...

### AI Review

> 葉の特別扱いをなくす別解: 業界でよくあるテクニックとして、Noneのとき-1を返す(「存在しない子の高さ」を-1とする)convention にすると、葉の特別扱いが不要になり、left_height + right_height + 2で統一的に書けます。

確かに、これですっきりする。ベースケースのときの「高さ」をどうするかをもうちょっと丁寧に考えるべきだった
ついでに、葉ノードのベースケースもいらなくなる。葉ノードのとき、最後のreturnで-1 + 1 = 0を返す

```py
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        diameter = 0
        def calculate_height(node):
            nonlocal diameter
            if node is None:
                return -1

            left_height = calculate_height(node.left)
            right_height = calculate_height(node.right)
            diameter = max(diameter, left_height + right_height + 2)
            return max(left_height, right_height) + 1

        calculate_height(root)
        return diameter
```

**[Maximum Depth of Binary Tree](../maximum-depth-of-binary-tree)
ではnodeが`None`のケースをdepth 0としているが、この問題は「ノード数」を基準に計算しているためベースは0で良い
今回の問題は、「エッジ数」を基準に計算するのでベースケースで-1を返すようにすると辻褄が合う**

葉で0を返したいので、逆算してNoneのときの値を決める

### フォローアップ

- iterativeで書いてみる
  - post-orderで子の結果が出揃ってから親を処理する必要がある

```py
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        is_children_processed = False
        stack = [(root, is_children_processed)]
        node_to_height = {}
        diameter = 0
        while stack:
            node, is_children_processed = stack.pop()
            if is_children_processed:
                left_height = node_to_height.get(node.left, -1)
                right_height = node_to_height.get(node.right, -1)
                node_to_height[node] = max(left_height, right_height) + 1
                diameter = max(diameter, left_height + right_height + 2)
                continue

            stack.append((node, True))
            if node.right is not None:
                stack.append((node.right, False))
            if node.left is not None:
                stack.append((node.left, False))

        return diameter
```

- N分木への拡張。子の数が可変のN -arytreeだったらどうなるか (premiumにあるらしい)

```py
first_max, second_max = -1, -1
for child in node.children:
    height = calculate_height(child)
    if height > first_max:
        first_max, second_max = height, first_max
    elif height > second_max:
        second_max = height

# サブツリーのうち、高さが大きい2つを用いて計算する
diameter = max(diameter, first_max + second_max + 2)
return first_max + 1
```

- 経路の復元:直径の「長さ」だけでなく、実際にその最長パスを構成する頂点の列を返す
  - 経路を求める処理を直径を求める処理と同時にやらない
  - まず、高さだけを計算しながらdiameterを更新する。このとき「直径を更新された瞬間のノード」を覚えておく (仮に`center`とする)
  - `center.left`からはじめて`left_height`と`right_height`のうち高い方の子を辿って葉まで降りていく。centerを挟んでrightも同じように
  - O(H)で経路を復元できる
  - `left_height`と`right_height`は辞書に予め保存しておく

## Step2

- https://github.com/kazuki-official/leetcode/pull/89
  - Code2-1 (recursion)
    - 自分が最初に思いついたやつの完成形っぽい
    - ボトムアップで直径を更新して再帰の返り値として伝搬していく
    - 直径とともに高さを返す
    - ベースを0にしてる

    (参考)

    ```py
    class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        def diameter_helper(root: TreeNode | None) -> tuple[int, int]:
            if root is None:
                return 0, 0

            left_height, left_diameter = diameter_helper(root.left)
            right_height, right_diameter = diameter_helper(root.right)

            height = max(left_height, right_height) + 1
            diameter = max(
                left_diameter,
                right_diameter,
                left_height + right_height
                )

            return height, diameter

        return diameter_helper(root)[1]
    ```

- https://github.com/huyfififi/coding-challenges/pull/21
- https://github.com/naoto-iwase/leetcode/pull/71
  - 再帰のベースケースの高さを0にしてる人が多い
  - ノード数ベースで数えている
  - 問題文の通りに素直に数えるとエッジ数で数えることになるが、ノード数で数えた方がわかりやすい

## Step3

```py
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        diameter = 0
        def calculate_height(node):
            nonlocal diameter
            if node is None:
                return -1

            left_height = calculate_height(node.left)
            right_height = calculate_height(node.right)
            diameter = max(diameter, left_height + right_height + 2)
            return max(left_height, right_height) + 1

        calculate_height(root)
        return diameter
```
