21. Merge Two Sorted Lists

You are given the heads of two sorted linked lists list1 and list2.
Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.

Return the head of the merged linked list.

Example 1:
Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]

Example 2:
Input: list1 = [], list2 = []
Output: []

Example 3:
Input: list1 = [], list2 = [0]
Output: [0]

Constraints:
- The number of nodes in both lists is in the range [0, 50].
- -100 <= Node.val <= 100
- Both list1 and list2 are sorted in non-decreasing order.

## Step1
例を増やしてみる
Example:
Input: list1 = [1,2,4], list2 = [1,1,4]
Output: [1,1,1,2,4,4]

Example:
Input: list1 = [-4,-2,-1], list2 = [-1,3,4]
Output: [-4,-2,-1,-1,3,4]

単純にTwo PointerのLinkedList版をやれば良さそう。

Time: O(m + n)
Space: O(1)

失敗パターン: `node.next.next = None` を `left_node = left_node.next` より先に書く
以下は誤り。
```py
while left_node is not None or right_node is not None:
    if right_node is None or (left_node is not None and left_node.val <= right_node.val):
        node.next = left_node
        node.next.next = None        # ← ここで X.next を None にしてしまう
        left_node = left_node.next   # ← この時点で left_node.next は None
    else:
        node.next = right_node
        node.next.next = None
        right_node = right_node.next
    node = node.next
```

list1 = X → Y → Z のとき:
- `node.next = left_node` で `node.next` と `left_node` が同じノード X を指す（エイリアス）
- `node.next.next = None` は `X.next = None` の意味。この時点で `left_node` はまだ X を指している
- `left_node = left_node.next` で `X.next`（たった今 None にした）を読む → `left_node` が None になり、Y 以降が辿れなくなる

直し方: 順序を逆にして、変数を先に張り替えてから next を切る。
```py
node.next = left_node
left_node = left_node.next   # 先に left_node を Y に張り替える
node.next.next = None        # その後で X.next を切る（left_node はもう X を指していないので安全）
```

`left_node = left_node.next` は「変数 left_node の指し先を張り替える」だけで、ノード X のフィールドには触らない。張り替えた後なら X.next を None にしても left_node には影響しないからok

```py
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        head = dummy
        node = head
        left_node = list1
        right_node = list2
        while left_node is not None or right_node is not None:
            if left_node is None:
                node.next = right_node
                break
            
            if right_node is None:
                node.next = left_node
                break
                
            if left_node.val <= right_node.val:
                node.next = left_node
                left_node = left_node.next
            else:
                node.next = right_node
                right_node = right_node.next

            node.next.next = None
            node = node.next
        
        return dummy.next
```

🤖レビュー
> コードレビューします。
良い点
- `dummy` ノードを使った定石パターン
- 両リスト終了条件を while で表現できている
気になる点
1. `node.next.next = None` は不要かつ危険
   - 73行目で毎回 next を切っていますが、最終的に片方が残ったら 59/63行目で `node.next = right_node`（または left_node）と「残り全部」を繋いでいます。つまり途中ノードの next を切る意味はなく、むしろ「途中で書いた next を後で上書きする」前提のロジックになっていて読みにくい。
   - splicing（既存ノードを繋ぎ替えるだけ）なら、選んだノードの next を意図的に触らずに、`node = node.next` するだけで十分です。
2. while 条件と分岐の冗長性
   - `while l or r` の中で「片方 None」を毎ループ判定するより、`while l and r` で両方ある間だけ比較 → ループ後に残った方を `node.next` に繋ぐ、の方が素直で短いです。
3. 変数名
   - `head = dummy` と `node = head` の2行は実質同義で、`node = dummy` 1行で十分。`head` 変数は使われていません。

直す
```py
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        node = dummy
        left_node = list1
        right_node = list2
        while left_node is not None and right_node is not None:
            if left_node.val <= right_node.val:
                node.next = left_node
                left_node = left_node.next
            else:
                node.next = right_node
                right_node = right_node.next

            node = node.next
        
        node.next = left_node if left_node is not None else right_node
        return dummy.next
```


残りをメインループ外で処理する部分をメインループ内で行うようにしてみた
条件が複雑で可読性が落ちる
```py
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        node = dummy
        left_node = list1
        right_node = list2
        while left_node is not None or right_node is not None:
            if right_node is None or (left_node is not None and left_node.val <= right_node.val):
                node.next = left_node
                left_node = left_node.next
            else:
                node.next = right_node
                right_node = right_node.next

            node = node.next
        
        return dummy.next
```

## Step2

### 過去解いた類題
- [Intersection of Two Arrays](https://github.com/Yuto729/leetcode/pull/18/)

### `node.next = list1 or list2` の罠
[naoto-iwase#62](https://github.com/naoto-iwase/leetcode/pull/62)
> 私は、ごく個人的に、値を`or`で繋ぐことに少し怖さを感じるんですよね。今回の問題設定では大丈夫なのですが、もし`ListNode`が`__bool__`を定義していたら（または将来的に定義されたら）予期せぬ挙動をする可能性があるからです。

Pythonの `or` は「左辺が truthy なら左辺、それ以外は右辺」という意味で、`is None` ではない`ListNode` が将来 `__bool__` を定義したら、None でないノードが falsy 判定されて右辺が返る事故が起きうるので明示的に `node.next = left_node if left_node is not None else right_node` と書くのが安全

### 変数名: `curr` より `tail` / `merged_tail`
[huyfififi#3](https://github.com/huyfififi/coding-challenges/pull/3)
> 私の言語感覚では、これは「マージ済みの最後尾」なんですがいかがですか。例えば、merged_tail あたりです。

ループ中で動かしているポインタは「次に書き込むノード」ではなく「マージ済み列の末尾」なので`node` や `curr` より `tail` の方が良さそう

### 非破壊版（dummyを使わずListNodeを新規生成）
[huyfififi#3](https://github.com/huyfififi/coding-challenges/pull/3)
> こういう問題を見ると私は非破壊的なバージョンが気になるのですが、これの非破壊的なバージョンはかけますか？

以下が非破壊バージョン。空間計算量がO(m+n)になる
```py
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        merged_tail = dummy
        left_node = list1
        right_node = list2
        while left_node is not None and right_node is not None:
            if left_node.val <= right_node.val:
                merged_tail.next = ListNode(left_node.val)
                left_node = left_node.next
            else:
                merged_tail.next = ListNode(right_node.val)
                right_node = right_node.next

            merged_tail = merged_tail.next
        
        rest = left_node if left_node is not None else right_node
        while rest is not None:
            merged_tail.next = ListNode(rest.val)
            rest = rest.next
            merged_tail = merged_tail.next
            
        return dummy.next
```

### 番兵で1ループ化（None を `inf` 扱い）
[huyfififi#3](https://github.com/huyfififi/coding-challenges/pull/3)
> 空のListNodeが与えられた時に、大きい値を返す関数を作れば、1回のwhileループで処理することはできるかなと思いました

```py
def node_to_val(node):
    return float("inf") if node is None else node.val

while list1 is not None or list2 is not None:
    if node_to_val(list1) < node_to_val(list2):
        ...
```
ループ後の「残りを連結」処理が消える面白い発想
`float("inf")` 比較や `inf` を超える値が来ると破綻するため、制約をよく見て使うのが良さそう

### 共通化のしすぎは可読性を損なう
[huyfififi#3](https://github.com/huyfififi/coding-challenges/pull/3)
> これ、list1 の先頭を取って、curr の最後尾に追加するというコードなわけですよね。追加するを構成する2文を離して書いて別の分岐と共通化していることに相当します。

`tail = tail.next` をループ末尾に1回だけ書く形にすると、「ノードを採用する → tailを進める」という一連の論理ステップが2つの分岐に分断される。冗長でも `if` 内に2回書いた方が読みやすいことがある。

### ポインタと参照の違い
[ryosuketc#3](https://github.com/ryosuketc/leetcode_grind75/pull/3)
> ポインタはアドレスという値を保持する型で、値を保持するという意味では `int` なんかと同じなんですね。... 一方参照は「変数への別名」で、エイリアスなんですね。

Python の `b = a` はポインタ的（同じオブジェクトを指すが `b = None` しても `a` は残る）。C++ の参照は別名なので「参照を nullptr にする」とは振る舞いが本質的に違う。

| | ポインタ (C++) | 参照 (C++) | Python の変数 |
|---|---|---|---|
| 正体 | アドレスという**値**を保持する型 | 既存変数の**別名 (エイリアス)** | オブジェクトに貼る**ラベル** |
| 再代入 | `p = &b` で別物を指せる | 不可（束縛先固定） | `b = ...` で別物を指せる |
| nullable | `nullptr` を持てる | 不可 | `None` を持てる |
| 性質 | — | — | **ポインタに近い** |

C++ の挙動:
```cpp
int a = 5;
int* p = &a;   p = nullptr;   // a は影響なし。p は別の値を持てる
int& r = a;    r = 20;        // a == 20。r への代入はそのまま a への代入
```

Python の挙動を C++ と比較:
```py
a = [1, 2]
b = a          # a と b は同じリストオブジェクトを指す2つの独立したラベル

b[1] = 20      # オブジェクト本体の書き換え → a も [1, 20] になる
               # （C++ のポインタでも参照でも同じ挙動）

b = None       # b というラベルを別の対象に貼り替えるだけ
               # a は [1, 20] のまま
               # ← もし b が「a の参照」なら a も None になるはずだが、ならない
               # → Python の b = a は「参照」ではなく「ポインタ」的
```

図で見ると:
```
初期:        a ──┐
                 ├──→ [1, 2]
             b ──┘

b[1] = 20 後: a ──┐
                  ├──→ [1, 20]      ← オブジェクト本体が変わるので両方から見える
             b ──┘

b = None 後: a ──→ [1, 20]           ← a のラベルはそのまま
             b ──→ None              ← b だけ別の対象に張り替わる
```
この問題のリンクリスト操作への接続
- `left_node = left_node.next` は「変数 left_node というラベルを別のノードに貼り替える」操作。元のノード自体には触らない。だから呼び出し元の `list1` は影響を受けない（ラベル `list1` は最初のノードに貼られたまま）
- `node.next.next = None` は「ノード本体のフィールド書き換え」。同じノードを指している他の変数（例: `left_node` がまだ同じノードを指していれば）からもこの変化が見える → エイリアスバグの源泉

つまり Python の変数モデルが「ポインタ的」だと理解していれば、リンクリストで何を書き換えると何に波及するかが自然に予測できる。

## Step3
```py
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        tail = dummy
        while list1 is not None and list2 is not None:
            if list1.val <= list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next
        
        if list1 is not None:
            tail.next = list1
        else:
            tail.next = list2

        return dummy.next
```