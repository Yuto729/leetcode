11. Container With Most Water
You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the container contains the most water.
Return the maximum amount of water a container can store.
Notice that you may not slant the container.

Example1:
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.

Example 2:
Input: height = [1,1]
Output: 1
Constraints:
- n == height.length
- 2 <= n <= 10^5
- 0 <= height[i] <= 10^4

Approach

わからない....
Two Pointerらしいというヒントを見て思いついた

```py
class Solution:
    def maxArea(self, height: List[int]) -> int:
        left = 0
        right = len(height) - 1
        max_area = 0
        while left < right:
            # [left, right]が範囲
            if height[left] < height[right]:
                max_area = max(max_area, height[left] * (right - left))
                left += 1
            else:
                max_area = max(max_area, height[right] * (right - left))
                right -= 1
        
        return max_area
```

インデックスrightを順番に舐めるとして、各rightに対して`height[left] >= height[right]`を満たす最も左のleftを見つけて`(right - left) * height[right]`を計算する。対称に各leftについて、`height[right] >= height[left]`を満たす最も右のrightを見つけて`(right - left) * height[left]`を計算。両者の最大を取るという方法が思いついた。こっちの方が素直そう

単調スタック+二分探索で実装できるらしい
- 自分より大きい最も端にあるインデックスを見つけるためにあらかじめ記録配列を作っておくことを考える
- 記録配列は左（または右）から見ていって単調増加になる部分列にすれば良い。途中の減少する部分は見なくても目的とする値が見つかる。例：[1,8,6,2,5,4,8,3,7]について、今5の位置にいるとして左部分を探す。この時6とかは見なくて良い。なぜなら6より左に6より大きい8があるから。よって、索引となる配列は、`prefix_max = [1,8]`とすれば良い

定式化すると、ある`i`が`prefix max`を更新しない時、iより左に`height[j] >= height[i]`となる`j`が存在する。最適な`left`候補として`i`を考えても`j`の方が「より左」かつ「同等以上の高さ」なので`j`の方が良いので、iは見なくて良い

`prefix_max`に対して、「right以上である一番左のインデックス」を求めるには, `prefix max`の中で、高さが`height[right]`以上となる最初の要素を二分探索すれば良い。Pythonであれば`bisect_left`でかける

Time: O(Nlog N)
```py
class Solution:
    def maxArea(self, height: List[int]) -> int:
        n = len(height)
        max_area = 0
        left_prefix_max_indices = []
        right_prefix_max_indices = []
        for i in range(n):
            if not left_prefix_max_indices or height[i] > height[left_prefix_max_indices[-1]]:
                left_prefix_max_indices.append(i)
            
            left = bisect_left(left_prefix_max_indices, height[i], key=lambda x: height[x])
            if left < len(left_prefix_max_indices):
                max_area = max(max_area, (i - left_prefix_max_indices[left]) * height[i])
        for i in range(n - 1, - 1, -1):
            if not right_prefix_max_indices or height[i] > height[right_prefix_max_indices[-1]]:
                right_prefix_max_indices.append(i)
            
            right = bisect_left(right_prefix_max_indices, height[i], key=lambda x: height[x])
            if right < len(right_prefix_max_indices):
                max_area = max(max_area, (right_prefix_max_indices[right] - i) * height[i])
            
        return max_area
```

リファクタリングする
```py
class Solution:
    def max_area_with_shorter_wall_on_right(self, height):
        left_wall_candidates = []
        max_area = 0
        for right_wall, h in enumerate(height):
            if not left_wall_candidates or h > height[left_wall_candidates[-1]]:
                left_wall_candidates.append(right_wall)
            pos = bisect_left(left_wall_candidates, h, key=lambda x: height[x])
            left_wall = left_wall_candidates[pos]
            max_area = max(max_area, (right_wall - left_wall) * h)
    
        return max_area

    def maxArea(self, height: List[int]) -> int:
        # 「右側が低い壁」のケースと「左側が低い壁」のケースを両方カバーする
        return max(self.max_area_with_shorter_wall_on_right(height), self.max_area_with_shorter_wall_on_right(height[::-1]))
```
上記の解法は、「どちらかの壁を固定したときの最適なもう片方の壁」を陽に求めていく分割統治法的な発想なのに対し、
Two Pointer解法は、「今の壁のペアより良くなりうるのはどっち側を動かしたときか？」を貪欲に考えていく。これは局所的な単調性（捨てても損しない方向がある）からできる貪欲法である。-> 交換論法(exchange argument)が成り立ってるはず。
つまり、最適解の中の違う選択を貪欲解の選択に置き換えて悪化しないなら貪欲は正しい。

また、本問題は高さと横幅という２つの可変な要素があるため、積を最適化しようと考えると難しい。両端にポインタを置いて狭めていくことで横幅について単調減少する方向に探索できるようになる。

幅ではなく、高さについて単調な方向に探索する方法がある。
- 高さを降順にし、そのインデックスを走査する
- その時点で見ている位置の壁が低い方の壁となるので、containerの縦の長さは固定できる。あとは今まで見た中で一番小さいインデックスと一番大きいインデックスがわかればmax_areaを計算できる

他の解法
- 高さの降順ソート: O(N log N) time, O(N) space。高さの降順で処理することで「今見ている壁が低い方の壁」と確定でき、既に見たインデックスの min/max との距離だけで面積が計算できる。

```py
class Solution:
    def maxArea(self, height: List[int]) -> int:
        indices_by_height_desc = sorted(range(len(height)), key=lambda i: -height[i])
        min_seen, max_seen = float('inf'), float('-inf')
        max_area = 0
        for i in indices_by_height_desc:
            if min_seen != float('inf'):
                width = max(i - min_seen, max_seen - i)
                max_area = max(max_area, width * height[i])
            min_seen = min(min_seen, i)
            max_seen = max(max_seen, i)
        return max_area
```

- セグメント木: O(N log N) time, O(N) space。各区間の高さの最大値を持ち、「区間内で値 >= threshold となる最左 index」を降下クエリで求める。降下クエリは「左部分木の max が threshold 以上なら左に潜る、なければ右」という意思決定で O(log N)。
オフラインの本問題では Two Pointer に明確に劣るが、heightが後から追加されるオンライン設定では単一点更新 O(log N) で対応できるため第一選択になりうる。

```py
class SegmentTree:
    """各区間の高さの最大値を保持し、'値 >= threshold となる最左 index' をサポート"""

    def __init__(self, values: List[int]):
        self.n = len(values)
        self.tree = [0] * (4 * self.n)
        self._build(values, 1, 0, self.n - 1)

    def _build(self, values, node, lo, hi):
        if lo == hi:
            self.tree[node] = values[lo]
            return
        mid = (lo + hi) // 2
        self._build(values, 2 * node, lo, mid)
        self._build(values, 2 * node + 1, mid + 1, hi)
        self.tree[node] = max(self.tree[2 * node], self.tree[2 * node + 1])

    def leftmost_at_least(self, query_lo: int, query_hi: int, threshold: int) -> int:
        return self._descend(1, 0, self.n - 1, query_lo, query_hi, threshold)

    def _descend(self, node, lo, hi, query_lo, query_hi, threshold):
        if hi < query_lo or lo > query_hi or self.tree[node] < threshold:
            return -1
        if lo == hi:
            return lo
        mid = (lo + hi) // 2
        left_result = self._descend(2 * node, lo, mid, query_lo, query_hi, threshold)
        if left_result != -1:
            return left_result
        return self._descend(2 * node + 1, mid + 1, hi, query_lo, query_hi, threshold)


class Solution:
    def maxArea(self, height: List[int]) -> int:
        n = len(height)
        max_area = 0

        tree = SegmentTree(height)
        for right_wall in range(1, n):
            left_wall = tree.leftmost_at_least(0, right_wall - 1, height[right_wall])
            if left_wall != -1:
                max_area = max(max_area, (right_wall - left_wall) * height[right_wall])

        # 対称: 反転して同じ処理で「左側が低い壁」のケースをカバー
        reversed_height = height[::-1]
        reversed_tree = SegmentTree(reversed_height)
        for right_wall in range(1, n):
            left_wall = reversed_tree.leftmost_at_least(0, right_wall - 1, reversed_height[right_wall])
            if left_wall != -1:
                max_area = max(max_area, (right_wall - left_wall) * reversed_height[right_wall])

        return max_area
```


## 練習
```py


```