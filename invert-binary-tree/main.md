# Invert Binary Tree
Given the root of a binary tree, invert the tree, and return its root.

Ex1
Input: root = [4,2,7,1,3,6,9]
Output: [4,7,2,9,6,3,1]

Ex2.
Input: root = [2,1,3]
Output: [2,3,1]

Ex3.
Input: root = []
Output: []

Constraints:
- The number of nodes in the tree is in the range [0, 100].
- -100 <= Node.val <= 100

## Step1
二分木を逆順にする問題。順番に書いてみるとわかるが、各ノードについてleft, rightを入れ替えれば良さそう。幅優先探索で走査しながら行う
8分

Time: O(N)
Space: O(N) -> 完全二分木で、最下層にN/2個のノードが入る
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        queue = deque()
        queue.append(root)
        while queue:
            node = queue.popleft()
            if node is None:
                continue
            
            current_left = node.left
            current_right = node.right
            node.left = current_right
            node.right = current_left
            queue.append(node.left)
            queue.append(node.right)
        
        return root
```

入力を破壊しないバージョン

Space: O(N)
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None

        head = TreeNode(root.val)
        queue = deque()
        queue.append((root, head))
        while queue:
            base, node = queue.popleft()
            if base is None:
                continue
            
            node.left = TreeNode(base.right.val) if base.right is not None else None
            node.right = TreeNode(base.left.val) if base.left is not None else None
            queue.append((base.right, node.left))
            queue.append((base.left, node.right))
        
        return head
```

🤖 AIレビュー
>
```py
current_left = node.left
current_right = node.right
node.left = current_right
node.right = current_left
```
Pythonicに書くなら一行で済む。可読性も上がる。
```py
node.left, node.right = node.right, node.left
```

>`node.left` / `node.right` が None でも queue に入れて、popleft 後に `continue` で弾いている。動作上は問題ないが、入れる前にチェックすればqueue操作が減る。
```py
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None
            
        queue = deque()
        queue.append(root)
        while queue:
            node = queue.popleft()
            node.left, node.right = node.right, node.left
            # 事前チェック
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        
        return root
```

> この問題はDFS（再帰）で書くと3〜4行で済むのが定番。BFS解と並べて比較しておくと「なぜBFSを選んだか」が説明できる。
```py
def invertTree(self, root):
    if not root:
        return None

    root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
    return root
```
- Time O(N), Space O(H)（H は木の高さ。平衡木で O(log N)、最悪 O(N)）
- BFS版より空間効率が良いケースが多い（平衡木のとき）

> 非破壊版は再帰の方が読みやすい
```py
def invertTree(self, root):                            
    if not root:                                 
        return None                                    

    new_left = self.invertTree(root.right)             
    new_right = self.invertTree(root.left)             
    return TreeNode(root.val, new_left, new_right)
```

## Step2

### BFSでqueueに入れる前にNoneチェックすべきか

[huyfififi#6](https://github.com/huyfififi/coding-challenges/pull/6)

> 大体の場合、出てきてからチェックでもいいのですが、まれに BFS で(2度入力しているかのチェックを出てきてからすると)急激に遅くなることがあります。

Number of Islandsのようなグラフ問題で、訪問済みフラグを「pop後」に立てると、同じ座標を複数回queueに入れてしまい、最悪パスカルの三角形状に膨らむことがあるそう

### iterative DFSではcall stackをstackで模す

[huyfififi#6](https://github.com/huyfififi/coding-challenges/pull/6)

> recursive (DFS) な解法はfunction callがcall stackに積まれていくので、iterativeにDFSを実装するとcall stackを模してstackを使用することになる。(BFSならFIFOのqueue。)

### stack overflowはstackが溢れることではない

[huyfififi#6](https://github.com/huyfififi/coding-challenges/pull/6)

> stack overflowとは再帰関数の呼び出しによりcall stackが溢れる状態を指し、単にstackが最大の要素数を超える場合を指すわけではない

iterativeにすると「stack overflowを避けられる」と言われるが、正確にはOSが割り当てたcall stack領域を超えることを指す。ユーザー定義のstack（list/deque）はヒープに置かれるので、メモリが許す限り伸ばせる。

## Step3
再帰で書く。
「自分の左部分木と右部分木を渡して、それぞれをinvertしてもらい、返ってきた根をleft, rightにセットする」

```py
class Solution:
    def invertTree(self, root):
        if not root:
            return None
        
        return TreeNode(root.val, self.invertTree(root.right), self.invertTree(root.left))
```
## 過去に解いた類題

- [merge-two-binary-trees]
- [maximum-depth-of-binary-tree]
- [binary-tree-level-order-traversal]