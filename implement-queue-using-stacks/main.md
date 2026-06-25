# 232. Implement Queue using Stacks

Implement a first in first out (FIFO) queue using only two stacks. The implemented queue should support all the functions of a normal queue (push, peek, pop, and empty).

Implement the MyQueue class:

void push(int x) Pushes element x to the back of the queue.
int pop() Removes the element from the front of the queue and returns it.
int peek() Returns the element at the front of the queue.
boolean empty() Returns true if the queue is empty, false otherwise.
Notes:

You must use only standard operations of a stack, which means only push to top, peek/pop from top, size, and is empty operations are valid.
Depending on your language, the stack may not be supported natively. You may simulate a stack using a list or deque (double-ended queue) as long as you use only a stack's standard operations.

Example
Input
["MyQueue", "push", "push", "peek", "pop", "empty"]
[[], [1], [2], [], [], []]
Output
[null, null, null, 1, 1, false]

Explanation
MyQueue myQueue = new MyQueue();
myQueue.push(1); // queue is: [1]
myQueue.push(2); // queue is: [1, 2] (leftmost is front of the queue)
myQueue.peek(); // return 1
myQueue.pop(); // return 1, queue is [2]
myQueue.empty(); // return false

Follow-up: Can you implement the queue such that each operation is amortized O(1) time complexity? In other words, performing n operations will take overall O(n) time even if one of those operations may take longer.

## Step1

ナイーブに２つのスタックを使って、互いに入れ替えるような操作を実装する
時間計算量: O(N)

```py
class MyQueue:

    def __init__(self):
        self.items = []

    def push(self, x: int) -> None:
        self.items.append(x)

    def pop(self) -> int:
        if self.empty():
            return None

        buffer = []
        while self.items:
            item = self.items.pop()
            if not self.empty():
                buffer.append(item)

        while buffer:
            self.items.append(buffer.pop())

        return item

    def peek(self) -> int:
        if self.empty():
            return None

        buffer = []
        while self.items:
            item = self.items.pop()
            buffer.append(item)

        while buffer:
            self.items.append(buffer.pop())

        return item

    def empty(self) -> bool:
        return len(self.items) == 0
```

follow-up
各操作の償却計算量でO(1)にできるか？

２つのスタックの役割を分けてうまくやるっぽいがわからないのでAIにヒントをもらう

> 今のコードの「無駄」に注目する

> Step1の pop / peek を見ると、こういう動きをしています：

> 1. items を全部 buffer に移す（順番がひっくり返る）
> 2. 1個取り出す
> 3. buffer を全部 items に戻す（また順番が元に戻る）

> ヒント1: ステップ3の「戻す」作業、本当に毎回必要でしょうか？ せっかくひっくり返した順番、次の pop でまた使えそうな気がしませんか？

> ヒント2: 2つのスタックに「役割」を持たせる

値を追加していくスタックと別に、pop/peekで取り出す専用のスタックを用意する。スタックでFIFOできるようにするには、pop/peek用スタックは挿入順と逆順になっている必要がある。毎回逆順になることを保証するのは計算量の観点から無駄が生じるので、「pop/peekスタックが空」のときだけ、構築操作を行う。
空でない時にpop/peekされた場合、専用スタックの末尾を返す（popする）。
構築操作を、空のときだけ行う理由は、

- 「古い要素を全部吐き出してから次の塊を入れる」という不変条件を守ることで、誤って古い要素より新しい要素が上（front）扱いされることがなくなる
- 償却計算量がO(1)になる

以下解説
pop/peek用スタックに移し替えるとき、追加用スタックにK個の要素があるとすると、移し替えのコストはO(K)だが、次に移し替えが発生するまで、少なくともK回以上のpopが必要となる。つまり、移し替えのコストO(K)はその後にくるK回のpopに割り当てられるので、1回のpopあたりO(K) / K = O(1)となる。

他の考え方として、「各要素に着目する」と、ある一つの要素が経験する操作は、

- 1.「追加用スタック」へpush
- 2. 上記からpopして「pop/peek用スタック」へpush -> 移し替え、1回だけ
- 3. 「pop/peek用スタック」からpop

2の移し替えは各要素につき、高々1回なので、n個の要素を処理する総コストは、O(3\*n)。n操作で割れば1操作あたりO(1)

```py
class MyQueue:

    def __init__(self):
        self.items = []
        self.reversed_items = []

    def push(self, x: int) -> None:
        self.items.append(x)

    def pop(self) -> int:
        if self.empty():
            return None

        if len(self.reversed_items) == 0:
            self._move_items_to_reversed()

        return self.reversed_items.pop()

    def peek(self) -> int:
        if self.empty():
            return None

        if len(self.reversed_items) == 0:
            self._move_items_to_reversed()

        return self.reversed_items[-1]

    def empty(self) -> bool:
        return len(self.items) == 0 and len(self.reversed_items) == 0

    def _move_items_to_reversed(self):
        while self.items:
            self.reversed_items.append(self.items.pop())

```

AIレビュー

- `len(self.reversed_items) == 0`より`not self.reversed...`の方がPythonらしい
- 空のときにNoneを返す設計について、例外を投げる方が早く失敗する設計としていいのでは？

- 変数名/メソッド名
  - items -> 中身が要素であることしか言っていない
  - reversed_items -> reversed（逆順）」という実装の詳細を名前にしている。これは読み手に「なぜ逆順なのか」を考えさせてしまう。
    命名を、「何のためのものか」つまり、役割をベースに考えると、
    - `self.input_stack`, `self.output_stack`が良さそう

  - \_move_items_to_reversed -> 何をやっているかというと、「入力側を出力側へ移し替える」操作
    - 意味を反映すると、`_transfer`, `_move_to_out_stack`など

償却がO(1)であれば最悪O(N)でも良いケースとは？

- スループット、つまり総処理時間だけが大事で、たまに遅延しても良い普通のバッチ処理やAPIなど.逆に1つ1つの処理の速度要件が厳しいと使えない

## 他の方のまとめ

> 🤖4つのPRのレビュー内容をまとめました。重要度順に並べています。

### 内容1: Okasaki『純粋関数型データ構造』とBanker's Queue ― この問題の本質的背景

[rihib#32](https://github.com/rihib/leetcode/pull/32/files#r1747065820) / [ryosuketc#13](https://github.com/ryosuketc/leetcode_grind75/pull/32)

> 純粋関数型データ構造にこれ載っていた気がします。
> Chris Okasaki の [Purely Functional Data Structures](https://www.cs.cmu.edu/~rwh/students/okasaki.pdf) に載ってますね。BankersQueue です。

複数のPRで同一レビュアーから言及されている最重要トピック。この「2スタックでキュー」は単なるパズルではなく、**関数型言語で永続データ構造として効率的なキューを作る**という研究背景を持つ。Okasakiの本では遅延評価(lazy evaluation)を使い、移し替えを「均す」のではなく**遅延させる**ことで、永続的に使っても償却O(1)を保証する `BankersQueue` / `PhysicistsQueue` が紹介されている。naoto-iwase#67のメモにも参考資料(slideshare, PDF)へのリンクあり。

### 内容2: 遅延評価版は命令型言語では難しい

[naoto-iwase#67](https://github.com/naoto-iwase/leetcode/pull/67#discussion) (line 139)

> あ、これは償却でいいと思います。遅延させるのはちょっと大変です。やるならば、Generator でも使えばできますかねー。

「均し(amortized)」と「遅延(lazy)」は別物。Pythonでは厳密な遅延評価版の実装は難しく、やるならGeneratorで擬似的に、という指摘。我々が実装した「out_stackが空のときだけ移す」は均し版で、これで十分というお墨付き。永続的（過去の状態を保持して複数回使う）場合に均し版が崩れる、というのが遅延版が必要になる理由。

### 内容3: pop/peekの重複ロジックは peek() に一元化

[naoto-iwase#67](https://github.com/naoto-iwase/leetcode/pull/67) / [rihib#32](https://github.com/rihib/leetcode/pull/32)

```python
def pop(self) -> int:
    self.peek()        # _shelfに値があることを保証
    return self._shelf.pop()
def peek(self) -> int:
    if not self._shelf:
        self._stock()
    return self._shelf[-1]
```

我々が議論した「pop/peekの分岐重複」問題に対する一つの定番解。`pop` が `peek` を呼ぶことで「out_stackに要素があることの保証」を peek に集約する。rihibのGo版も `Pop` が `Peek` を呼ぶ同じ構造。ただし huyfififi のレビューでは「視線が移動するので書き下す方が好み」という反対意見もあり、ここは好みが分かれるポイント。

### 内容4: 変数名 ― in/out 系が定番、storage/shelf のような比喩も

[ryosuketc#13](https://github.com/ryosuketc/leetcode_grind75/pull/13) (step3.cpp line 6)

> 分かりやすい名前で良いと思いました！（自分はpush用のスタック、pop用のスタックで `stack_push, stack_pop` とかにするかなと考えていました）

我々の `input_stack`/`output_stack` 議論と一致。実際に採用されている命名のバリエーション：

- `stack_in` / `stack_out`（ryosuketc, 最終版）
- `pushStack` / `popStack`（rihib, Go）
- `store` / `retrievable`（kitano）→ ただし後述の指摘あり
- `_storage` / `_shelf`（naoto-iwase, 倉庫と商品棚の比喩）

### 内容5: `...able` で終わる名前はbool値を期待させる

[kitano-kazuki#79](https://github.com/kitano-kazuki/leetcode/pull/79) (memo.md line 24)

> ...ableという変数名はboolであることを期待させるように思います。また、意味的にも、storeもretrievableもどちらもstoreされた値ではあるので、storeはunprocessedとかtemporaryみたいなもの、retrievableはprocessedみたいなもの、ぐらいが良いのかなと思いました。

`retrievable` という名前が後で `if retrievable:` と書かれると「取得可能か」というbool判定に読めてしまう違和感。命名は型の期待まで含めて選ぶべき、という鋭い指摘。

### 内容6: `not (a)` の冗長な括弧 ― 演算子の優先順位

[kitano-kazuki#79](https://github.com/kitano-kazuki/leetcode/pull/79) (memo.md line 48)

> notはandより優先されるので()は不要ですね。あっても無害ですが、冗長な()は個人的には外したいです。
> https://docs.python.org/3/library/stdtypes.html#boolean-operations-and-or-not

`not` は `and`/`or` より優先順位が高いので `(not a) and (not b)` の括弧は不要。`not a and not b` で同じ意味。我々が議論した `not self.out_stack` の話とも通じる。

### 内容7: 略称 `aux` (auxiliary) の使いどころ

[ryosuketc#13](https://github.com/ryosuketc/leetcode_grind75/pull/13) (memo.md line 12)

> aux はたまにみますが、私の考える典型例は下のような再帰のための補助関数ですね。
> `static int IntersectAux(...)` （Chromium/V8のソース）

`aux` は「補助」の略称として実在するが、典型的な使用例は**再帰のヘルパー関数**（`fooAux`）。スタックの補助変数名としてはやや非典型、という文脈の解説。実際のChromium/V8コードへのリンク付き。

### 内容9: 空のとき例外を投げるか問題 ― 「特殊なintが作れない」

[ryosuketc#13](https://github.com/ryosuketc/leetcode_grind75/pull/13) (memo.md line 19)

> C++ は速度のために配列外アクセスは未定義動作にしてよいという風潮がありますが、まあ、空で pop したら例外を投げるほうが行儀はいいでしょうね。

我々が議論した「None vs 例外」と全く同じ論点。ryosuketcのメモには鋭い考察：**「どのようなintもqueueに入りうるので、特定のintをエラー値として扱うのは無理がある」**→ だから例外を選ぶ、という根拠。エラー値で表現できない場合は例外が正当化される好例。

---

## 練習

変数名、関数名を整えた。また、空キューに対するpop/peekは例外を投げるようにした

```py
class MyQueue:
    def __init__(self):
        self.input_stack = []
        self.output_stack = []

    def push(self, x: int):
        self.input_stack.append(x)


    def pop(self):
        if self.empty():
            raise IndexError("pop from empty queue")

        if not self.output_stack:
            self._move_to_out_stack()

        return self.output_stack.pop()


    def peek(self):
        if self.empty():
            raise IndexError("peek from empty queue")

        if not self.output_stack:
            self._move_to_out_stack()

        return self.output_stack[-1]


    def empty(self):
        return not self.input_stack and not self.output_stack


    def _move_to_out_stack(self):
        while self.input_stack:
            self.output_stack.append(self.input_stack.pop())
```

### 過去に解いた類題（本リポジトリ内）

- [kth-largest-element-in-a-stream](../kth-largest-element-in-a-stream/main.md) データ構造設計（クラス実装）系
