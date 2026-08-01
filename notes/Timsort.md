---
tags:
  - Leetcode
  - ソート
  - アルゴリズム
  - Python
  - 内部実装
---

# Timsort

Python の `sorted()` / `list.sort()` で使われているソートアルゴリズム。Tim Peters が 2002 年に Python のために設計。Java (Arrays.sort for objects)、Android、Rust (`slice::sort`) などでも採用されている。

参考: https://tech.preferred.jp/ja/blog/tim-sort/

---

## 特徴

- **ハイブリッド**: Merge sort + Insertion sort の組み合わせ。
- **安定ソート (stable)**: 同じキーの要素の相対順序が保たれる。
- **適応的 (adaptive)**: 入力が部分的にソート済みだと高速化される。
- **In-place に近い**: 補助領域は O(n) だがフルマージソートより小さく抑える工夫あり。

位置づけとしては「STL の IntroSort のマージソート版」。IntroSort がクイックソートをベースに、再帰深さで heapsort、要素数で insertion sort に切り替えるのと同様、Timsort は merge sort をベースに局所的に insertion sort を組み合わせる。

---

## 計算量

| ケース | Time |
|---|---|
| 最良 (既ソート、逆順ソート済み) | **O(n)** |
| 平均 | O(n log n) |
| 最悪 | O(n log n) |
| Space | O(n) |

最良 O(n) なのが特徴。現実のデータは部分的にソート済みのことが多く、そこで性能を発揮する。

---

## アルゴリズムの流れ

### 1. Run 作成フェーズ

入力列を「run」と呼ばれる **単調な連続部分列** に分割する。

- 配列を先頭から見て、**単調増加 (または単調減少) の最大接頭辞** を切り出す。
- 単調減少だった場合は **反転** して増加 run にする (安定性を保つため、strict descending のみ反転)。
- run が短すぎる場合 (< minrun) は、足りない分を後続の要素から取って **insertion sort** で拡張する。

### 2. Minrun の決定

run のサイズ minrun は次の方針で決める:

- insertion sort が最速の範囲 (< 64, 通常 32 前後) でできるだけ大きく。
- かつ、**run の総数が 2 の累乗に近づく** ように調整 (後段のマージのバランスを取るため)。
- 結果として `[32, 64]` の範囲のどれかが選ばれる。

具体的には: `n` の上位 6 bit を取り、残りに 1 bit でも立っていれば +1 する、というロジック (CPython の `merge_compute_minrun`)。

### 3. マージフェーズ

run をスタックに積みながら、サイズのバランスを保つようにマージしていく。

**スタック不変条件** (top を先頭とする):

```
length[top]    + length[top-1] < length[top-2]
length[top]                    < length[top-1]
```

この条件が崩れたら、`top` と `top-1`、または `top-1` と `top-2` の小さい方とマージする。これにより、マージ対象のサイズが極端に偏ることを防ぎ、全体で O(n log n) を保証する。

### 4. Galloping Mode

マージ中、**一方の run から連続して 7 要素以上採用される** と「ギャロップモード」に切り替わる。

- 通常モード: 2 つの run の先頭同士を比較し、小さい方を出力 (1要素ずつ)。
- ギャロップモード: 「次にどこまでまとめて採用できるか」を **指数探索 + 二分探索** で一気に決めて、まとめて出力する。

一方の run が他方より明らかに小さい / 大きい場合に劇的に高速化される。連続採用が減ったら通常モードに戻る。

---

## 擬似コード

```text
function timsort(A):
    n = len(A)
    minrun = compute_minrun(n)
    stack = []           # run のスタック (開始位置, 長さ)

    i = 0
    while i < n:
        # 1. 自然な run を検出
        run_start = i
        run_end = find_run(A, i)   # 単調増加/減少の最大接頭辞
        if A[i..run_end] が降順:
            reverse(A, i, run_end)

        # 2. minrun に満たなければ insertion sort で拡張
        run_len = run_end - run_start
        if run_len < minrun:
            extend = min(minrun, n - run_start)
            binary_insertion_sort(A, run_start, run_start + extend)
            run_len = extend

        # 3. スタックに push
        stack.push((run_start, run_len))
        i = run_start + run_len

        # 4. 不変条件を満たすようマージ
        merge_collapse(stack, A)

    # 5. 残った run をすべてマージ
    merge_force_collapse(stack, A)


function merge_collapse(stack, A):
    while len(stack) >= 2:
        let X, Y, Z = stack[-1], stack[-2], stack[-3]  # 存在する分だけ
        if (len(stack) >= 3 and Z.len <= X.len + Y.len) or
           (len(stack) >= 4 and W.len <= Y.len + Z.len):
            if Z.len < X.len:
                merge(Y, Z); pop Y, Z; push merged
            else:
                merge(X, Y); pop X, Y; push merged
        elif Y.len <= X.len:
            merge(X, Y); pop X, Y; push merged
        else:
            break
```

---

## Python での実装例 (簡易版)

理解用の簡易実装。実用版 (CPython の `Objects/listobject.c` の `listsort_impl`) は数千行ある。

```python
MIN_MERGE = 32

def compute_minrun(n):
    r = 0
    while n >= MIN_MERGE:
        r |= n & 1
        n >>= 1
    return n + r


def insertion_sort(arr, left, right):
    """arr[left:right+1] を insertion sort"""
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def merge(arr, l, m, r):
    """arr[l:m+1] と arr[m+1:r+1] をマージ (両方ともソート済み前提)"""
    left = arr[l:m + 1]
    right = arr[m + 1:r + 1]
    i = j = 0
    k = l
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]; i += 1
        else:
            arr[k] = right[j]; j += 1
        k += 1
    while i < len(left):
        arr[k] = left[i]; i += 1; k += 1
    while j < len(right):
        arr[k] = right[j]; j += 1; k += 1


def timsort(arr):
    n = len(arr)
    minrun = compute_minrun(n)

    # 1. minrun ごとに insertion sort で run を作る
    for start in range(0, n, minrun):
        end = min(start + minrun - 1, n - 1)
        insertion_sort(arr, start, end)

    # 2. run を merge していく (サイズを倍々に)
    size = minrun
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(left + size - 1, n - 1)
            right = min(left + 2 * size - 1, n - 1)
            if mid < right:
                merge(arr, left, mid, right)
        size *= 2

    return arr


# 動作確認
if __name__ == "__main__":
    a = [5, 21, 7, 23, 19, 10, 4, 8, 12, 1, 3, 17, 9, 14, 22]
    print(timsort(a))
```

注意: この簡易版は「自然な run の検出」「galloping mode」「stack invariant に基づくマージ順制御」を省略している。実用の Timsort はこれらの最適化により、現実のデータで圧倒的に高速になる。

---

## なぜ実用で強いか

- 現実のデータは「完全ランダム」ではなく **部分的にソート済み** のことが多い (例: ログを時刻順に追記、ID 順に近い配列、ほぼソート済み + ノイズ)。
- Timsort は自然な run を検出してそのまま使うので、こうした入力で線形時間に近づく。
- Galloping mode により、「片方の run の値域がもう片方とほぼ重ならない」ケースで大幅な高速化。
- 安定ソートなので、複合キーソート (例: 名前で並べた後に年齢で並べる) で挙動が予測可能。

理論的な O(n log n) ソート (heapsort、純粋な merge sort) より定数倍で速いことが多く、安定性も持つため、汎用ライブラリのデフォルトとして採用されている。

---

## LeetCode との関連

`sorted(nums)` や `nums.sort()` を使うと内部で Timsort が走る。

- 計算量を答えるときは **O(n log n)** で OK (最悪も O(n log n))。
- ただし「ほぼソート済み入力で速い」のは Timsort の性質として知っておくと、入力の性質を活かす議論ができる。

---

## 参考

- PFN ブログ: https://tech.preferred.jp/ja/blog/tim-sort/
- CPython 実装: `Objects/listobject.c` の `listsort_impl`
- Tim Peters 原文の解説: `Objects/listsort.txt` (CPython リポジトリ内)
- Wikipedia: https://en.wikipedia.org/wiki/Timsort
