---
tags:
  - leetcode
date: 2026-08-08
url: https://leetcode.com/problems/binary-tree-right-side-view/
---

# 199. Binary Tree Right Side View

Given the `root` of a binary tree, imagine yourself standing on the **right side** of it, return *the values of the nodes you can see ordered from top to bottom*.

**Input:** root = [1,2,3,null,5,null,4]
**Output:** [1,3,4]

## Step1

```
   1 x
2    3 x
  5   4 x
```

各レベルの一番右の値が右から見たものになる

- rootがNoneのときwhileループが飛ばされるので期待通り[]がかえると勘違いしていたが、実際にはNoneが`current_level_nodes`に入るので間違いだった

time: O(n)
space: O(w) w: 最大幅 最悪 n/2よりO(n)

```py
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        result = []
        current_level_nodes = [root]
        while current_level_nodes:
            next_level_nodes = []
            result.append(current_level_nodes[-1].val)
            for node in current_level_nodes:
                if node.left is not None:
                    next_level_nodes.append(node.left)
                if node.right is not None:
                    next_level_nodes.append(node.right)
            current_level_nodes = next_level_nodes

        return result
```

### 実装2 DFS

root -> right -> leftの順に走査していく。
各レベルの一番右 -> depth nの中で一番最初に辿り着くノードのこと・
stackにdepthと一緒に情報を入れておき、答えを格納する側もノードとともにdepthを把握しておく。current nodeのdepthと同じdepthのノードが答えに含まれていなければ加える。depthからnodeをhashmapなどでO(1)で引けるようにする
上記のような感じで考えたが、答え配列に含まれるノードは各depthで一つだけであり、depthに対して昇順になるように格納されるはずなので、(答え配列に含まれるノードの最大のdepth + 1)が次に求めるdepthである。最初にこのdepthに一致したnodeを答えに加える。

time: O(n)
space: O(h) h: 高さ

空間計算量がO(h)になるので、幅の広い木ではBFSより有利になる
ex. 完全二分木であれば w ~= n/2, h ~= lognなのでDFSが有利

```py
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        stack = [(root, 0)]
        result = []
        max_depth = -1
        while stack:
            node, depth = stack.pop()
            if depth == max_depth + 1:
                result.append(node.val)
                max_depth = depth
            if node.left is not None:
                stack.append((node.left, depth + 1))
            if node.right is not None:
                stack.append((node.right, depth + 1))

        return result
```

### 実装3

`if depth == max_depth + 1:`は`depth == len(result)`で置き換えることができる

```py
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        result = []
        stack = [(root, 0)]
        while stack:
            node, depth = stack.pop()
            if depth == len(result):
                result.append(node.val)
            if node.left is not None:
                stack.append((node.left, depth + 1))
            if node.right is not None:
                stack.append((node.right, depth + 1))

        return result
```

root -> left -> rightの走査順にしてもかける。この場合は後から同じ深さのノードがきた場合は上書きをする

```py
def visit(node, depth):
    if node is None:
        return

    if depth == len(result):
        result.append(node.val)
    else:
        result[depth] = node.val   # 後から来た＝より右
    visit(node.left, depth + 1)
    visit(node.right, depth + 1)
```

## Step3

```py
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        result = []
        current_level_nodes = [root]
        while current_level_nodes:
            next_level_nodes = []
            result.append(current_level_nodes[-1].val)
            for node in current_level_nodes:
                if node.left is not None:
                    next_level_nodes.append(node.left)
                if node.right is not None:
                    next_level_nodes.append(node.right)
            current_level_nodes = next_level_nodes

        return result
```
