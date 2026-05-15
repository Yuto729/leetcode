# Invert Binary Tree

## Step1
二分木を逆順にする問題。順番に書いてみるとわかるが、各ノードについてleft, rightを入れ替えれば良さそう。幅優先探索で走査しながら行う
8分

Time: O(N)
Space: O(N/2)
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