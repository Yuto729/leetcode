# 235. Lowest Common Ancestor of a Binary Search Tree
Given a binary search tree (BST), find the lowest common ancestor (LCA) node of two given nodes in the BST.

According to the definition of LCA on Wikipedia: “The lowest common ancestor is defined between two nodes p and q as the lowest node in T that has both p and q as descendants (where we allow a node to be a descendant of itself).”

Ex.1
Input: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8
Output: 6
Explanation: The LCA of nodes 2 and 8 is 6.

Constraints:

- The number of nodes in the tree is in the range [2, 10^5].
- -10^9 <= Node.val <= 10^9
- All Node.val are unique.
- p != q
- p and q will exist in the BST.

## Step1

root = [6,2,8,0,4,7,9,null,null,3,5]で考える
p, q = 0, 7の時, 6が答えになるが、
例えばBFS的に走査していって、ノードの親を記録する。要素がユニークなのでハッシュマップを用いることができる。
{2:6, 8:6, 0:2, 4:2, 7:8, 9:8} 
0と7をみて、順にdictをひいて行って初めて共通する祖先が現れたらそれが答えになる。

以上のように考えたが、BSTの性質を使えば上記より良い方法がある。
p,q=0,7で考える。根を見ると0は6の左にあり、7は6の右にあるのでその時点で6が答えとわかる

p,q=2,4 -> どちらも6の左なので探索を続ける。2にヒットする. 2はノードの値以下で4はノードの値より大きいので2が答えとなる。
p,q=6,8の時 -> 6はroot以下で、8はrootより大きいので、6が答えになる

Time: O(N) BSTが均等に分かれていないケースの最悪
Space: O(1) スタックに追加されるのは1回のループで高々1つのノードで、毎回popされるのでスタックのサイズは最大で1

```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if not root:
            return None
        
        if p.val > q.val:
            p, q = q, p
        
        stack = [root]
        while stack:
            node = stack.pop()
            if p.val <= node.val <= q.val:
                return node

            if q.val < node.val and node.left is not None:
                stack.append(node.left)
            if node.val < p.val and node.right is not None:
                stack.append(node.right)

        # unreachable
        return None
```

test case
- root = [6,2,8,0,4,7,9,null,null,3,5], p = 0, q = 5
init: stack = [6]
loop
// node = 6, stack = [2]
// node = 2, return 2

- root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 6
init: stack = [6]
loop
// node = 6, return 6

- root = .. p = 2, p = 4

よく考えるとスタックを使っている必要がない
```py
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if not root:
            return None
        
        if p.val > q.val:
            p, q = q, p
        
        node_to_visit = root
        while node_to_visit is not None:
            if p.val <= node_to_visit.val <= q.val:
                return node_to_visit

            if q.val < node_to_visit.val:
                node_to_visit = node_to_visit.left
            if node_to_visit.val < p.val:
                node_to_visit = node_to_visit.right

        return None
```

> 潜在的バグが含まれてしまっている。1つ目のif文でnode_to_visitがNoneになってしまったら、2つ目のif文でAttribute Errorが発生しうる。2つ目はelifにするべき
今回は、必ずp, qがBSTに存在するという条件があるからエラーが起きていない

```py
if q.val < node_to_visit.val:
    node_to_visit = node_to_visit.left
if node_to_visit.val < p.val:
    node_to_visit = node_to_visit.right
```

再帰で書く
```py
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if not root:
            return None
        
        if p.val > q.val:
            p, q = q, p
        
        def traverse_node(node):
            if p.val <= node.val <= q.val:
                return node

            if q.val < node.val and node.left is not None:
                return traverse_node(node.left)
            
            if node.val < p.val and node.right is not None:
                return traverse_node(node.right)
            
            return None
        
        return traverse_node(root)
```

### フォローアップ
- ただの二分木だったら？
    - ただの二分木の場合、左の子が現在のノードより小さく、右の子が現在のノードより大きいという保証がない。DFSで探索をし、各ノードの親をハッシュマップで記録する。pは木の実際のノードなので、pからスタートして親を順に辿り、setに親ノードを順次追加していく。
    次にqを同じように親を辿り、初めて上記のsetに存在するノードが出てきたらその時のノードを返す。時間・空間ともにO(N)で解ける

    ```py
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        parent = {root: None}
        stack = [root]
        while stack:
            node = stack.pop()
            if node.left:
                parent[node.left] = node
                stack.append(node.left)
            if node.right:
                parent[node.right] = node
                stack.append(node.right)
        
        ancestors = set()
        node = p
        while node:
            ancestors.add(node)
            node = parent[node]
        
        node = q
        while node:
            if node in ancestors:
                return node
            node = parent[node]
    ```

    - 上記より簡単な方法: 左右のサブツリーを再帰で探索し、pかqに当たったらそのノードを返す。左右両方から返ってきたら今のノードがLCA。片方だけが返ってきたらそのままそれを返す。（pかqの一方がもう一方の祖先であるケース）。ボトムアップ再帰, post order
    - 参考: https://github.com/naoto-iwase/leetcode/pull/66/changes/BASE..a6dde1912d047faa3ede41b8a9c002345e97e910#r2571495973

    ```py
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode'):
        """
            Returns:
            - LCA if both p and q exist
            - p if only p exists
            - q if only q exists  
            - None if neither exists
        """

        if root is None:
            return None
        
        if root == p or root == q:
            return root
        
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left is not None and right is not None:
            # rootがLCA
            return root
        
        return left if left is not None else right
    ```
    上記の実装だと、再帰関数の戻り値の意味が2つ出てくることになる。以下のようにすると冗長だが意味を分けることができる
    ```py
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode'):
        lca = None
        def dfs(node):
            nonlocal lca
            if node is None:
                return False, False
            
            found_p_left, found_q_left = dfs(node.left)
            found_p_right, found_q_right = dfs(node.right)
            found_p = found_p_left or found_p_right or node == p
            found_q = found_q_left or found_q_right or node == q
            if found_p and found_q and lca == None:
                lca = node
            
            return found_p, found_q

        dfs(root)
        return lca
    ```

- ノードの値がユニークじゃないとき
    - 今回の解法だと難しい
    - 例  3
        / \
       2   3   ← p（val=3）
            \
                5  ← q（val=5） 

## Step2
### O(log N) は平衡な場合に限る

[kitano-kazuki#77](https://github.com/kitano-kazuki/leetcode/pull/77) -> https://github.com/kitano-kazuki/leetcode/pull/77#discussion_r2097890118

> 平衡ではない、ずっと子が片方にしかない木もBSTの条件は満たしうるので、O(log N)は平衡な場合に限ります。

時間計算量は O(h) であり、最悪ケースは O(N)。

### `sorted()` を使った書き方

[tom4649#110](https://github.com/tom4649/Coding/pull/110)

> `lower, upper = sorted([p.val, q.val])` の書き方の方が `p, q` 自体を交換するより分かりやすい

`p, q = q, p` のように引数自体を書き換えると関数内で p, q の意味が変わるため混乱しやすい。値だけ取り出す方がクリーン。

```python
lower, upper = sorted([p.val, q.val])
```

### 到達不能をどう表現するか

[ryosuketc#10](https://github.com/ryosuketc/leetcode_grind75/pull/10) -> https://github.com/ryosuketc/leetcode_grind75/pull/10#discussion_r2087315279
[tom4649#110](https://github.com/tom4649/Coding/pull/110)

制約上 p, q は必ず BST に存在するため、LCA は必ず見つかりループの末尾には到達しない。この到達不能なコードをどう扱うかについて複数の考え方がある。

- `return None`

制約が壊れても気づけない。p が BST に存在しないバグがあった場合、`None` が返って呼び出し元で別の場所に `AttributeError` が発生し、原因箇所とエラー箇所がずれてデバッグが難しくなる。

- `while True` にして dead code を消す

```python
node = root
while True:
    if p.val <= node.val <= q.val:
        return node
    elif q.val < node.val:
        node = node.left
    else:
        node = node.right
```

到達不能なコードをそもそも書かずに済む。
しかし制約が壊れたとき無限ループになり問題が隠蔽されてしまう可能性がある。またループが必ず終わることを読み手が自分で確認しないといけなさそう

- dead code を書かない

- `raise RuntimeError("unreachable")`

制約が壊れたとき即座に例外で発覚する。読み手になぜここに来ないかを推測させてしまうが、コメントで意図を補足すれば良いのか

```python
# p, q が BST に存在することが保証されているため到達しない
raise RuntimeError("unreachable")
```

### 
[kitano-kazuki#77](https://github.com/kitano-kazuki/leetcode/pull/77) -> https://github.com/kitano-kazuki/leetcode/pull/77#discussion_r2097890118

> アプローチを考えたときに BST という条件を使っているか？（ただの木で考えていないか？）というメタ的な検討はあって良いかもしれません。

## Step2
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode'):
        if p.val > q.val:
            p, q = q, p
        
        node_to_visit = root
        while node_to_visit is not None:
            if p.val <= node_to_visit.val <= q.val:
                return node_to_visit
            
            if q.val < node_to_visit.val:
                node_to_visit = node_to_visit.left
                continue

            if p.val > node_to_visit.val:
                node_to_visit = node_to_visit.right
        
        raise RuntimeError("unreachable")
```

## 類題

- [validate-binary-search-tree](../validate-binary-search-tree/)
- [convert-sorted-array-to-binary-search-tree](../convert-sorted-array-to-binary-search-tree/)
- [split-bst](../split-bst/)
