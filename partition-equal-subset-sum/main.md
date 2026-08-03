---
date: 2026-08-01
tags:
  - leetcode
  - review
url: https://leetcode.com/problems/partition-equal-subset-sum
---

Given an integer array `nums`, return `true` *if you can partition the array into two subsets such that the sum of the elements in both subsets is equal or* `false` *otherwise*.

Example 2:
Input: nums = [1,5,11,5]
Output: true
Explanation: The array can be partitioned as [1, 5, 5] and [11].

Example 2:
Input: nums = [1,2,3,5]
Output: false
Explanation: The array cannot be partitioned into equal sum subsets.

Constraints:
1 <= nums.length <= 200
1 <= nums[i] <= 100

## Step1

- subsetの合計値がnumsの合計の1/2になるようなsubsetが存在するかどうかを判定する
  - integerなので割り切れない場合は即False

- Two SumやThree Sumの要領で、足していくと考えたが、めんどくさそう。
- ナイーブに考えたら、各indexについてsubsetに含むか含まないかで分岐が生じるので総当たりすれば良い

- 長さの最大が200なので総当たりは無理そう
  - 2^200 ~= 10^60くらい
- TopicsにDPとあったのでヒントとして活用。DPが使えるなら再帰でトップダウンでもいける。
  - `@cache`を使い軽く書いてみる -> Acceptなので一旦終了

- Acceptしてから計算量を考えるのはよくない。事前に素早く見積もれないと手法の評価ができないので、ノーヒントで解けるようにならない

Time: O(N*sum(nums))
@cacheありなら、indexとtargetの2次元マトリクスを全て埋めるのに必要な計算ステップが上界となる。target = 0 ~ sum(nums)である。
本問の制約だと、最大200*200\*100 = 10^6程度

```py
class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        array_sum = sum(nums)
        if array_sum % 2 == 1:
            return False

        @cache
        def helper(i, target):
            if i == len(nums) - 1:
                if nums[i] == target:
                    return True
                return False

            if target == 0:
                return True

            if target < 0:
                return False

            # iを入れる場合
            if helper(i + 1, target - nums[i]):
                return True
            # iを入れない場合
            if helper(i + 1, target):
                return True

            return False

        return helper(0, array_sum // 2)
```

最初に書いたのはこれだが、偶然これでも通ってるのは、最後の要素が必ずどちらかの集合に属するから

```py
class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        sum_ = sum(nums)
        if sum_ % 2 == 1:
            return False

        @cache
        def helper(i, target):
            if i == len(nums) - 1:
                if nums[i] == target:
                    return True
                return False
            if helper(i + 1, target - nums[i]):
                return True
            if helper(i + 1, target):
                return True

            return False

        return helper(0, sum_ // 2)
```

### 実装2

ボトムアップバージョン

### 実装3

bitset DP
