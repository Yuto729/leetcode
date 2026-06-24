# 110. Balanced Binary Tree

Given a binary tree, determine if it is height-balanced.

> A height-balanced binary tree is a binary tree in which the depth of the two subtrees of every node never differs by more than one.

Examples

Input: root = [3,9,20,null,null,15,7]
Output: true

Input: root = [1,2,2,3,3,null,null,4,4]
Output: false

Input: root = []
Output: true

Constraints:

- The number of nodes in the tree is in the range [0, 5000].
- -10^4 <= Node.val <= 10^4

## Step1

再帰が一番考えやすいので再帰で解く。再帰関数にsubtreeの根を渡したときに返ってきてほしい情報を考えると、subtreeが"balanced"かどうかとsubtreeの高さになりそう。
どちらかのsubtreeがbalancedじゃなければその時点で探索を打ち切ることができる。左右のsubtreeの高さの差が1より大きいときにFalseを返す。

時間計算量: O(N) N: ノード数
空間計算量: O(logN)

```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True

        def helper(root):
            if not root:
                return True, 0

            is_balanced_left, depth_left = helper(root.left)
            if not is_balanced_left:
                return False, depth_left

            is_balanced_right, depth_right = helper(root.right)
            if not is_balanced_right:
                return False, depth_right

            if abs(depth_left - depth_right) > 1:
                return False, max(1 + depth_left, 1 + depth_right)

            return True, max(1 + depth_left, 1 + depth_right)

        is_balanced, _ = helper(root)
        return is_balanced
```

iterative版を書こうとしたが、素直に変換できないので、AIにヒントをもらう

> 再帰版が自然に書けるのは、「子の高さが分かってから親を判定する」という順序が再帰で勝手に保証されるからです。
> iterativeにするとき、まずこれを自問してください：どの走査順なら「子を処理し終えてから親を処理する」が保証できるか？

> ヒント1: 走査順
>
> - 前順（pre-order）だと親を先に見てしまう
> - レベル順（BFS）だと高さの集約がやりにくい
> - 後順（post-order） なら、親を処理する時点で左右の子はすでに処理済み
>
> → スタックで post-order をどう実現するか、がメインの課題になります。
>
> ヒント2: 高さをどう持ち回るか
>
> 再帰では戻り値で高さが返ってきました。iterative では戻り値がないので、処理し終えたノードの高さをどこかに保存しておく必要があります。
>
> ノード → そのノードを根とする部分木の高さ、を引けるものは何か？
> （dict が素直です）
>
> ヒント3: 「処理済みか」の判定
>
> post-orderをスタックでやる典型的な詰まりどころは、あるノードをスタックから取り出したとき：
>
> - 「まだ子をスタックに積んでいない状態」なのか
> - 「子をすべて処理し終えて、いま自分を確定させる状態」なのか
>   を区別する必要がある点です。区別の仕方はいくつかあります：
>
> 1. visited フラグを一緒に積む（(node, False) → 再度 (node, True)）
> 2. 「子の高さが両方 dict に入っているか」を見て判定する
> 3. last_visited（直前に確定したノード）を覚えておく
>
> どれか一つを選んで組み立ててみてください。
>
> ヒント4: 打ち切り
>
> 再帰版では not is_balanced_left で早期 return していました。iterativeでは、ある親で abs(左高 - 右高) > 1 が見つかった瞬間に return Falseすればよいです（ループを抜ける）。

post-orderの走査順、つまり左右のsubtreeがすでに処理済みであるとき現在のノードを処理するようにすれば良い。逆に処理済みでないとき、左右のノードをスタックに積むだけで終わる
スタックに積んだとき、post-order順になっていれば良い

時間計算量: O(N) 各ノードは2回スタックに追加される
空間計算量: O(N) dict分

高さのデフォルトは-1じゃなくて良いのか？

```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True

        stack = [(root, False)]
        node_to_depth = {} # nodeを根とするsubtreeの深さを記録する
        while stack:
            node, is_children_processed = stack.pop()
            if not is_children_processed:
                stack.append((node, True))
                if node.left is not None:
                    stack.append((node.left, False))
                if node.right is not None:
                    stack.append((node.right, False))
                continue

            left_depth = node_to_depth.get(node.left, 0)
            right_depth = node_to_depth.get(node.right, 0)
            if abs(left_depth - right_depth) > 1:
                return False

            node_to_depth[node] = max(left_depth, right_depth) + 1

        return True
```

testしてみる

- root = [3,9,20,null,null,15,7]
  init s = [(3,false)], node_to_depth = {}
  // pop (3, false) -> s = [(3,true),(9,false),(20,false)], ..
  // pop (20, false) -> s = [(3,true),(9,false),(20,true),(15,false),(7,false)]
  // pop (7, false) -> s = [(3,true),(9,false),(20,true),(15,false),(7,true)]
  // pop (7, true) -> left_depth = 0, right.. = 0, node_to_depth ={7: 1}
  // pop (15, false) -> (15, true)をstackに追加  
  // pop (15, true) -> 同じように add (15, 1) to node_to_depth
  // pop (20, true) -> left_depth = 1, right_depth = 1, add (20, 2) to node_to_depth
  // pop (9, false) -> (9, true)のみ追加
  // pop (9, true) -> add (9, 1) to node_to_depth
  // pop (3, true) -> left_depth = 1, right_depth = 2 差が1なので問題なし
  return true

- root = [1,2,2,3,3,null,null,4,4]
  最後 root = 1がpopされた時に左右のsubtreeの高さの差が1より大きいのでfalseになる

AIにレビューしてもらう

> node_to_depthは処理済みノードを溜め続けますが、post-orderで確定した子の高さは親で使った後はもう不要です。

不要となったらdictのエントリを削除することで空間計算量をO(木の高さ)に削減できる
なぜか -> (node, True) -> 右 -> 左の順でpushするので、右部分木を処理し終えてから左部分木に入る。左を処理している間、dictに残っているのは「すでに確定した右の子」の高さで、これはスタック上の各祖先につき高々1つなので合計O(高さ)になる

```py
if node.left is not None:
    del node_to_depth[node.left]
if node.right is not None:
    del node_to_depth[node.right]
```

- そもそもdictなしでもできる
  - last_visitedの記録

```py
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        stack = []
        node = root
        last_visited = None
        node_to_depth = {}
        while stack or node:
            if node is not None:
                # 行けるだけ左に潜る
                stack.append(node)
                node = node.left
            else:
                peek = stack[-1]
                if peek.right is not None and last_visited is not peek.right:
                    # 左から戻ってきた。右がまだなら右へ
                    node = peek.right
                else:
                    # 左右とも済んだ。peek を確定する
                    left_dpth = node_to_depth.get(peek.left, 0)
                    right_depth = node_to_depth.get(peek.right, 0)
                    if abs(left_depth - right_depth) > 1:
                        return False

                    node_to_depth[peek] = max(left_depth, right_depth) + 1
                    last_visited = stack.pop()

        return True
```

あまりわかっていないので後でまた考える

## Step2

### 補助関数の設計：返り値に2つの意味を持たせる3つの選択肢

[huyfififi#11](https://github.com/huyfififi/coding-challenges/pull/11/files#r)

> だいたい選択肢は3つで
> isBalancedAuxiliary など補助関数で呼ぶことがまったく想定されていないような名前にする。
> pair<int, bool> get_height_and_is_balanced(TreeNode* root) のようにペアを返す。
> int get_height(TreeNode* root, bool\* is_balanced) という風にポインターにバランスしているかを書き込む。

Python は参照を取れないので、C++ のポインタ書き込み方式の代わりに「List を渡して書き込んでもらう」形になる、という話も出ていた。

### nonlocal を避けて、子から親へ報告する

[huyfififi#11](https://github.com/huyfififi/coding-challenges/pull/11)

> 木の全ノードに部下を立たせるんですよ。そうすると、nonlocal って、部下たちのいる部屋に共通の看板を立てておいて、全部下がその看板に書いたり消したりするんですよね。それだったら、部下同士のやり取り(関数呼び出し)の中で、自分より下の部分の情報も報告するようにしたほうがスマートじゃないでしょうか ... こっちの方がスレッド増やしたくなったときに並列性が良さそうです。

確かに再帰で `nonlocal` の共有変数に書き込むより、返り値で下からの情報を上に返すほうが並列化しやすく素直

### 高さの起点は 0 が正しい（が相対差だけなので動く）

[kitano-kazuki#78](https://github.com/kitano-kazuki/leetcode/pull/78)

> これは再帰の起点なので1始まりでも結果的に影響は出ないのですが、heightとしては0が正しいのではないでしょうか？（平衡の計算は相対的なずれだけなので、起点が常に1になっていても計算上のずれはなく、たとえば1を255とかにしても正しく動作します）

まさに自分が「default は -1 では？」と悩んだ点と。バランス判定は高さの相対差だけを見るので、起点を 0/1/255 のどれにしても正しく動く。ただし「height の定義」としては空=0 が標準。

### Go: 値渡し vs ポインタ渡しと GC

[rihib#30](https://github.com/rihib/leetcode/pull/30)

> 大きなサイズの構造体や、小さいサイズの構造体だがサイズが大きくなるものでない限り、単に数バイト節約するためにポインタを渡すのは良くない

参照渡しは複数スコープから参照されうるため値がヒープに置かれ、GC の追跡対象になって重くなるそう。小さなデータはスタックに乗る値渡しのほうが GC 不要で軽い。最近Goを使うので参考に

## Step3

ループで練習

```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True

        stack = [(root, False)] # (node, 子が処理済みかどうか)
        node_to_depth = {}
        while stack:
            node, is_children_processed = stack.pop()
            if not is_children_processed:
                stack.append((node, True))
                if node.left is not None:
                    stack.append((node.left, False))
                if node.right is not None:
                    stack.append((node.right, False))
                continue

            left_depth = node_to_depth.get(node.left, 0)
            right_depth = node_to_depth.get(node.right, 0)
            if abs(left_depth - right_depth) > 1:
                return False

            node_to_depth[node] = max(left_depth, right_depth) + 1
            if node.left in node_to_depth:
                del node_to_depth[node.left]
            if node.right in node_to_depth:
                del node_to_depth[node.right]

        return True

```

## 過去に解いた類題

- [Maximum Depth of Binary Tree](../maximum-depth-of-binary-tree/) — 高さ（深さ）を再帰/iterative で求める基礎
- [Minimum Depth of Binary Tree](../minimum-depth-of-binary-tree/) — 高さ系の派生。葉の扱いに注意
- [Path Sum](../path-sum/) — ルートから葉への再帰走査でボトムアップ/トップダウンを比較できる
- [Merge Two Binary Trees](../merge-two-binary-trees/) — 二分木の基本的な再帰走査
- [Binary Tree Level Order Traversal](../binary-tree-level-order-traversal/) — iterative 走査（BFS）の練習
- [Validate Binary Search Tree](../validate-binary-search-tree/) — 子の情報を使った再帰判定が同型
