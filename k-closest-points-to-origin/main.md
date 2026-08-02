973. K Closest Points to Origin

Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane and an integer k, return the k closest points to the origin (0, 0).
The distance between two points on the X-Y plane is the Euclidean distance (i.e., √(x1 - x2)2 + (y1 - y2)2).

You may return the answer in any order. The answer is guaranteed to be unique (except for the order that it is in).

Example 1:
Input: points = [[1,3],[-2,2]], k = 1
Output: [[-2,2]]
Explanation:
The distance between (1, 3) and the origin is sqrt(10).
The distance between (-2, 2) and the origin is sqrt(8).
Since sqrt(8) < sqrt(10), (-2, 2) is closer to the origin.
We only want the closest k = 1 points from the origin, so the answer is just [[-2,2]].

Example 2:
Input: points = [[3,3],[5,-1],[-2,4]], k = 2
Output: [[3,3],[-2,4]]
Explanation: The answer [[-2,4],[3,3]] would also be accepted.

## Step1

原点から近い座標をkを持っておけば良いのでヒープが使える。距離に`-`をかけたものをキーとしてヒープに格納し、長さがkを超えたらpopする。最終的にヒープに残っている要素が答えとなる

時間計算量: O(nlog k)
空間計算量: O(k)

```py
class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        if not points:
            return []

        k_closest_points = []
        for point in points:
            x, y = point[0], point[1]
            heapq.heappush(k_closest_points, ((- (x ** 2 + y ** 2), x, y)))
            if len(k_closest_points) > k:
                heapq.heappop(k_closest_points)

        return [[elem[1], elem[2]] for elem in k_closest_points]
```

test
Input: points = [[3,3],[5,-1],[-2,4]], k = 2

// heap=[(-18,3,3)]
// .. = [(-18,3,3),(-26,5,-1)]
// .. = [(-18,3,3),(-26,5,-1),(-20,-2,4)]
len>2 -> pop (-26...)
heap = [(-18,3,3),(-20,-2,4)]
return

other test case

- [[0,0],[1,1]], k=1 キーが0になるケース
- [[3,3],[5,-1],[-2,4]], k = 3 1回もpopしない
- [[3,3],[3,3]], k=1 キーが同じ
- [[0,0]], k=1

### follow up

- 平均計算量をO(n)にできるか？
  quick selectを使う（書き方を覚えていないので見ながらトレースする）
  partitionをランダムに決める。partitionの左側（pivot含む）に何個の要素があるか見る。要素の数 m が、

1. m > kのとき -> 答えは左側だけにあるので左側に対してさらにquick select
2. m = kのとき -> 答え
3. m < kのとき -> 左側にあるものは決定で、右側から k - m 個残りを探すためにquick select

最悪計算量: O(n^2)

```py
class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        if not points:
            return []

        def calc_distance_squared(point):
            return point[0] ** 2 + point[1] ** 2

        pivot = random.randint(0, len(points) - 1)
        closer = []
        equal = []
        farther = []
        pivot_distance = calc_distance_squared(points[pivot])
        for point in points:
            distance = calc_distance_squared(point)
            if distance <= pivot_distance:
                closer.append(point)
            else:
                farther.append(point)

        if len(closer) > k:
            return self.kClosest(closer, k)

        elif len(closer) == k:
            return closer

```

上記のコードは、最大距離の点がpivotとして選択され続けると無限再帰が発生してしまう。乱数を振っているので確率的に無限再帰が発生する可能性は限りなく低いが、動作が決定的に保証されているわけではない。
また、Leetcodeのテストケースにはなかったが、以下のような例で無限再帰が発生する。

- [[0,1],[1,0],[0,-1],[-1,0]], k=2 全点同距離かつk < len(points)

以下のように`closer`, `equal`, `farther`に分けると、`closer`と`farther`の長さが毎ステップ縮むことが保証されるので、必ず収束する.

```py
class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        if not points:
            return []

        def calc_distance_squared(point):
            return point[0] ** 2 + point[1] ** 2

        pivot = random.randint(0, len(points) - 1)
        closer = []
        equal = []
        farther = []
        pivot_distance = calc_distance_squared(points[pivot])
        for point in points:
            distance = calc_distance_squared(point)
            if distance == pivot_distance:
                equal.append(point)
            elif distance < pivot_distance:
                closer.append(point)
            else:
                farther.append(point)

        if len(closer) >= k:
            return self.kClosest(left, k)

        if len(closer) + len(equal) >= k:
            return closer + equal[:k - len(closer)]

        return closer + equal + self.kClosest(farther, k - len(closer) - len(equal))
```

pointsをin-placeで並び替えて計算するバージョン

```py
class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        def dist(i):
            x, y = points[i]
            return x * x + y * y

        def partition(left, right):
            pivot_index = random.randint(left, right)
            pivot_dist = dist(pivot_index)
            points[pivot_index], points[right] = points[right], points[pivot_index]

            store = left
            for i in range(left, right):
                # storeより前は、pivot_distより距離が近い座標の集合
                if dist(i) < pivot_dist:
                    points[store], points[i] = points[i], points[store]
                    store += 1

            # 退避していたpivotを戻す
            points[store], points[right] = points[right], points[store]
            return store

        left, right = 0, len(points) - 1
        target = k - 1
        while left <= right:
            pivot_index = partition(left, right)
            if pivot_index == target:
                break

            if pivot_index < target:
                left = pivot_index + 1
            else:
                right = pivot_index - 1

        return points[:k]
```

pivotは以下のように3つの値の中央値から選ぶ方法もある

```py
def median_of_three(left, right):
    mid = (left + right) // 2
    a, b, c = dist(left), dist(mid), dist(right)
    if a <= b <= c or c <= b <= a:
        return mid
    if b <= a <= c or c <= a <= b:
        return left
    return right
```

## Step2

### 距離にマイナスをかけている意図はコメントで補足する

[huyfififi#28](https://github.com/huyfififi/coding-challenges/pull/28#discussion_r2236756647)

> 距離にマイナスがかかっていることが自明ではないため、コメントで補足するちょいと思いました。

自分のStep1コードでもキーに `-(x**2+y**2)` を使っているので、`# max-heapにするためマイナスをかける` のような一言があると良さそう

### quick select でin-place破壊するのは「関数として気持ち悪い」

[tom4649#123](https://github.com/tom4649/Coding/pull/123#discussion_r2156835310)

> このアルゴリズムは練習・選択肢の幅としてはよいと思いますが、副作用が「常に完全にpointsをソートするわけではなく、この問題において必要な範囲のみpointsを並び替える」という内容なので、pointsが使い捨ての想定でなければかなり関数として気持ち悪いとは思います。（…）関数としてのこの問題の想定解は長さkのheapを使うものかなという気がします。

「引数で受け取った `points` を中途半端に並び替えて返す」という副作用は、呼び出し側からしたら気持ちが悪い（確かに）

### `heappushpop` / `heapreplace` で操作を1回にまとめる

[huyfififi#28 memo](https://github.com/huyfififi/coding-challenges/pull/28) / [kitano-kazuki#94](https://github.com/kitano-kazuki/leetcode/pull/94)

自分が書いた解法は、`heappush` → `if len > k: heappop` と2操作だが、

- `heapq.heappushpop(heap, item)`: push してから最小要素をpop (sift downが1回)
- `heapq.heapreplace(heap, item)`: pop してから 根があった位置にpushする

を使うと heap の再構成が1回で済む。[ドキュメント](https://docs.python.org/3/library/heapq.html#heapq.heappushpop)にもより効率的との記述がある

さらに「新しい距離が現在の最遠 `heap[0]` 以上なら何もしない」早期スキップを入れると、無駄な heap 操作を減らせる。

```python
if len(topk) < k:
    heapq.heappush(topk, (-distance, point))
elif distance < abs(topk[0][0]):   # 既存の最遠より近いときだけ
    heapq.heapreplace(topk, (-distance, point))
```

## Step3

quick selectの練習
`if dist(i) < pivot_dist`部分は、`<=`にしても正解

```py
class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        def dist(i):
            x, y = points[i]
            return x * x + y * y

        def partition(left, right):
            pivot_index = random.randint(left, right)
            pivot_dist = dist(pivot_index)
            points[pivot_index], points[right] = points[right], points[pivot_index]

            store = left
            for i in range(left, right):
                if dist(i) < pivot_dist:
                    points[store], points[i] = points[i], points[store]
                    store += 1

            points[store], points[right] = points[right], points[store]
            return store

        left, right = 0, len(points) - 1
        target = k - 1
        while left <= right:
            pivot_index = partition(left, right)
            if pivot_index == target:
                break

            if pivot_index < target:
                left = pivot_index + 1
            else:
                right = pivot_index - 1

        return points[:k]
```

## 過去に解いた類題

- [kth-largest-element-in-a-stream](../kth-largest-element-in-a-stream/) — k個をheapで保持する発想がそのまま共通。3つのPR全てでこの問題が参照されている
- [top-k-frequent-elements](../top-k-frequent-elements/) — heap / quick select 両方が使える「top-k」典型問題
- [find-k-pairs-with-smallest-sums](../find-k-pairs-with-smallest-sums/) — k番目までを取り出す、和の小さい順という構造が近い
- [median-of-two-sorted-arrays](../median-of-two-sorted-arrays/) — partition / 第k要素を探す発想の親戚
