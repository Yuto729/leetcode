---
date: 2026-08-01
tags:
  - leetcode
  - review
---

# Sort Colors

Given an array nums with n objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue.

We will use the integers 0, 1, and 2 to represent the color red, white, and blue, respectively.

You must solve this problem without using the library's sort function.

Example 1:
Input: nums = [2,0,2,1,1,0]
Output: [0,0,1,1,2,2]

Example 2:
Input: nums = [2,0,1]
Output: [0,1,2]

- numsが0 -> 1 -> 2の順になるように並び替える。同じ色が隣同士になるようにする
- 普通のソートアルゴリズムを使うか、0,1,2だけなので特別な方法でやるか
  - in-placeなので追加の配列を使うことは想定されていない？
- in-placeで効率的なソートで言えば、クイックソートを思いつく。数字が限られているので本解ではなさそうだが、実装してみる
  - クイックソートのin-place版を普通に忘れていて書けなかった...
- 別の方法
  - 一旦ナイーブなソートで書いてみる
  - 選択ソート
  - バブルソートなど

### 実装1

選択ソート
Time: O(N^2)
Space: O(1)

```py
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        for i in range(len(nums)):
            min_index = i
            for j in range(i + 1, len(nums)):
                if nums[j] < nums[min_index]:
                    min_index = j
            nums[i], nums[min_index] = nums[min_index], nums[i]
```

- 制約がゆるいのでこれでもそこそこの実行時間でAcceptしたので一旦ok

- ヒントの1個目を見てカウンティングソートを思い出す
  - なるほど、固定長のスペースならin-placeのうちに入るのか

### 実装2

カウンティングソート
Time: O(N)
Space: O(1)

```py
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        frequency_count = [0] * 3
        for num in nums:
            frequency_count[num] += 1

        start = 0
        for i, freq in enumerate(frequency_count):
            nums[start: start + freq] = [i] * freq
            start += freq
```

- 3がマジックナンバー。RED, WHITE, BLUE, NUM_COLORSで定数をおいた方が良さそう
- `[i] * freq`で毎回リストを作成しているのがin-placeと整合するのかという指摘
  - 代入ループにする

### 実装2 改善

```py
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        NUM_COLORS = 3
        counts = [0] * NUM_COLORS
        for num in nums:
            counts[num] += 1

        index = 0
        for color, count in enumerate(counts):
            for _ in range(count):
                nums[index] = color
                index += 1
```

- クイックソートが途中までしか書けなかったので完成させるが、0,1,2だけに値が限定されているので工夫して簡単にする

### 実装3 途中まで

```py
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        Do not return anything, modify nums in-place instead.
        def get_pivot(nums):
            first = nums[0]
            last = nums[-1]
            median = (nums[len(nums) // 2] + nums[len(nums) // 2 - 1]) // 2 if len
            return ...

        def swap(i, j, nums):
            nums[i], nums[j] = nums[j], nums[i]
        pivot_index = get_pivot(nums)
        partition = pivot_index
        while 0 < partition < len(nums):
            pivot = nums[pivot_index]
            swap(pivot_index, -1, nums)
            partition = 0
            for i in range(len(nums) - 1):
                if nums[i] <= pivot:
                    swap(first_index_more_than_pivot, i, nums)
                    first_index_more_than_pivot += 1

            swap(first_index_more_than_pivot, -1, nums)
            pivot_index = get_pivot(nums)
```

### 実装3

2-passでいけた。1-passでいけるのかこれ

```py
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        RED = 0
        WHITE = 1
        BLUE = 2
        def sort_by_partition(pivot):
            first_index_more_than_pivot = 0
            for i in range(len(nums)):
                if nums[i] <= pivot:
                    nums[i], nums[first_index_more_than_pivot] = nums[first_index_more_than_pivot], nums[i]
                    first_index_more_than_pivot += 1

        sort_by_partition(WHITE)
        sort_by_partition(RED)
```

### 実装4

1-passかつO(1)の解法

クイックソートをそのまま実装するのはオーバースペックだと思うが、簡単なやり方がわからない。ヒントをもらいつつ進める

> いま2パスなのは、「0を前に寄せる仕事」と「2を後ろに送る仕事」を別々のループでやっているからです。1パスにしたいなら、この2つを1回の走査の中で同時にやることになります。
> そのために不変条件を考えます。走査位置を i として、配列を4区間に割ります:

```
[0が確定][1が確定][未確定][2が確定]
                  i
```

- 未確定領域の先頭 `nums[i]` の値によって場合分けをする
  - 1のとき -> 1の確定領域と繋がるのでそのままで良い
  - 2のとき -> 未確定領域の末尾と入れ替える
    - このとき, iを進めてしまうと入れ替え後の`nums[i]`の位置がまだ未確定なのに判定されなくなってしまう

  - 0のとき -> 1の確定領域の先頭と入れ替える

- `i`が未確定領域の末尾を超えたら未確定区間が空になって終了
- 初期状態がわかりにくいが、与えられた配列に仮想的に「確定済みの0,1,2」を差し込んで考えるとわかりやすい
  - nums = [2,0,2,1,1,0]を例とする
  - 補完してみると、`(0,0)(1,1),2,0,2,1,1,0,(2,2)` ()で囲まれたところは仮想的に配置したもの

以下のように変数を置く

- `red_end = 0` 赤領域の排他的な終端, 次に赤を置く位置
  - 排他的とは領域には含まないということ。赤の終端かつ白の始まり
  - nums[:red_end] -> 赤, nums[red_end:i] -> 白

- `blue_start = len(nums)` 青が始まる位置。初めは配列外にとっておく
- 上記は半開区間。基本的に半開区間でとっておくと、自然に書ける

nums = [2,0,2,1,1,0]。赤[] 白[] 未[] 青[] の4領域

初期 red_end=0 i=0 blue_start=6
赤[] 白[] 未[2,0,2,1,1,0] 青[]

i=0: 2 → blue_start を 5 に下げて nums[0] と nums[5] を交換。i は進めない
red_end=0 i=0 blue_start=5
赤[] 白[] 未[0,0,2,1,1] 青[2]

i=0: 0 → nums[0] と nums[red_end=0] を交換（自分自身）。red_end=1, i=1
red_end=1 i=1 blue_start=5
赤[0] 白[] 未[0,2,1,1] 青[2]

i=1: 0 → nums[1] と nums[red_end=1] を交換（自分自身）。red_end=2, i=2
red_end=2 i=2 blue_start=5
赤[0,0] 白[] 未[2,1,1] 青[2]

i=2: 2 → blue_start を 4 に下げて nums[2] と nums[4] を交換。i は進めない
red_end=2 i=2 blue_start=4
赤[0,0] 白[] 未[1,1] 青[2,2]

i=2: 1 → 何もせず i=3
red_end=2 i=3 blue_start=4
赤[0,0] 白[1] 未[1] 青[2,2]

i=3: 1 → 何もせず i=4
red_end=2 i=4 blue_start=4
赤[0,0] 白[1,1] 未[] 青[2,2]

これで全部確定済みなので終了 -> [0,0,1,1,2,2]となる

```py
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        # nums[:red_end] == RED, nums[red_end:i] == WHITE,
        # nums[i:blue_start] は未確定, nums[blue_start:] == BLUE
        red_end = 0
        blue_start = len(nums)
        i = 0
        while i < blue_start:
            if nums[i] == BLUE:
                blue_start -= 1
                nums[i], nums[blue_start] = nums[blue_start], nums[i]
                # 受け取った値は未確定なので i は進めない
                continue
            if nums[i] == RED:
                nums[i], nums[red_end] = nums[red_end], nums[i]
                red_end += 1
            i += 1
```

- 開区間にするとこんな感じ

```py
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        # nums[:last_red_index + 1] == RED, nums[last_red_index + 1:i] == WHITE
        RED = 0
        WHITE = 1
        BLUE = 2

        last_red_index = -1
        first_blue_index = len(nums)
        i = 0
        while i < first_blue_index:
            if nums[i] == BLUE:
                first_blue_index -= 1
                nums[i], nums[first_blue_index] = nums[first_blue_index], nums[i]
                continue

            if nums[i] == RED:
                last_red_index += 1
                nums[i], nums[last_red_index] = nums[last_red_index], nums[i]

            i += 1
```

- [0が確定][1が確定][2が確定][未確定]]
  - ちなみにこの領域の分割の仕方でもいける。
  - この場合ちょっとめんどくさい

```py
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        RED = 0
        WHITE = 1
        BLUE = 2

        red_end = 0
        white_end = 0
        i = 0
        while i < len(nums):
            if nums[i] == RED:
                # 赤を置くとき、白のブロックを右へずらさないと、nums[red_end: white_end] = 白の領域 の不変条件が壊れうる。 ex. [2,0,1]
                nums[i], nums[white_end] = nums[white_end], nums[i]
                nums[white_end], nums[red_end] = nums[red_end], nums[white_end]
                red_end += 1
                white_end += 1
            elif nums[i] == WHITE:
                nums[i], nums[white_end] = nums[white_end], nums[i]
                white_end += 1
            i += 1
```

### クイックソート（in place）

```py
def quick_sort(arr, low, high):
    if low >= high:
        return

    pivot_index = high
    first_index_more_than_pivot = high - 1
    for i in range(low, high):
        if arr[i] > arr[pivot_index]:
            first_index_more_than_pivot -= 1
            arr[first_index_more_than_pivot], arr[i] = arr[i], pivot[first_index_more_than_pivot]
    arr[first_index_more_than_pivot], arr[high] = arr[high], arr[    first_index_more_than_pivot]

    pivot_index = first_index_more_than_pivot - 1
    quick_sort(arr, low, pivot_index)
    quick_sort(arr, pivot_index + 1, high)
```

Lomuto Partition

全て開区間で定義する

```py
def quicksort(nums, lo, hi):
    if hi - lo <= 1:
        return

    pivot_index = partition(nums, lo, hi)
    # pivotは確定済みなので除いてソートする
    quicksort(nums, lo, pivot_index) # nums[lo: pivot]をsort
    quicksort(nums, pivot_index + 1, hi) # nums[pivot + 1: hi]をsort

def partition(nums, lo, hi):
    pivot = nums[hi - 1]
    less_end = lo
    # nums[lo: less_end] < pivot, less_end=loで空集合
    # nums[less_end: i] >= pivot, 同じく
    # nums[i: hi - 1] 未確定
    # nums[hi - 1] == pivot
    for i in range(lo, hi - 1):
        if nums[i] < pivot:
            nums[i], nums[less_end] = nums[less_end], nums[i]
            less_end += 1
    nums[less_end], nums[hi - 1] = nums[hi - 1], nums[less_end]
    return less_end
```

閉区間バージョン

```py
def quicksort(nums, lo, hi):
    # nums[lo: hi + 1]をソート
    if hi <= lo:
        return

    pivot_index = partition(nums, lo, hi)
    quicksort(nums, lo, pivot_index - 1) # nums[lo: pivot]をsort
    quicksort(nums, pivot_index + 1, hi) # nums[pivot + 1: hi + 1]をsort

def partition(nums, lo, hi):
    pivot = nums[hi]
    less_end = lo - 1
    # nums[lo: less_end + 1] <= pivot, less_end=lo-1で空集合になるのでok
    # nums[less_end + 1: i] > pivot, less_end=lo-1で空集合になるのでok
    # nums[i: hi] 未確定
    # nums[hi] == pivot
    for i in range(lo, hi):
        if nums[i] <= pivot:
            less_end += 1
            nums[i], nums[less_end] = nums[less_end], nums[i]
    nums[less_end + 1], nums[hi] = nums[hi], nums[less_end + 1]
    return less_end + 1
```

## Step3

```
[  0確定  ][  1確定  ][  未確定  ][  2確定  ]
       red_end        i         blue_start
```

nums[:red_end] red確定済み
nums[red_end:i] white確定済み
nums[i:blue_start] 未確定
nums[blue_start] blue確定済み

- 初期値
  - red_end=0
  - blue_start=len(nums)
  - i=0

```py
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        RED = 0
        WHITE = 1
        BLUE = 2

        red_end = 0
        blue_start = len(nums)
        i = 0
        while i < blue_start:
            if nums[i] == BLUE:
                blue_start -= 1
                nums[i], nums[blue_start] = nums[blue_start], nums[i]
                continue

            if nums[i] == RED:
                nums[i], nums[red_end] = nums[red_end], nums[i]
                red_end += 1
            i += 1
```

### 関連

- [[ソートアルゴリズム]]
- [[move-zeroes/main|Move Zeroes]]
- [[remove-duplicates-from-sorted-list/main|Remove Duplicates from Sorted List]]
- [[next-permutation/main|Next Permutation]]
- [K Closest Points to Origin #81](https://github.com/Yuto729/leetcode/pull/81)
