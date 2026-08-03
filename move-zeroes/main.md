---
tags:
  - algorithm/two-pointer
---

Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements.
Note that you must do this in-place without making a copy of the array.

Example 1:
Input: nums = [0,1,0,3,12]
Output: [1,3,12,0,0]

Example 2:
Input: nums = [0]
Output: [0]
 
Constraints:
- 1 <= nums.length <= 10^4
- -2^31 <= nums[i] <= 2^31 - 1

Follow up: Could you minimize the total number of operations done?

## Step1
手作業で考える。in-placeなので、0が出てきたら0以外の値と交換することを考える。0が連続しない場合は隣のと交換していけばいいので問題ない。0が連続する場合は次に出てくる0ではない値と交換する。この方針でコードを書く。

Accept
Time: 最悪O(n^2) ex. [0,0,0,...,1]
Space: O(1)
```py
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        for i in range(len(nums)):
            if nums[i] == 0:
                j = i
                while j < len(nums) - 1 and nums[j] == 0:
                    # j < len(nums)としてしまうとインデックスがオーバーするケースがある
                    j += 1
                
                # if j == len(nums):
                #     # 一回目ミス
                #     return

                nums[i], nums[j] = nums[j], nums[i]
```
acceptしたが最頻値より500倍ほど遅いので最適化できないか考えてみる
中のwhileループでiより後ろの情報について探索しているのに、iを進めないのは無駄だと考えた。0の情報は一旦入れておいて後から参照する方が良い。それに最適なデータ構造はスタックかキュー。

0が出てくる位置をキューに入れておいて、0以外が出てきたらキューをpopして交換する。これでO(n)になる
Time: O(n)
Space: 最悪O(n) ex. 全要素0
```py
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        remaining_zeros = deque()
        for i in range(len(nums)):
            if nums[i] == 0:
                remaining_zeros.append(i)
                continue
            
            if len(remaining_zeros) == 0:
                continue

            index = remaining_zeros.popleft()
            nums[i], nums[index] = nums[index], nums[i]
            remaining_zeros.append(i)
```
最頻値付近の実行時間に改善。

他の解法
- two pointer
発想：非ゼロを前から詰めていく方式。上記のキュー方式と本質的には同じで、「連続するゼロの一番最初の位置」を記録するwriteポインターを用意する。非ゼロが現れた時、writeポインターの位置と交換をする。非ゼロの時だけwriteポインターをインクリメントする。writeポインターはスワップ操作と合わせると、常に「これまで見てきた非ゼロの個数」を表している。二重の意味がある

「最初のゼロ」と交換をすることで答えになる理由:
ループ中、走査済み領域 `[0, read)` は常に以下の不変条件（invariant）を満たす。
```
[非ゼロ, 非ゼロ, ..., 非ゼロ][0, 0, ..., 0] [未確定領域]
                                          ↑read
                          ↑
                       write (非ゼロとゼロの境界 / 走査済み領域での最初の0の位置)
```

つまり「走査済み領域は常に 非ゼロブロック + 0ブロック にソート済み」で、`write` がその境界＝最初の0の位置を指している。

新しい非ゼロ `nums[read]` に出会ったとき、`nums[write]`（最初の0）と交換すると：
- 非ゼロブロックが末尾に1つ伸びる（順序は出現順なので保たれる）
- 0ブロックは先頭の0を失い、末尾に1つ追加される
- 結果として走査済み領域は再び「非ゼロブロック + 0ブロック」の形を保つ

この不変条件がループ全体で維持されるので、`read = n` に到達した時点で配列全体が答えの形になっている。

Time: O(n)
Space: O(1)
```py
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        write = 0
        for read in range(len(nums)):
            if nums[read] != 0:
                nums[read], nums[write] = nums[write], nums[read]
                write += 1
```
- 最初のゼロが出てくるまで、同じ位置同士でswapを行なってしまうので、以下のガードをつけると良い
```py
for read in range(len(nums)):
    if nums[read] != 0:
        # ガード
        if write != read:
          ...
```
Follow up: Could you minimize the total number of operations done? への回答
- Two pointerが操作回数最小になる。書き込み回数2k (k = 非ゼロの個数)になる。
最悪ケース（[0,0,0,....,1,2,3,...k]のようなケース）で書き込み 2k が下界

Two Pass
1回目で非ゼロを前に詰める -> 2回目で残りを0埋めする
- Time: O(n), Space: O(1)
- swapではなく代入なので定数倍が軽いか？全要素非ゼロの時の書き込みが無駄

```py
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        write = 0
        for x in nums:
            if x != 0:
                nums[write] = x
                write += 1

        # writeは非ゼロブロックとゼロブロックの境界を表すので、write以降を0で埋めれば良い。
        for i in range(write, len(nums)):
            nums[i] = 0
```

### swap vs 代入 の定数倍

計算量はどちらもO(n)だが、メモリアクセス回数（定数倍）に差が出る。

- swap (Two Pointer): 1回あたり 読み2回 + 書き2回 = 4アクセス
- 代入 (Two Pass): 1回あたり 読み1回 + 書き1回 = 2アクセス（ただし2パス目で残りを0埋め）

非ゼロ k個 / ゼロ n-k個 のとき：
- Two Pointer: 走査n + swap時の余計な書き込み 2k
- Two Pass: 走査n + 書き込み k + 0埋め (n-k) = 2n
→ ゼロが多い (k << n) ほど Two Pointer 有利、非ゼロが多いほど Two Pass 有利。

また Two Pointer では `write == read` のとき自己swap（無駄な書き込み）が起きるので、`if write != read:` でガードできる。

### ベンチマーク (N=10000, 200回平均, μs/call)

| シナリオ | two_pointer | two_pointer_guard | two_pass | deque |
|---------|------------:|------------------:|---------:|------:|
| ランダム(50%ゼロ) | 380.4 | 430.8 | **269.8** | 663.4 |
| ゼロ多め(90%ゼロ) | **208.3** | 215.0 | 235.3 | 398.8 |
| 非ゼロ多め(10%ゼロ) | 489.9 | 563.4 | **262.9** | 900.4 |
| 全部非ゼロ | 527.0 | 377.8 | **265.9** | 390.3 |
| 全部ゼロ | **165.2** | 175.4 | 245.1 | 349.6 |

考察:
- 予想通り **ゼロが多い** 入力では Two Pointer が最速（swap自体が起きないので走査だけで済む）。
- **非ゼロが多い** 入力では Two Pass が圧勝。swapの書き込み2回 vs 代入の書き込み1回の差がそのまま出る。
- guard版は「全部非ゼロ」で効果絶大（自己swap回避）だが、ランダム入力ではif分岐コストが上回り遅くなる。入力分布次第。
- deque は Time O(n) でも Python のオブジェクト割り当て + popleftオーバーヘッドで常に最遅。Space O(n) も含めて Two Pointer に劣る。


## Step2

### ループ不変条件 (loop invariant) を意識した変数名とコメント
[fhiyo#50](https://github.com/rihib/leetcode/pull/50#discussion_r1888189547)
> zeroIndexという名前で何を表す変数なのか(indexである以上のことが)分からない気はしました。(...) この問題はループ不変条件が何かを意識するのが大事な気がしており、今回であればzeroIndexより左と、zeroIndexからiまでが各ループの終わりで何が入っているか書いてあると分かりやすい

`write` のような変数は「何の境界か」を不変条件として明記するのが読み手に親切。自分は不変条件を本文に書いたが、変数名 or 直前コメントに `# any elements in nums[:write] are non-zero` のように書く流儀もある（[fhiyo#54](https://github.com/fhiyo/leetcode/pull/54)）。

### 「境界」より「これまで見た非ゼロの個数」と捉える
https://github.com/rihib/leetcode/pull/50#discussion_r1888189547
> これは配列とサイズの組み合わせで追記をしている(vector push_back の動作)ものの変形と感じるので。「いくつ非ゼロが見つかったか」というように見ています。

writeを「次に書く位置 = これまでの非ゼロ個数」と捉えると、最初の0が見つかる前の自己swapも自然に説明できる。つまり、「非ゼロを見つけたら配列にpushする」という操作を本来ならするが、in-placeなので、push先が nums[write]であるということ。0がまだ出てきていなければnums[read]と同じ位置にpushすることになる。

### swap ではなく代入する案
[nittoco#50](https://github.com/rihib/leetcode/pull/50)
> `nums[zeroIndex], nums[i] = nums[i], nums[zeroIndex]` ではなく `nums[zeroIndex] = nums[i]; nums[i] = 0` としてしまう案もありますね。(結局同じですが、意図がわかりやすい気がしてます)

ただしこれは `zeroIndex < i` のときしか正しくないので、Two Pass形式（後から0埋め）の方が安全。

### loop unrolling と一括0fill
https://github.com/fhiyo/leetcode/pull/54
> まとめて 0 fill は、loop unrolling できたりするのでちょっと嬉しいこともあるでしょう。

連続書き込みはコンパイラがループ展開・SIMD化しやすい。Pythonでは `nums[write:] = [0] * (len(nums) - write)` のようにスライス代入すると C 実装の一括処理に乗る（[naoto-iwase#55](https://github.com/naoto-iwase/leetcode/pull/55) の実装3）。CPython本体ではloop unrollingは期待できない。

### 仕様変更への強さ（保守性）
[sasanquaneuf#54](https://github.com/fhiyo/leetcode/pull/54)
> 仮に仕様変更で0ではなくて0以下を端に寄せたいとなった場合にもcontinueする条件をnums[i] <= 0とするだけでワークするので、良いと思います。

「速いから」だけでなく「仕様変更に強いから」で解法を選ぶ視点。`if nums[i] != 0` 型は条件を差し替えるだけで一般化できる。

### 多重代入の言語仕様を確認する癖
https://github.com/rihib/leetcode/pull/50#discussion_r1888189547
> これ C++ だと zeroIndex == i の場合は未定義動作にあたるかと思いますが、Go では大丈夫でしょうか。(...) 言語仕様を調べたことがありますか、それとも漫然と経験上書いていますか、という質問です。

Pythonの場合 [docs](https://docs.python.org/3/reference/simple_stmts.html#assignment-statements) で「右辺を全部評価してから左辺へ代入」と保証されているので `a, a = a, a` も安全。Go の[仕様](https://go.dev/ref/spec#Assignment_statements)も同様。C++では同一オブジェクトへの2回書き込みは未定義動作の可能性。

### Linked List 解法
https://github.com/hroc135/leetcode/pull/51#discussion_r2052911267
> Linked List ならばこの操作は得意ですね。一回全部 list に移した後に、頭から n 要素を調べて、0 だったら MoveToBack をするというコードを書けば、step1 と同じアルゴリズムで O(n) でできる

配列の `pop(i)` は O(n) だが、Linked Listのノード移動は O(1)。アルゴリズム的には同じでも基盤データ構造の選択でオーダーが変わる。

## Step3
Two Passで練習をする
```Py
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        # 不変条件: nums[:write]はすべて非ゼロ
        write = 0
        for num in nums:
            if num != 0:
                nums[write] = num
                write += 1
            
        # この時点でnums[write]はゼロと非ゼロの境界で、初めてゼロになるところ
        nums[write:] = [0] * (len(nums) - write)
```

### 類題

- [27. Remove Element](https://leetcode.com/problems/remove-element/)
- [26. Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/)
- [80. Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/)
- [75. Sort Colors](https://leetcode.com/problems/sort-colors/) (Dutch National Flag, three-way partition)
- [905. Sort Array By Parity](https://leetcode.com/problems/sort-array-by-parity/)

### 参考
- [[不変条件と境界条件の設計]]
- [[sort-colors/main|Sort Colors]]