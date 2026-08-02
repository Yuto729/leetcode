# serialize-and-deserialize-binary-tree

Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.

Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.

Clarification: The input/output format is the same as how LeetCode serializes a binary tree. You do not necessarily need to follow this format, so please be creative and come up with different approaches yourself.

Ex.
Input: root = [1,2,3,null,null,4,5]
Output: [1,2,3,null,null,4,5]

## Step1

Serializeのフォーマットとして、"1,2,3,null,null,4,5"というような文字列を考える。これはpreorderで二分木を走査した結果をそのまま文字列にしたものである。Serialize関数は、DFSを用いてPreorderで走査した配列を作り、最後に`,` で結合する。

Deserializeについては、iterativeに最初解こうとして難しかったので再帰を考えたが、なかなか思い付かず答えをみる。

- preorderは「親->左部分木->右部分木」の順で値を並べたものなので、配列の先頭から順に読んでいけば次に読むべき値が一意に定まる。再帰関数は、「次に読むべき位置」を参照し、そのノードを根とする部分木を構築し、根を返す仕様。

あとはどのようにして「エンコード文字列の中で次に読むべき場所」を共有しながら木を構築するかを考える必要がある

いくつか方法がある

- iteratorを用いる。文字列を配列としてイテレーターを作成し、木のノードを1つ作成するごとに一つ進める。
- 再帰関数の戻り値に次見るべきインデックスを返す
- `nonlocal`でグローバルなインデックスにする

### iteratorバージョン

```py
class Codec:

    def serialize(self, root):
        """Encodes a tree to a single string.

        :type root: TreeNode
        :rtype: str
        """
        if not root:
            return ""

        stack = [root]
        encoded = []
        while stack:
            node = stack.pop()
            if node is None:
                encoded.append("null")
                continue

            encoded.append(str(node.val))
            stack.append(node.right)
            stack.append(node.left)

        return ','.join(encoded)

    def deserialize(self, data):
        """Decodes your encoded data to tree.

        :type data: str
        :rtype: TreeNode
        """
        if not data:
            return None

        token_iter = iter(data.split(','))
        def build_tree():
            value = next(token_iter)
            if value == "null":
                return None

            node = TreeNode(int(value))
            node.left = build_tree()
            node.right = build_tree()
            return node

        return build_tree()
```

### 返り値に含めるバージョン

```py
def deserialize(self, data):
        """Decodes your encoded data to tree.

        :type data: str
        :rtype: TreeNode
        """
        if not data:
            return None

        parsed = data.split(',')
        def build_tree(i):
            value = parsed[i]
            if value == "null":
                return None, i + 1

            node = TreeNode(value)
            node.left, i = build_tree(i + 1)
            node.right, i = build_tree(i)
            return node, i

        root, _ = build_tree(0)
        return root
```

### レベル別オーダーのやり方

LeetCode公式では、レベル別オーダーで二分木が表現されている。https://support.leetcode.com/hc/en-us/articles/32442719377939-How-to-create-test-cases-on-LeetCode#h_01J5EGREAW3NAEJ14XC07GRW1A

```py
class Codec:

    def serialize(self, root):
        """Encodes a tree to a single string.

        :type root: TreeNode
        :rtype: str
        """
        if not root:
            return ""

        encoded = []
        current_level_nodes = [root]
        while current_level_nodes:
            next_level_nodes = []
            for node in current_level_nodes:
                if node is None:
                    encoded.append("null")
                    continue

                encoded.append(str(node.val))
                next_level_nodes.append(node.left)
                next_level_nodes.append(node.right)

            current_level_nodes = next_level_nodes

        return ",".join(encoded)

    def deserialize(self, data):
        """Decodes your encoded data to tree.

        :type data: str
        :rtype: TreeNode
        """
        if not data:
            return None

        parsed = data.split(",")
        token_iter = iter(parsed)
        root = TreeNode(int(next(token_iter)))
        current_level_nodes = [root]
        while current_level_nodes:
            next_level_nodes = []
            for node in current_level_nodes:
                left_token = next(token_iter)
                right_token = next(token_iter)
                left_node = TreeNode(int(left_token)) if left_token != "null" else None
                right_node = TreeNode(int(right_token)) if right_token != "null" else None
                node.left = left_node
                node.right = right_node
                if left_node is not None:
                    next_level_nodes.append(left_node)
                if right_node is not None:
                    next_level_nodes.append(right_node)
            current_level_nodes = next_level_nodes

        return root
```

test case

- root = [1,2,3,null,null,4,5]
- 単一ノード: [1]
- 空の木
- 左に偏った木 [1,2,null,3,null]

ai review

- 末尾の冗長なnullが気になる。例: 1,2,null,3,null,null,null
  これの対応方法は、

serialize側で、以下のように現在のレベルの実ノードにNoneでないノードが１つもなければ処理をせずループを打ち切る処理を入れる

```py
while current_level_nodes:
    if all(node is None for node in current_level_nodes):
        break
    ...
```

deserialize側も対応が必要。そのままだと木の末尾でトークンが尽きた時に`next`が`StopIteration`を起こす。以下のようにデフォルト値を渡すことで解決する

```py
left_token = next(token_iter, "null")
```

## Step2

- https://github.com/tom4649/Coding/pull/125
  - dfsを用いたpost order (left -> right -> root)
  - [1,2,3,null,null,4,5]であれば[null,null,2,null,null,4,null,null,5,3,1]のようにシリアライズされる。
  - デシリアライズの際はtokenを末尾からpopしていき、node.rightを先に再帰的に処理すると元の木を構築できる。

  ```py
  def deserialize(self, data: str) -> TreeNode | None:
        """Decodes your encoded data to tree."""
        if not data or data == self.NO_NODE:
            return None

        tokens = data.split(self.DELIM)

        def traverse() -> TreeNode | None:
            if not tokens:
                return None

            token = tokens.pop()
            if token == self.NO_NODE:
                return None

            node = TreeNode(token)
            node.right = traverse()
            node.left = traverse()

            return node

        return traverse()
  ```

## Step3

DFSベースの方法で実装

```py
class Codec:

    def serialize(self, root):
        """Encodes a tree to a single string.

        :type root: TreeNode
        :rtype: str
        """
        if not root:
            return ""

        encoded = []
        def traverse(node):
            if node is None:
                encoded.append("null")
                return

            encoded.append(str(node.val))
            traverse(node.left)
            traverse(node.right)

        traverse(root)
        return ",".join(encoded)


    def deserialize(self, data):
        """Decodes your encoded data to tree.

        :type data: str
        :rtype: TreeNode
        """
        if not data:
            return None

        token_iter = iter(data.split(","))
        def build_tree():
            token = next(token_iter)
            if token == "null":
                return None

            node = TreeNode(int(token))
            node.left = build_tree()
            node.right = build_tree()
            return node

        root = build_tree()
        return root
```
