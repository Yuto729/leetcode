# find-median-from-data-stream

The median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value, and the median is the mean of the two middle values.

For example, for arr = [2,3,4], the median is 3.
For example, for arr = [2,3], the median is (2 + 3) / 2 = 2.5.
Implement the MedianFinder class:

MedianFinder() initializes the MedianFinder object.
void addNum(int num) adds the integer num from the data stream to the data structure.
double findMedian() returns the median of all elements so far. Answers within 10-5 of the actual answer will be accepted.

Ex.
["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
[[], [1], [2], [], [3], []]

## Step1

まずはシンプルに毎回ソートする方法で実装する。ギリギリAcceptしたが最適解ではなさそう

addNum: O(nlogn)
findMedian: O(1)

```py
class MedianFinder:

    def __init__(self):
        self.store = []
        self.length = 0

    def addNum(self, num: int) -> None:
        self.store.append(num)
        self.store.sort()
        self.length += 1

    def findMedian(self) -> float:
        if self.length % 2 == 0:
            return (self.store[self.length // 2] + self.store[self.length // 2 - 1]) / 2

        return self.store[self.length // 2]
```

中央値
左の配列の最大値 <= 右の配列の最小値
を満たせばうまく分割できている。この状態を作る。2つのPQを使えばうまくできそうだと思ったが、その後がなかなか思いつかない

左の配列の最大値 <= 新しく入れる値 <= 右の配列の最小値の時は、どちらか小さい方に入れ、

左の配列より小さい時は左、右の配列より大きい時は右になるようにする。
左の配列の最大値と右の配列の最小値から中央値を計算すると、例えば以下のような例でうまくいく

add 1 -> left=[1]
add 5 -> left=[1] right=[5]
find -> 3
add 3 -> left=[1,3] right=[5]
find -> 3
add 6 -> left=[1,3] right=[5,6]
find -> 4

add 1
add -1
add -3
...
のような例では左の配列に偏ってしまいうまくいかない。

AIにヒントをもらう。2つのグループのサイズ差が1以下になるようにバランスを取れば良いとのこと

left -> small
right -> largeにする

ロジックが思いついてからAcceptするまでに40分ほどかかってしまった。

詰まったところ

- large, smallの取り違え
- heapq.heappush(self.small_pq, -min_of_large) # ここのマイナスミス

以下の不変条件を保つようにする

- 順序の不変条件: smallの要素は全てlargeの要素以下である
- サイズの不変条件: largeとsmallのサイズ差が1以内

addNum: O(logn)

```py
class MedianFinder:

    def __init__(self):
        self.small_pq = [] # 符号を反転させる
        self.large_pq = []

    def addNum(self, num: int) -> None:
        small_pq_length = len(self.small_pq)
        large_pq_length = len(self.large_pq)
        if not self.small_pq:
            heapq.heappush(self.small_pq, -num)
            return

        max_of_small = -self.small_pq[0]
        min_of_large = self.large_pq[0] if self.large_pq else -float('inf')
        if max_of_small <= num <= min_of_large:
            if small_pq_length <= large_pq_length:
                heapq.heappush(self.small_pq, -num)
            else:
                heapq.heappush(self.large_pq, num)
            return

        if num < max_of_small:
            # numはsmallに入れる
            if large_pq_length < small_pq_length:
                heapq.heappop(self.small_pq)
                heapq.heappush(self.large_pq, max_of_small)
            heapq.heappush(self.small_pq, -num)
            return
        # largeに入れる
        if small_pq_length < large_pq_length:
            heapq.heappop(self.large_pq)
            heapq.heappush(self.small_pq, -min_of_large)
        heapq.heappush(self.large_pq, num)
        return

    def findMedian(self) -> float:
        small_pq_length = len(self.small_pq)
        large_pq_length = len(self.large_pq)
        if small_pq_length > large_pq_length:
            return -self.small_pq[0]

        if small_pq_length < large_pq_length:
            return self.large_pq[0]

        return (-self.small_pq[0] + self.large_pq[0]) / 2
```

AI Review

- 分岐が多いのでもっとシンプルにできる

- 先にsmallもしくはlargeに入れ、後からサイズを調整するようにすると少しシンプルになる。
- smallかlargeが空のときは、smallに入れるように統一する。smallが空のときはsmall, largeが空のときはlargeというようにしてしまうと、「比較対象がないままlargeに入れて順序を壊す」というバグが発生してしまう。

```py
class MedianFinder:

    def __init__(self):
        self.small_pq = []
        self.large_pq = []

    def addNum(self, num: int) -> None:
        if self.large_pq and num > self.large_pq[0]:
            heapq.heappush(self.large_pq, num)
        else:
            heapq.heappush(self.small_pq, -num)

        # サイズの差が1より大きい時に調整する
        if len(self.small_pq) > len(self.large_pq) + 1:
            max_of_small = -heapq.heappop(self.small_pq)
            heapq.heappush(self.large_pq, max_of_small)
        if len(self.large_pq) > len(self.small_pq) + 1:
            min_of_large = heapq.heappop(self.large_pq)
            heapq.heappush(self.small_pq, -min_of_large)

    def findMedian(self) -> float:
        small_pq_length = len(self.small_pq)
        large_pq_length = len(self.large_pq)
        if small_pq_length > large_pq_length:
            return -self.small_pq[0]

        if small_pq_length < large_pq_length:
            return self.large_pq[0]

        return (-self.small_pq[0] + self.large_pq[0]) / 2
```

AIから教えてもらった簡略化法

1. とりあえずsmallに入れる
2. smallの最大値をlargeに移す
3. smallとlargeのサイズ差が1を超えたら、大きい方から小さい方へ1個移す

- 「smallの最大値 <= largeの最小値」の不変条件が保たれる理由

numがsmallの最大値以下の時は明らか、smallの最大値より大きい時はnumが新しいsmallの最大値となりlargeに移動するので、この場合も保たれる

- 2の操作が終わった時点で、1の操作前と比べてlargeのサイズだけが1増加するので、「largeのサイズ > smallのサイズ+1」になるかどうかだけチェックすれば良い。

- サイズに関する不変条件として、「smallのサイズ <= largeのサイズ」が`addNum`ごとに保たれるため、`findMedian`の分岐もシンプルになる

```py
class MedianFinder:

    def __init__(self):
        self.small_pq = [] # 符号を反転させる
        self.large_pq = []

    def addNum(self, num: int) -> None:
        # とりあえずsmallに入れる
        heapq.heappush(self.small_pq, -num)
        # smallの中の最大値をlargeの方に移す
        max_of_small = -heapq.heappop(self.small_pq)
        heapq.heappush(self.large_pq, max_of_small)
        if len(self.large_pq) > len(self.small_pq) + 1:
            # large -> smallに最小値を移す
            min_of_large = heapq.heappop(self.large_pq)
            heapq.heappush(self.small_pq, -min_of_large)

    def findMedian(self) -> float:
        if len(self.small_pq) < len(self.large_pq):
            return self.large_pq[0]

        return (-self.small_pq[0] + self.large_pq[0]) / 2
```

## Step2

- https://github.com/tom4649/Coding/pull/112/changes
  - step1 二分探索を用いる方法。一番最初に思いついたが、配列の途中に挿入する方法を忘れていてできなかった。`list.insert(index, element)`でできるのか。
  - step2 heap
    - lowの長さ >= highの長さ が常に成り立つようにしているので、分岐が少なくて済む

## Step3

```py
class MedianFinder:

    def __init__(self):
        self.small_pq = []
        self.large_pq = []

    def addNum(self, num: int) -> None:
        heapq.heappush_max(self.small_pq, num)
        max_of_small = heapq.heappop_max(self.small_pq)
        heapq.heappush(self.large_pq, max_of_small)
        if len(self.large_pq) > len(self.small_pq) + 1:
            min_of_large = heapq.heappop(self.large_pq)
            heapq.heappush_max(self.small_pq, min_of_large)

    def findMedian(self) -> float:
        if len(self.large_pq) a> len(self.small_pq):
            return self.large_pq[0]

        return (self.large_pq[0] + self.small_pq[0]) / 2
```
