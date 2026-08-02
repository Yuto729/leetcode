15. 3Sum
Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

Example 1:
Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
Explanation: 
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].
Notice that the order of the output and the order of the triplets does not matter.

Example 2:
Input: nums = [0,1,1]
Output: []
Explanation: The only possible triplet does not sum up to 0.

Example 3:
Input: nums = [0,0,0]
Output: [[0,0,0]]
Explanation: The only possible triplet sums up to 0.

Constraints:
- 3 <= nums.length <= 3000
- -10^5 <= nums[i] <= 10^5

## Step1
Two Sumに落とし込むと良さそう。配列を先頭から見ていって１つ要素を選び、それ以降で和が特定の値になるものをTwo Sumを用いて探してペアにする。そのままだと重複を避けるのが難しかったので、ソートをすることにした。

時間計算量: O(n^2)
空間計算量: O(n)
```py
class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        if not nums:
            return []
        
        n = len(nums)
        nums.sort()
        def two_sum_from(start, target):
            pairs = []
            added = set()
            seen_complement = set()
            for i in range(start, n):
                if nums[i] in added:
                    seen_complement.add(nums[i])
                    continue
                
                complement = target - nums[i]
                if complement in seen_complement:
                    pairs.append([complement, nums[i]])
                    added.add(nums[i])
                seen_complement.add(nums[i])
            
            return pairs
        
        result = []
        seen = set()
        for i in range(len(nums)):
            if nums[i] in seen:
                continue
            
            seen.add(nums[i])
            rest = two_sum_from(i + 1, -nums[i])
            for pair in rest:
                pair.append(nums[i])
                result.append(pair)
        
        return result
```

ソートしたということは、同じ値は連続しているので以下のように書き換えられる
```py
class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        if not nums:
            return []
        
        nums.sort()
        n = len(nums)
        def two_sum_from(start, target):
            pairs = []
            seen = set()
            i = start
            while i < len(nums):
                complement = target - nums[i]
                if complement in seen:
                    pairs.append([complement, nums[i]])
                    while i < len(nums) - 1 and nums[i] == nums[i + 1]:
                        i += 1

                seen.add(nums[i])
                i += 1
            
            return pairs
        
        result = []
        for i in range(len(nums)):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            
            for pair in two_sum_from(i + 1, -nums[i]):
                pair.append(nums[i])
                result.append(pair)
        
        return result
```

空間計算量がO(1)になるやり方があるので書いてみる
sort + two pointer
時間計算量: O(N^2)
空間計算量: O(1)
```py
class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        n = len(nums)
        nums.sort()
        result = []
        for i in range(n - 2):
            if nums[i] > 0:
                break
                
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            
            left, right = i + 1, n - 1
            while left < right:
                s = nums[i] + nums[left] + nums[right]
                if s == 0:
                    result.append([nums[i], nums[left], nums[right]])
                    right -= 1
                    left += 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1

                elif s > 0:
                    right -= 1
                else:
                    left += 1
        
        return result
```

### Follow Up
- K Sumに拡張

```py
class Solution:
    def kSum(self, nums: list[int], target: int, k: int) -> list[list[int]]:
        nums.sort()
        return self._kSum(nums, target, k, 0)
    
    def _kSum(self, nums, target, k, start):
        n = len(nums)
        if start >= n or nums[start] * k > target:
            return []
        
        if k == 2:
            return self._twoSum(nums, target, start)
        
        res = []
        for i in range(start, n - k + 1):
            if i > start and nums[i] == nums[i - 1]:
                continue
            
            for sub in self._kSum(nums, target - nums[i], k - 1, i + 1):
                res.append([nums[i]] + sub)
        
        return res
    
    def _twoSum(self, nums, target, start):
        res = []
        l, r = start, len(nums) - 1
        while l < r:
            s = nums[l] + nums[r]
            if s < target:
                l += 1
            elif s > target:
                r -= 1
            else:
                res.append([nums[l], nums[r]])
                l += 1
                r -= 1
                while l < r and nums[l] == nums[l - 1]:
                    l += 1
                while l < r and nums[r] == nums[r + 1]:
                    r -= 1
        
        return res
```

## Step2
### 入力配列を変更しない

[huyfififi#30](https://github.com/huyfififi/coding-challenges/pull/30) 

> 入力を変更している点が気になりました。呼び出し側の視点に立って考えると、関数に渡した値が勝手に書き換えられているとびっくりすると思います。入力は原則変更しないか、変更する場合は関数コメントでそれを明記することをおすすめします。

自分の回答も入力を変更してしまっていたので気をつける。変更する前提の呼び出し方ではないケースで注意

### 変数名: 不要な "current" を排除

[yamashita-ki#4](https://github.com/yamashita-ki/codingTest/pull/4)

> 一度に着目しているsumはこの変数だけなので、現在着目しているという意図であれば、"current" は情報を追加せず不要かと思います。

ループ内で一つしかないものに `current_` を付けても情報量が増えない。シンプルに `sum`, `total` で十分。「現在の」という意味の `current` は、複数の同種要素が共存している文脈（リスト要素 vs カーソル位置など）でのみ意味を持つ。

### two pointer の重複スキップ: 2つの等価な書き方

**形A: 先にずらして「後ろを見る」**
```python
left += 1
right -= 1
while left < right and nums[left] == nums[left - 1]:  # 後ろ (= ずらす前) と比較
    left += 1
while left < right and nums[right] == nums[right + 1]:
    right -= 1
```

**形B: 先に「前を見て」スキップ、最後にずらす**
```python
while left < right and nums[left] == nums[left + 1]:  # 前 (= 未訪問) と比較
    left += 1
while left < right and nums[right] == nums[right - 1]:
    right -= 1
left += 1
right -= 1
```

形Aは「直前に見たのと同じならスキップ」、形Bは「次が同じなら今いる位置でスキップ完了」
どちらも最終的に `(left, right)` が「次に評価すべき新しい値」を指す。

### `total == 0` のブロックを早期 continue でフラット化

[huyfififi#30](https://github.com/huyfififi/coding-challenges/pull/30) (Step3 メモより)

> `total == 0`の場合の処理が`total < 0` や `total > 0`の場合と比べると複雑で、このブロックこそネストを浅くしたいなと思った。

```python
if total < 0:
    left += 1
    continue
if total > 0:
    right -= 1
    continue
# total == 0 のメイン処理（インデント浅い、両端の対称性も見える）
```

## その他

### 3手法の比較表

[tom4649#69](https://github.com/tom4649/Coding/pull/69)

| 手法 | Time | Space | 重複排除 |
|------|------|-------|--------|
| ハッシュマップ法 | O(n²) | O(n) | タプルを `seen` セットに追加 |
| 2ポインタ法 | O(n²) | O(1) ※結果除く | ポインタを `while` でスキップ |
| ハッシュセット法 | O(n²) | O(n) | `while` で j をスキップ |

> 2ポインタ法は、ハッシュ構造が不要なため空間効率が最良。

### 重複スキップを関数化

[naoto-iwase#75](https://github.com/naoto-iwase/leetcode/pull/75) 

```python
def skip_to_next_different(start, step):
    index = start
    while (0 <= index + step < n
        and sorted_nums[index] == sorted_nums[index + step]):
        index += step
    return index + step
```

`step=+1` / `-1` の両方向に使えて、3か所の重複スキップ while を共通化できる。可読性とのトレードオフはある（呼び出し箇所だけ見ても何が起きているかは追えない）。

### ソート済み配列での早期打ち切り

[yamashita-ki#4](https://github.com/yamashita-ki/codingTest/pull/4) 

> numsはソート済みなのでaが負の数でなければ、走査をやめる
> `if (nums[i] > 0) break;`

`nums[i] > 0` の時点で残り2要素もそれ以上なので和は必ず正になるから打ち切ることができる


## Step3
```py
class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        sorted_nums = sorted(nums)
        result = []
        for i in range(len(sorted_nums) - 2):
            if sorted_nums[i] > 0:
                break
            
            if i > 0 and sorted_nums[i] == sorted_nums[i - 1]:
                continue

            left = i + 1
            right = len(sorted_nums) - 1
            while left < right:
                s = sorted_nums[i] + sorted_nums[left] + sorted_nums[right]
                if s < 0:
                    left += 1
                elif s > 0:
                    right -= 1
                else:
                    result.append([sorted_nums[i], sorted_nums[left], sorted_nums[right]])
                    left += 1
                    right -= 1
                    while left < right and sorted_nums[left] == sorted_nums[left - 1]:
                        left += 1
                    while left < right and sorted_nums[right] == sorted_nums[right + 1]:
                        right -= 1
        return result
```

test case
- [-2,-1,0,1,2]
- [-1,0,1,2,-1,-4] 重複がある
- [-1,0,1] 最小長
- [0,0,0,0] [0,0,0]が返る
- [-4,-1,-1,-1,1,2,2] 内側のwhileに入る
- [0,1,2,3] early break
- [-3,-2,-1] 全て負

## 過去に解いた類題

- [two-sum]
- [combination-sum] 再帰 + バックトラック
- [minimum-size-subarray-sum] two pointer（sliding window）
- [find-k-pairs-with-smallest-sums]
- [subarray-sum-equals-k]