# Merge Intervals
Given an array of intervals where intervals[i] = [start_i, end_i], merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.

Example 1:
Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].

Example 2:
Input: intervals = [[1,4],[4,5]]
Output: [[1,5]]
Explanation: Intervals [1,4] and [4,5] are considered overlapping.

Example 3:
Input: intervals = [[4,7],[1,4]]
Output: [[1,7]]
Explanation: Intervals [1,4] and [4,7] are considered overlapping.

## Approach
制約
- 区間の要素は0以上の整数
- 配列の長さの最大は10^4程度
- 各要素の値の最大値も10^4程度
- [start, end]はstart <= endが保証されている
- 空の配列は来ない

Meeting Rooms Iと同じように、区間配列を開始時刻で並び替えて隣同士をみる。隣同士について、start_i+1 <= end_iなら重なりがあると判定し、マージをする。マージしたら区間配列を更新する必要があるが、ここはスタックが使えそう。
`intervals`を走査し、スタックの末尾の区間と新しい区間に重なりがある場合は、ポップしてマージした区間をスタックに追加する。重なりがない場合はそのまま追加する
マージは、[スタックの末尾の区間の始まり, スタックの末尾の区間と新しい区間の終わりのうちで大きい方]でできる

Time: O(N logN) ソート分
Space: O(N)

```py
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        sorted_intervals = sorted(intervals, key=lambda x: (x[0], x[1]))
        stack = []
        for interval in sorted_intervals:
            if stack and stack[-1][1] >= interval[0]:
                previous = stack.pop()
                stack.append(([previous[0], max(interval[1], previous[1])]))
                continue
            
            stack.append(interval)

        return stack
```

test case
- [[1,3],[2,6],[8,10],[15,18]]
// init
stack = []
// i=0 stack = [[1,3]]

// i=1 stack = [[1,6]]
// i=2 stack = [[1,6],[8,10]]
// i=3 stack = [[1,6],[8,10],[15,18]] return

- [[1,4],[4,5]]
stack = []
// i=0 stack = [[1,4]]
// i=1 stack=[[1,5]]

- [[1,10],[2,3]]
- [[1,10]]

別の解法
Sweap Line（イベントベース）

Time: O(NlogN), Space: O(N)

```py
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        events = []
        for start, end in intervals:
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

### Follow Up

#### Insert Interval
マージ済み区間リストに新しい区間を挿入する問題。
[../insert-interval/]に解いた

#### 動的な区間管理（カレンダーアプリ等）
会議の追加・削除が頻繁に起きる場合、配列ベースはO(N)のシーケンシャルスキャンが毎回発生する。

平衡二分探索木（Balanced BST）を使うと挿入・削除・近傍探索がO(log N)になる。

- AVL木: 左右の部分木の高さの差（バランス因子）を±1以内に保つ。厳密なバランスで検索が速い 
- 赤黒木: ノードに赤・黒の色をつけてバランスを保つ。回転回数が少なく挿入・削除が速い。JavaのTreeMap、C++のstd::mapの内部実装 - Pythonでは標準ライブラリに平衡BSTがないため `sortedcontainers.SortedList` がよく使われる