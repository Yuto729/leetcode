---
date: 2026-08-01
tags:
  - leetcode
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

最初に書いたのは以下だが、偶然これでも通ってるのは、最後の要素が必ずどちらかの集合に属するから

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

ボトムアップバージョンを書いてみる。
久しぶりに書いたのでちょっと詰まったところがある

- DPテーブルの形状は、再帰関数の引数がそのまま表の行と列に対応する。
- 0 <= i < len(nums), 1 <= j <= target
- dp[i][j]: nums[:i + 1]から選んで和がjとなるsubsetを作れるかどうか
- 再帰の分岐は「nums[i]を使うとき」と「nums[i]を使わないとき」なので、そのままボトムアップ版でも上記の条件を使う

```py
class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        # dp[i][j]: nums[:i + 1]から選んで和がjとなるsubsetを作れる. 0/1ナップザック
        sum_of_nums = sum(nums)
        if sum_of_nums % 2 == 1:
            return False

        target = sum_of_nums // 2
        dp = [[False] * (target + 1) for _ in range(len(nums))]
        for i in range(len(nums)):
            if nums[i] > target:
                continue

            for j in range(i, len(nums)):
                dp[j][nums[i]] = True

        for i in range(len(nums)):
            for j in range(1, target + 1):
                if j < nums[i]:
                    dp[i][j] = dp[i - 1][j]
                    continue

                # nums[i]を使わないときとnums[i]を使うとき
                dp[i][j] = dp[i - 1][j] or dp[i - 1][j - nums[i]]

        return dp[len(nums) - 1][target]
```

### 実装3

上記のDPテーブルは1次元に落とせる

```py
class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        sum_of_nums = sum(nums)
        if sum_of_nums % 2 == 1:
            return False

        target = sum_of_nums // 2
        dp = [False] * (target + 1)
        dp[nums[0]] = True
        for i in range(1, len(nums)):
            for j in range(1, target + 1):
            # for j in range(target, 0, -1) が正しい
                if j < nums[i]:
                    continue

                if j == nums[i]:
                    dp[j] = True
                    continue

                dp[j] = dp[j] or dp[j - nums[i]]

        return dp[target]
```

-> 間違い。上記は重複ありナップザックのときの解法になってしまう。内側のjのループで複数回`nums[i]`を用いた結果になることがある。

- jのループを逆向きにすれば解決する
  - なぜ？ -> jを順方向に回すと、`j - nums[i]`はすでにいくつか前のループで更新されている、つまりnums[i]を一度使った結果を元にもう一度numを使えてしまうが、降順にすると、`j - nums[i]`はまだ更新されていない領域なので前の行の値が保たれる = 更新は外側のループ1回につき1回だけとなるので、0/1ナップサックの要件を満たす。

  ```py
  class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)
        if total % 2:
            return False

        target = total // 2

        # dp[j]: ここまで見た要素から選んで和 j を作れるか
        dp = [False] * (target + 1)
        dp[0] = True                          # 空集合

        for num in nums:
            if num > target:                  # 単独で超える要素は絶対に使えない
                continue

            for j in range(target, num - 1, -1):   # 降順。num 未満は変化しないので下限は num
                dp[j] = dp[j] or dp[j - num]
            if dp[target]:                    # 早期リターン
                return True

        return dp[target]
  ```

### 実装3

bitset DP

- 上記一次元DPは[True, False, True, ...]という真偽値の列だが、これを整数1個の各ビットとして表現する
  - T -> 1, F -> 0
  - 第jビットがdp[j]に対応
- `dp[j] = dp[j] or dp[j - num]`は、dp[j - num]のビットが立っているならdp[j]を立てる = 全てのビットをnumだけ左にずらして元と重ね合わせる（重ね合わせ = 和 = orに対応）
  - `bits |= bits << num`

- 向きの問題が消える
  - 上記の更新式で全てのjに対して一括で更新がかかるので、jの走査向きによって、「更新ずみの値を読んでしまう」という問題がなくなる

計算量は同じ

```py
class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)
        if total % 2:
            return False
        target = total // 2

        bits = 1                      # 和 0 のみ作れる
        for num in nums:
            bits |= bits << num
        return bits >> target & 1 == 1
```

### ナップサック問題との関連

- 0/1 ナップサック
  - 容量Wのリュックがある。品物iは重さw[i]、価値v[i]。各品物は使うか使わないかの二択。容量を超えない範囲で価値の合計を最大化する
  - 品物を入れるか入れないかで場合分け
  - 1次元DPで解く場合は内側ループを降順に回す

- 本問題は、
  - 品物i -> nums[i]
  - 重さ -> nums[i]
  - 価値 -> nums[i]
  - 容量 -> sum(nums) // 2
  - 最大化した価値 -> 作れる和の最大値
  - 答え -> 最大値が容量ちょうどか？
    と設定できる

DP配列に格納される値

- ナップサック -> 価値の最大値
- 本問題 -> 和をちょうど作れるかどうかのbool

- 無限ナップサック
  - 同じ品物を何度も選ぶことができる
  - [[leetcode/coin-change/main|Coin Change]]

### 関連

[[部分配列系問題のパターン]]

## Step3

```py
class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)
        if total % 2 == 1:
            return False

        target = total // 2
        dp = [False] * (target + 1)
        dp[0] = True
        for i in range(len(nums)):
            # nums[:i + 1]から要素を選ぶとき
            for j in range(target, 0, -1):
                # 合計がjを満たす組み合わせがあるかどうか
                if j < nums[i]:
                    continue

                dp[j] = dp[j] or dp[j - nums[i]]

        return dp[target]
```
