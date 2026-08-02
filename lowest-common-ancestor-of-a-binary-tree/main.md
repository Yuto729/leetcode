# lowest-common-ancestor-of-a-binary-tree

Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.

According to the definition of LCA on Wikipedia: “The lowest common ancestor is defined between two nodes p and q as the lowest node in T that has both p and q as descendants (where we allow a node to be a descendant of itself).”

Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
Output: 3
Explanation: The LCA of nodes 5 and 1 is 3.

## Step1

条件の確認

- 数字が重複しないか
- p, qは必ず二分木内に存在するノードか
- p != qで良いか

BSTの場合は簡単だったが、普通の二分木なので少しめんどくさい。再帰で解く

left, rightの部分木を対象にp, qを探してもらう。部下に返してもらうのは、(pがあるか, qがあるか, lca)

すでにlcaがある場合はそれを返す。ない場合でnodeがp, q自身の場合はqがどこにあるかをチェックし適切にreturnする
nodeがp, qではない場合でさらにp, qの場所が左部分木と右部分木でちょうど別れている場合、node自身がlcaとなる。上記の全てに当てはまらない場合は、p, qの存在を部分木について集約して上司に返す。

30分くらいかかってしまった

Time: O(N) N: ノード数
Space: O(H) H: 深さ

```py
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        def helper(node):
            """
                return p_exists, q_exists, lca
            """
            if node is None:
                return False, False, None

            p_exists_left, q_exists_left, lca_left = helper(node.left)
            p_exists_right, q_exists_right, lca_right = helper(node.right)
            if lca_left is not None:
                return True, True, lca_left

            if lca_right is not None:
                return True, True, lca_right

            if node is p:
                if q_exists_left or q_exists_right:
                    return True, True, p

                return True, False, None

            if node is q:
                if p_exists_left or p_exists_right:
                    return True, True, q

                return False, True, None

            if (p_exists_left and q_exists_right) or (q_exists_left and p_exists_right):
                return True, True, node

            return (p_exists_left or p_exists_right), (q_exists_left or q_exists_right), None

        _, _, lca = helper(root)
        return lca
```

### AI Review

1. 状態管理が複雑すぎる
   (p_exists, q_exists, lca) という3値タプルを引き回す必要は実はありません。以下のように「見つかったノード（またはNone）」だけを返す設計にすると、同じロジックが半分以下の行数で書けます。

```py
class Solution:
    def lowestCommonAncestor(self, root, p, q):
        if root is None or root is p or root is q:
            return root

        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left and right:
            return root

        return left or right
```

ポイントは「rootがpまたはqと一致したら、それ以上左右を探さずその場で返してよい」という点です。これは「pの子孫にqがいるかもしれないが、いたとしてもLCAはp自身になる」という性質（"a node is a descendant of itself"という問題文の定義）を使っています。あなたのコードはnode is pのケースでq_exists_left or q_exists_rightをわざわざ確認していますが、実は確認しなくてもpを返してしまってよく、その後上位の再帰で自然に正しいLCAに収束します。ここが設計を複雑にしていた主因だと思います。

2. ヘルパー関数名・docstring
   helperは中身が予測できないので find や dfs の方が意図が伝わります。docstringも「戻り値の意味」だけでなく、pythonなら型ヒント (-> tuple[bool, bool, Optional[TreeNode]]) で表現する手もあります。

### Follow Up

1. p, qが木の中に必ず存在するとは限らない場合、シンプル版のコード（および今回のあなたのコード）はどう振る舞いますか？正しくNoneや不正な結果を返せますか？対処するには設計をどう変えますか？
2. 各ノードに 親へのポインタ (parent) が生えている場合、この問題はどう解き方が変わりますか？（LeetCode 1650 相当）
3. p, qの2つではなく、N個のノードのLCAを求めたい場合、どうアプローチしますか？
4. 再帰ではなく反復(iterative)で書くとしたら、どういうデータ構造が必要になりますか？
5. 非常に偏った木（実質リスト状）の場合、Space O(H) は最悪どうなりますか？大きな入力でこれが問題になるケースは？

1について 自分のコードはうまくいく。qが存在しないとすると、`q_exists`と`node is q`の分岐が実行されずNoneしか返らない。Noneを返した時にエラーでも良い。
しかし、シンプル版のコードは、pかqかのどちらかにマッチした時点でそのノードを返す設計になっているのでうまく行かない。確認していない方が本当に存在するのか確認する必要がある。2回走査するか自分の解法のように情報を明示的に運ぶ設計にする

4については以下のように考えることができる

1. p, qそれぞれに至るまでの親ポインタを作成する
2. 親ポインターのリストをpからrootまで辿った記録をsetとして作成する
3. qから親を辿って初めて上記のsetの中にある要素がLCAとなる

Time: O(N) 最悪
Space: O(N) 最悪

```py
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        stack = [root]
        parent = {root: None}
        node = root
        while p not in parent or q not in parent:
            node = stack.pop()
            if node.left is not None:
                parent[node.left] = node
                stack.append(node.left)
            if node.right is not None:
                parent[node.right] = node
                stack.append(node.right)

        ancestors = set()
        node = p
        while node is not None:
            ancestors.add(node)
            node = parent[node]

        node = q
        while node not in ancestors:
            node = parent[node]

        return node
```

## Step3

```py
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if root is None or root is p or root is q:
            return root

        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left and right:
            return root

        return left if left else right
```
