# 169. Majority Element
Given an array nums of size n, return the majority element.

The majority element is the element that appears more than ⌊n / 2⌋ times. You may assume that the majority element always exists in the array.

Example 1:
Input: nums = [3,2,3]
Output: 3

Example 2:
Input: nums = [2,2,1,1,1,2,2]
Output: 2

Constraints:
- n == nums.length
- 1 <= n <= 5 * 10^4
- -10^9 <= nums[i] <= 10^9
- The input is generated such that a majority element will exist in the array.

## 回答

HashMapで各要素の出現回数を数え、n//2を超えるものを返す。time O(n), space O(n)。
```py
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        n = len(nums)
        condition = n // 2
        num_to_count = defaultdict(int)
        for num in nums:
            num_to_count[num] += 1
        
        for num, count in num_to_count.items():
            if count > condition:
                return num
        
        return -1
```

上と同じ方針だが、カウントがn//2を超えた時点で即リターンする早期終了版。
```py
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        n = len(nums)
        condition = n // 2
        num_to_count = defaultdict(int)
        for num in nums:
            num_to_count[num] += 1
            if num_to_count[num] > condition:
                return num
  
        return -1
```

## Follow Up

### space O(1)で解けるか？
方法その1。ソートして連続する同じ要素を数える。time O(n log n), space O(1)（nums.sort()はin-placeなので入力を破壊する）。
```py
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        n = len(nums)
        nums.sort()
        current_num_freq = 1
        for i in range(n):
            if i > 0 and nums[i] == nums[i - 1]:
                current_num_freq += 1
            else:
                current_num_freq = 1

            if current_num_freq > n // 2:
                return nums[i]

        return -1
```

majority elementの出現回数はn//2より大きいため、ソート後は必ず配列の中央index（n//2）を占める。上のループは不要。
```py
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        n = len(nums)
        nums.sort()
        current_num_freq = 1
        return nums[n // 2]
```

方法その2: Boyer-Moore Voting Algorithm。
各要素を異なる国の兵士と見なし、１つの陣地を取り合う。陣地が空いているとき、新しくきた兵士の属する国の陣地とすることができる。陣地が空いておらず、次の兵士が来た場合、同じ国であれば兵士数が増え、異なる国であれば1対1で相打ちにする。陣地の兵士数が１人減る。兵士数が0人になったとき、陣地が解放される。
最後に陣地を持っている国は、全兵士の過半数を有していた国となり、それが答え。

majority elementはそれ以外の全要素の合計より多く出現するため、相殺しきれずに最後まで残る。
candidateが空のとき（count==0）は次の要素を新しい候補に立て、同じなら+1、違えば-1する。

time O(n), space O(1)。
```py
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        n = len(nums)
        candidate = None
        count = 0
        for num in nums:
            if count == 0:
                candidate = num
            if num == candidate:
                count += 1
            else:
                count -= 1

        return candidate
```


### Majority Element II
> Given an integer array of size n, find all elements that appear more than ⌊ n/3 ⌋ times.

Majority Element 2（n//3超えを全て返す）へのBoyer-Moore拡張。
n//3超えの要素は最大2個しか存在できない（3個あると合計がnを超える）ため、候補を2つ持つ。

同じように戦場の例えで考えることができる。２つの陣地が存在し、陣地が空いていればその陣地を占領できる。1つの国は１つの陣地しか占領できない。
陣地が空いておらず、新しい国の兵士が来た場合、つまり3つの国の兵士が集まった場合は3者同時に相打ちになり、それぞれの陣地から兵士が１人ずつ消える。新しく来た兵士が陣地のどちらかの国に属する場合、その陣地の兵士数が増える。

条件分岐の順番は「既存の陣地の確認を先、空き地の確認を後」にする必要がある。
順番が逆になると、すでに陣地を持っている国の兵士が来たとき、空き地を見て別の陣地を新たに作ってしまう（candidate1をnumで上書きする）。
1つの国が2つの陣地を持つことになり、例えと矛盾する。

ループ後に候補が実際にn//3超えているか検証が必要。戦場の生き残りが本当の多数派とは限らないため。

```py
class Solution:
    def majorityElement(self, nums: List[int]) -> List[int]:
        n = len(nums)
        candidate1 = None
        candidate2 = None
        count1 = 0
        count2 = 0
        for num in nums:
            if candidate1 == num:
                count1 += 1
            elif candidate2 == num:
                count2 += 1
            elif count1 == 0:
                candidate1, count1 = num, 1        
            elif count2 == 0:
                candidate2, count2 = num, 1
            else:
                count1 -= 1
                count2 -= 1
        
        result = []
        for c in [candidate1, candidate2]:
            if c is not None and nums.count(c) > len(nums) // 3:
                result.append(c)
        
        return result
```


## Step2

### Quick Select

[huyfififi#19](https://github.com/huyfififi/coding-challenges/pull/19)

> Quickselectで`n // 2`番目に小さい数を見つけるなら、Quickselectもあるな、と記憶に残っていた。しかし、実際に調べながら実装して走らせてみると、Time Limit Exceededとなった。入力Arrayの数字が全て同じであった場合、範囲の分割が効率的に行われない（1つずつしか範囲が削られない）ため、時間計算量がO(n^2)かかってしまう。

QuickSelectはk番目に小さい要素をO(n)で見つけるアルゴリズム。k番目を探したい時、pivotが確定した位置を見て、
- pivotのindex == k -> 答え
- pivotのindex > k -> 左側だけ再帰
- pivotのindex < k -> 右側だけ再帰

```py
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        def quickselect(nums: list[int], left: int, right: int, k: int) -> int:
            if left == right:
                return nums[left]

            pivot_index = random.randint(left, right)
            pivot_value = nums[pivot_index]
            store_index = left
            nums[right], nums[pivot_index] = nums[pivot_index], nums[right]
            for i in range(left, right):
                if nums[i] < pivot_value:
                    nums[i], nums[store_index] = nums[store_index], nums[i]
                    store_index += 1
            nums[store_index], nums[right] = nums[right], nums[store_index]

            if store_index == k:
                return nums[store_index]
            elif store_index < k:
                return quickselect(nums, store_index + 1, right, k)
            else:
                return quickselect(nums, left, store_index - 1, k)

        return quickselect(nums, 0, len(nums) - 1, len(nums) // 2)
```

### ソートアプローチのPythonの空間計算量

[huyfififi#19](https://github.com/huyfififi/coding-challenges/pull/19)

> Pythonのソートアルゴリズムはinsertion sortとmerge sortを組み合わせたTimsortで、best case(入力が既にソートされている)の時の時間計算量はinsertion sortのO(n)。average/worst caseでmerge sortのO(nlogn)。空間計算量: O(n), best case時はinsertion sortのO(1)、そうでない場合はmerge sortのO(n)。

`nums.sort()`はin-placeだが内部的にはTimsort（insertion sort + merge sort）を使うため、merge sortのパスでは一時配列にO(n)の空間を使うらしい。

挿入ソートについて忘れていたので書いてみる。
```py
def insertion_sort(arr):
    for i in range(1, len(arr)):
        target = arr[i]
        j = i - 1
        # jはソート済み部分の末尾
        while j >= 0 and arr[j] > target:
            arr[j + 1] = arr[j]
            j -= 1
        # jは、arr[j] <= targetとなる初めてのj。 よってj + 1にtargetを挿入する
        arr[j + 1] = target
    return arr
```
- [3,1,4,2]でトレース

### Boyer-Mooreはソフトウェアエンジニアの常識には含まれる？

[rihib#37](https://github.com/rihib/leetcode/pull/37) -> [コメント](https://github.com/rihib/leetcode/pull/37/files#r1770000000)

> こちらはソフトウェアエンジニアの常識には含まれないと思います。

[huyfififi#19](https://github.com/huyfififi/coding-challenges/pull/19)

> 常識には含まれないが、GoogleのSWEの中では知っている方が多いらしい

### Heapを使ったアプローチ

[huyfififi#19](https://github.com/huyfififi/coding-challenges/pull/19)

> `n // 2 + 1`番目に大きい数が答えであることを利用する。[703. Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/description/)の解法で`k = (n // 2) + 1`とすれば答えが求まる。

min-heapで常にサイズ`n//2 + 1`を保ちながら走査し、最後のheap topが答えになるという解法。time O(n log n), space O(n)


## Step3
```py
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        n = len(nums)
        candidate = None
        count = 0
        for num in nums:
            if count == 0:
                candidate = num
            if num == candidate:
                count += 1
            else:
                count -= 1

        return candidate
```

### 類題

- [kth-largest-element-in-a-stream](../kth-largest-element-in-a-stream/)
- [top-k-frequent-elements](../top-k-frequent-elements/)