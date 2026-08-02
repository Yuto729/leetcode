# Insert Interval
You are given an array of non-overlapping intervals intervals where intervals[i] = [start_i, end_i] represent the start and the end of the ith interval and intervals is sorted in ascending order by start_i. You are also given an interval newInterval = [start, end] that represents the start and end of another interval.

Insert newInterval into intervals such that intervals is still sorted in ascending order by start_i and intervals still does not have any overlapping intervals (merge overlapping intervals if necessary).

Return intervals after the insertion.

Note that you don't need to modify intervals in-place. You can make a new array and return it.

Example 1:
Input: intervals = [[1,3],[6,9]], newInterval = [2,5]
Output: [[1,5],[6,9]]

Example 2:
Input: intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
Output: [[1,2],[3,10],[12,16]]
Explanation: Because the new interval [4,8] overlaps with [3,5],[6,7],[8,10].

Constraints:
- 0 <= intervals.length <= 10^4
- intervals[i].length == 2
- 0 <= start_i <= end_i <= 10^5
- intervals is sorted by starti in ascending order.
- newInterval.length == 2
- 0 <= start <= end <= 10^5

## Step1
- `intervals`はソートされている想定なので、二分探索で「新しい区間の開始時刻以下の開始時刻である最後のインデックス」を求める。
    - そのインデックスより前の区間は挿入後も変化しないので先に加える。
- 上記の位置からスタートして、「初めて新しい区間の終了時刻以上の終了時刻である区間のインデックス」を求める。
    - その２つのインデックスでいくつかの場合分けをし、重複期間を求める

```py
class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        if not intervals:
            return [newInterval]
        
        result = []
        # idx = startがnewInterval[0]以下の最も右の区間のインデックス
        idx = bisect_right(intervals, newInterval[0], key=lambda x: x[0]) - 1
        if idx == -1:
            idx = 0

        result = []
        result.extend(intervals[:idx])
        j = idx
        while j < len(intervals) and intervals[j][1] < newInterval[1]:
            j += 1
        # jは初めてintervals[j][1] >= newInterval[1]となる位置
        new_start = intervals[idx][0]
        if newInterval[0] < intervals[idx][0]:
            new_start = newInterval[0]

        if intervals[idx][1] < newInterval[0]:
            result.append(intervals[idx])
            new_start = newInterval[0]
        
        new_end = newInterval[1]
        if j < len(intervals) and intervals[j][0] <= newInterval[1]:
            new_end = intervals[j][1]
        
        result.append([new_start, new_end])
        if j < len(intervals) and intervals[j][0] > newInterval[1]:
            result.append(intervals[j])
        
        result.extend(intervals[j + 1: ])
    
        return result
```

AIにレビューしてもらったがよく考えると二分探索を使う必要がない。以下のフローで書き直せる
区間を3つのフェーズに分けて処理する：
1. newIntervalより前の区間（end < newInterval[0]）をそのまま追加
2. newIntervalと重なる区間をまとめてマージ
3. 残りの区間をそのまま追加

Time: O(N)
Space: O(N)

### パターン1: ループ内でnew_endを更新

ループ中に状態を作る設計のコード
```python
class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        i = 0
        result = []

        while i < len(intervals) and intervals[i][1] < newInterval[0]:
            result.append(intervals[i])
            i += 1

        # i はintervals[i]がnewIntervalより完全に前ではない位置
        new_start = newInterval[0]
        new_end = newInterval[1]
        while i < len(intervals) and intervals[i][0] <= newInterval[1]:
            # 重なる場合
            new_start = min(new_start, intervals[i][0])
            new_end = max(new_end, intervals[i][1])
            i += 1

        result.append([new_start, new_end])
        result.extend(intervals[i:])
        return result
```

### パターン2: ループ後にintervals[i-1]からnew_endを計算

2つ目のwhileでiを進めるだけにして、ループ後に `intervals[i-1]`（最後に重なった区間）からnew_endを求める。
ループ後に状態を読む設計のコード。

```python
class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        if not intervals:
            return [newInterval]

        i = 0
        result = []
        while i < len(intervals) and intervals[i][1] < newInterval[0]:
            result.append(intervals[i])
            i += 1
        
        new_start = min(intervals[i][0], newInterval[0]) if i < len(intervals) else newInterval[0]
        new_end = newInterval[1]
        while i < len(intervals) and intervals[i][0] <= newInterval[1]:
            i += 1

        # intervals[i-1]が最後に重なった区間（1つ目のwhileだけ進んだ場合はend < newInterval[0]なので影響なし）
        if i > 0:
            new_end = max(newInterval[1], intervals[i - 1][1])

        result.append([new_start, new_end])
        result.extend(intervals[i:])
        return result
```
パターン２は最初から書こうと思った時に認知負荷が高い。理由としては、
- 1回目のループを抜けた後`new_start`を初期化する時に`intervals[i]`と`newInterval`が重なっているかを暗黙にチェックしている。
    - `intervals[i]`が重なるなら、そのstartかもしれない
    - 重ならない（完全に`intervals[i]`が後ろ）ならminは`newInterval[0]`になる。

- ２つ目のループの目的が、「重ならなくなる最初の位置」を求めることになっている。それだと、重ならなくなる最初の位置が先頭、つまり最初から重ならない場合も含んでいて、その時の場合分けが必要になる(`i > 0`)。
- また、1つ目のwhileだけ進んだ場合は、`i > 0`を満たす場合でも、i以降と**重ならず**`newInterval`がすっぽり入るが、その場合でもmaxで`newInterval[1]`が選ばれて`new_end`の結果が同じなので問題ないことが一見分かりずらい

- `i`の意味が時間とともに変化する
    - 1つの目のwhileの後 -> 重なるかもしれない最初の区間
    - 2つ目のwhileの後 -> 重ならない最初の区間
    - `intervals[i - 1]` -> 最後に重なった区間

パターン１だとなぜ書きやすいか？
- １つ目のループ後の`i`は「intervals[i]がnewIntervalより完全に前ではない位置」を意味する
    - 1つ目のループの責務はnewIntervalより完全に前の部分を先に入れておくこと

- ２つ目のループは重なる場合にマージをすること
    - マージ操作は`new_start`, `new_end`を同じループ内で更新することで行う
    - `i`の意味が常に「今見ている位置」で固定される
    -> 重なる間は新区間を広げるという不変条件のみ

- ループを出た後に状態を読まなくて良くなる
    - 次のループでは、マニュアル(後述)と開始位置だけ渡して仕事をしてもらうことができる

エッジケース
| ケース | 入力 | 出力 |
|--------|------|------|
| 空配列 | `[]`, `[1,2]` | `[[1,2]]` |
| 全区間より前 | `[[3,5]]`, `[1,2]` | `[[1,2],[3,5]]` |
| 全区間より後 | `[[1,2]]`, `[3,4]` | `[[1,2],[3,4]]` |
| 内包される | `[[1,5]]`, `[2,3]` | `[[1,5]]` |
| 全区間をまたぐ | `[[1,2],[3,4]]`, `[1,4]` | `[[1,4]]` |

### 他の解法
A. Merge Intervalに帰着させる
time: O(NlogN)
space: O(N)
```py
class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        new_intervals = intervals + [newInterval]
        new_intervals.sort()
        merged_intervals = []
        for i in range(len(new_intervals)):
            if merged_intervals and new_intervals[i][0] <= merged_intervals[-1][1]:
                previous_interval = merged_intervals.pop()
                merged_intervals.append([previous_interval[0], max(previous_interval[1], new_intervals[i][1])])
                continue
            merged_intervals.append(new_intervals[i])
        
        return merged_intervals
```

B. Sweep Line
time: O(NlogN)
space: O(N)
Merge IntervalsでやったSweep Lineをそのまま適用する。newIntervalをイベントに足すだけ
```py
class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        events = []
        for start, end in intervals + [newInterval]:
            events.append((start, +1))
            events.append((end, -1))
        
        sorted_events = sorted(events, key=lambda x: (x[0], -x[1]))
        current_start = 0
        count = 0
        result = []
        for time, diff in sorted_events:
            if diff == 1 and count == 0:
                current_start = time

            count += diff
            if count == 0:
                result.append([current_start, time])
        
        return result
```

C. 二分探索だけを使う
重なる区間の範囲 [left, right]を直接求める。「最初に終了時刻 >= newInterval[0]となる時刻」「最後にnewInterval[1] >= 開始時刻」となるインデックスをそれぞれ求める。
それぞれ、`bisect_left(終了時刻の配列, newInterval[0])`, `bisect_right(開始時刻の配列, newInterval[1]) - 1`になる

time: O(N) ends, starts配列の作成、スライスでのコピーで発生
space: O(N)
```py
class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        if not intervals:
            return [newInterval]
        
        ends = [interval[1] for interval in intervals]
        starts = [interval[0] for interval in intervals]

        left = bisect_left(ends, newInterval[0])
        right = bisect_right(starts, newInterval[1]) - 1
        # [left, right]まで重なりがある
        if left > right:
            # 重なりが存在しない
            return intervals[:left] + [newInterval] + intervals[left: ]

        merged = [min(newInterval[0], intervals[left][0]), max(newInterval[1], intervals[right][1])]

        return intervals[:left] + [merged] + intervals[right + 1: ]
```

## Step2

### 入力を破壊しない

https://github.com/ryosuketc/leetcode_grind75/pull/26#discussion_r2541466847

> 入力を変更している点が気になりました。呼び出し側の視点に立って考えると、関数に渡した値が勝手に書き換えられているとびっくりすると思います。入力は原則変更しないか、変更する場合は関数コメントでそれを明記することをおすすめします。

なるべく関数は純粋に保ったほうが良さそう

### 高次概念と低次操作の距離を縮める — 関数分割

https://github.com/ryosuketc/leetcode_grind75/pull/26#discussion_r2541466847

> 「2つのインターバルを引数に取って被ってるかを判定する関数」作りませんか。で、次に「2つのインターバルをくっつける関数」です。この2つあればできませんか。

> 左にあるか、オーバーラップしているかどうか、という高次の概念と、`[0][1]`の比較という低次の操作の距離が遠いので、やっているうちに混乱するというものです。

２つ目の自分の解法に適用すると、以下のようになる
```py
while i < len(intervals) and is_before(intervals[i], newInterval):
    result.append(intervals[i])
    i += 1
... 

while i < len(intervals) and overlaps(intervals[i], newInterval):
    merged = merge(merged, intervals[i])
    i += 1
```

### 複数人でシフトを組めるか

https://github.com/ryosuketc/leetcode_grind75/pull/26#discussion_r2548502413

> 発想のときに「手でできるか」の後に「複数人でシフトを組んでできるか」という話をしています。
>
> queue に移したか、というとテッシュのボックスみたいに、一枚ずつ紙を引っ張ると出てくるような仕組みのほうが、複数人でシフトを組む上で都合がいいからです。
>
> フラグの管理をするというのは、複数人でシフトを組む上では、部屋に大きなホワイトボードを置いておいて、従業員たちに参照や書き換えをさせるということです。一方行にしか状態が遷移していかないならば、別のマニュアルにしてマニュアルの取り換えをしたほうがいいでしょう。

1ループ＋フラグ管理は「共有ホワイトボード」、3フェーズに分けるのは「マニュアルの取り換え」。状態遷移が一方向なら後者のほうが素直で分かりやすい。
マニュアルの取り替えは、各マニュアルに基づいた処理ごとに関数化できるのでテストも書きやすい。一方で複数の状態を同時に管理していると関数への切り出しが少し難しい。

### `mergeIntervals(intervals1, intervals2)` への一般化

https://github.com/ryosuketc/leetcode_grind75/pull/26#discussion_r2548502413

> intervals1 と intervals2 という2つのティッシュボックスがあって、全部のテッシュをマージしたいです。intervals2 には newInterval と書かれたティッシュだけ入れればいいです。

Insert Intervalを「2つのソート済み区間リストのマージ」に一般化する発想。Merge Sortのマージステップと同じ構造で書ける。

```python
class Solution:
    def merge_intervals(
        self,
        intervals1: List[List[int]],
        intervals2: List[List[int]],
    ) -> List[List[int]]:
        result = []
        i = j = 0

        while i < len(intervals1) or j < len(intervals2):
            # どちらのリストから次の区間を取り出すか決定
            if i < len(intervals1) and (j >= len(intervals2) or intervals1[i][0] <= intervals2[j][0]):
                current = intervals1[i]
                i += 1
            else:
                current = intervals2[j]
                j += 1

            # resultが空、または重ならない場合は新しい区間として追加
            if not result or current[0] > result[-1][1]:
                result.append(current)
            else:
                # 重なる場合はresultの末尾を更新
                result[-1][1] = max(result[-1][1], current[1])

        return result

    def insert(
        self, intervals: List[List[int]], newInterval: List[int]
    ) -> List[List[int]]:
        return self.merge_intervals(intervals, [newInterval])
```

`merge_intervals` は2つのソート済み区間リストを受け取る汎用関数。`insert` はその特殊ケース（片方が単一区間のリスト）として実装される。

さらに k-way merge にも拡張可能（`heapq` で各リストの先頭を管理）：

```python
import heapq

def merge_k_interval_lists(lists: List[List[List[int]]]) -> List[List[int]]:
    result = []
    heap = []
    # 各リストの先頭をヒープに入れる: (start, list_idx, interval_idx)
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0][0], i, 0))

    while heap:
        _, list_idx, interval_idx = heapq.heappop(heap)
        current = lists[list_idx][interval_idx]

        # 次の要素をヒープに追加
        if interval_idx + 1 < len(lists[list_idx]):
            next_iv = lists[list_idx][interval_idx + 1]
            heapq.heappush(heap, (next_iv[0], list_idx, interval_idx + 1))

        if not result or current[0] > result[-1][1]:
            result.append(current)
        else:
            result[-1][1] = max(result[-1][1], current[1])

    return result
```

### 変数名

[huyfififi#26](https://github.com/huyfififi/coding-challenges/pull/26)

> 新しいリストの変数名に迷った。`answer`は曖昧でもう少し情報が欲しいし、`intervals_after_insertion`としてしまったが、本当に挿入後のインターバルのリストになるのは最後の最後なので、途中経過においてその名付けは語弊を生む。`new_intervals`はどうだろう。

`merged_intervals`, `output_intervals` なども候補

### 位置に意味を持たせるなら tuple

[huyfififi#26](https://github.com/huyfififi/coding-challenges/pull/26)

> 位置が意味を持つことがコメントなどで明確に共有されていれば良いのだが、`intervals[i][0]`がi番目の区間の始まりを表していて、`intervals[i][1]`がi番目の区間の終わりを表していることが少しわかりづらく感じる。(位置に意味を持たせるなら、immutableな`tuple`の方が使われている印象。)

`[start, end]` のように位置に意味を持たせるなら、`namedtuple` / `@dataclass` を使いたい。
LeetCodeでは入力が `List[List[int]]` 固定なので、ループ内で `start, end = interval` のように分解するのが良さそう

## Step3

```py
class Solution:
    @staticmethod
    def is_before(interval1, interval2):
        return interval1[1] < interval2[0]

    @staticmethod
    def overlaps(interval1, interval2):
        return interval1[0] <= interval2[1] and interval2[0] <= interval1[1]

    @staticmethod
    def merge(interval1, interval2):
        return [min(interval1[0], interval2[0]), max(interval1[1], interval2[1])]

    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        if not intervals:
            return [newInterval]
        
        i = 0
        merged_intervals = []
        while i < len(intervals) and self.is_before(intervals[i], newInterval):
            merged_intervals.append(intervals[i])
            i += 1
        
        merged = [newInterval[0], newInterval[1]]
        while i < len(intervals) and self.overlaps(intervals[i], merged):
            # 重なっている間
            merged = self.merge(intervals[i], merged)
            i += 1

        merged_intervals.append(merged)
        merged_intervals.extend(intervals[i: ])
        return merged_intervals
```
## 類題

本リポジトリで解いた関連問題：
- [merge-intervals/](../merge-intervals/) — 本問題の前段。重なる区間をまとめる
- [meeting-rooms/](../meeting-rooms/) — 会議が重ならないかを判定（区間オーバーラップの基本）
- [meeting-rooms-ii/](../meeting-rooms-ii/) — 同時に必要な会議室数。Sweep Lineが効く
- [search-insert-position/](../search-insert-position/) — ソート済み配列への挿入位置を二分探索で

類題
- Interval List Intersections
- Non-overlapping Intervals
- My Calendar I, II
- Range Module