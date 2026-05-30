# Capacity To Ship Packages Within D Days
A conveyor belt has packages that must be shipped from one port to another within days days.
The ith package on the conveyor belt has a weight of weights[i]. Each day, we load the ship with packages on the conveyor belt (in the order given by weights). We may not load more weight than the maximum weight capacity of the ship.

Return the least weight capacity of the ship that will result in all the packages on the conveyor belt being shipped within days days.

Example 1:
Input: weights = [1,2,3,4,5,6,7,8,9,10], days = 5
Output: 15
Explanation: A ship capacity of 15 is the minimum to ship all the packages in 5 days like this:
1st day: 1, 2, 3, 4, 5
2nd day: 6, 7
3rd day: 8
4th day: 9
5th day: 10

Note that the cargo must be shipped in the order given, so using a ship of capacity 14 and splitting the packages into parts like (2, 3, 4, 5), (1, 6, 7), (8), (9), (10) is not allowed.

Example 2:
Input: weights = [3,2,2,4,1,4], days = 3
Output: 6
Explanation: A ship capacity of 6 is the minimum to ship all the packages in 3 days like this:
1st day: 3, 2
2nd day: 2, 4
3rd day: 1, 4

Example 3:
Input: weights = [1,2,3,1,1], days = 4
Output: 3
Explanation:
1st day: 1
2nd day: 2
3rd day: 3
4th day: 1, 1
 

Constraints:
- 1 <= days <= weights.length <= 5 * 10^4
- 1 <= weights[i] <= 500

## Step1
船の容量をいくつにすれば、順番通りに荷物を分割してdays日以内に全部運べるか？その最小の容量を求める問題
Approach
- dp
    - dp[i][j]をweightsの0 ~ iまでをj日で運ぶときの最小の容量とする
    - 0 ~ iまでをj日で運ぶときの最小の容量 = min over k(0 ~ kまでをj - 1日で運ぶときの最小の容量 + k+1 ~ iまでを1日で運ぶ)

TLE
```py
class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        if not weights:
            return

        n = len(weights)
        dp = [[float('inf')] * (days + 1) for _ in range(n)]
        for i in range(n):
            dp[i][1] = sum(weights[:i + 1])

        for i in range(1, n):
            for j in range(2, min(days + 1, i + 2)):
                for k in range(i):
                    dp[i][j] = min(dp[i][j], max(dp[k][j - 1], sum(weights[k + 1: i + 1])))
        
        return min(dp[n - 1][:days + 1])
```

二分探索だけどやり方がわからないので聞いてみる
- `max(dp[k][j - 1], sum(weights[k + 1: i + 1]`で求めたいのは、「全分割のmaxを最小化するcapasity」
- capasityはdaysを増やすと単調減少する（自然）
    - しかしdaysを目的関数にして二分探索はできないので逆転をさせる
    - 「capasityを増やすとdaysは単調減少する」
上記の性質から以下のように述語を記述できる
「capasityがmidの時、days以内に全部運べるか」
初めてTrueになるcapasityを探索する
- days以内に全部運べるかどうかの計算は貪欲法で行う

```py
class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        if not weights:
            return

        n = len(weights)
        left, right = 0, sum(weights)
        while left < right:
            # capasityがmidの時にdays以内に全部運べるか
            mid = (left + right) // 2
            num_days = 1
            total = 0
            i = 0
            while i < n:
                if weights[i] > mid:
                    num_days = float('inf')
                    break
                    
                if total + weights[i] > mid:
                    num_days += 1
                    total = 0
                    continue
                
                total += weights[i]
                i += 1

            if num_days <= days:
                right = mid
            else:
                left = mid + 1
        
        return left
```
🤖
> left=0だとmid=0になりうる場面で全部inf→leftが上がっていくので正し
  く動きますが、無駄な探索が増えます。left=max(weights)にすればその分速
  くなります。

修正
```py
class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        if not weights:
            return

        n = len(weights)
        left, right = max(weights), sum(weights)
        while left < right:
            # capacityがmidの時にdays以内に全部運べるか
            mid = (left + right) // 2
            num_days = 1
            total = 0
            i = 0
            for weight in weights:
                if total + weight > mid:
                    num_days += 1
                    total = weight
                    continue
                
                total += weight
            if num_days <= days:
                right = mid
            else:
                left = mid + 1
        
        return left
```

## Step2

### bisect_leftを使った実装
[naoto-iwase#27](https://github.com/naoto-iwase/leetcode/pull/27) / [mamo3gr#42](https://github.com/mamo3gr/arai60/pull/42)
> ```python
> return bisect.bisect_left(range(capacity_hi), True, lo=capacity_lo, key=is_feasible)
> ```
Pythonの`range`はO(1)空間でインデックスアクセスをサポートするので、`bisect_left`にそのまま渡せる。

`bisect_left`は「ソート済みリストで値を挿入すべき左端位置」を返す関数。`key=is_feasible`により各capacityに対して`[False, False, ..., True, True, ...]`という列が生まれ、最初にTrueになる位置=最小のcapacityを二分探索で見つける。`key`はPython 3.10以降。

```python
def is_feasible(capacity):
    days_needed = 1
    total = 0
    for weight in weights:
        if total + weight > capacity:
            days_needed += 1
            total = 0
        total += weight
    return days_needed <= days
```

### 関数名: is_feasible vs is_shippable vs can_ship
[naoto-iwase#27](https://github.com/naoto-iwase/leetcode/pull/27/files#r1852073960)
> shippableも少し検討したんですが、"able"が複数日にわたる輸送計画の可能性ではなく、もっと狭い「ある1日において輸送可能かどうか」のニュアンスを持つ気がして、少し違う気がしたのでふんわりとfeasibleにしてみました。

命名の粒度に対する考察。`can_be_shipped`（yumyum116）、`CanBeShipped`（5ky7）なども。判定関数の名前はbool値を返すことが分かるように。

### 日数を返す vs boolを返す
[mamo3gr#42](https://github.com/mamo3gr/arai60/pull/42) / [5ky7#44](https://github.com/5ky7/arai60/pull/44)
> 好みの範囲だろうが、daysを計算する方が、メインルーチンでの二分探索の更新がバグりにくそうだし、汎用的に使いまわせそう。

サブルーチンが「日数」を返すか「bool」を返すかの設計判断。日数を返す方が汎用的で、呼び出し側の条件変更（days以下→days未満など）に強い。boolを返す方はearly returnしやすく、daysを超えた時点で打ち切れるのでパフォーマンスが良い。
自分の回答をサブルーチンに切り出すと、「日数」を返す解法になる。`calculate_shipping_days`とかが良さそう。

### 不変条件のコメント
[mamo3gr#42](https://github.com/mamo3gr/arai60/pull/42) (garunituleのコード参照)
> ```python
> """
> 不変条件
> - capacity < left_capacityの場合、daysより大きい
> - right < capacityの場合、days以下
> """
> ```
二分探索で探索区間の不変条件をコメントとして明記する。半開区間`[lo, hi)`で管理し、終了時に`lo`が答えを指すことが自明になる。

### 「先に操作してから辻褄合わせ」パターン
[olsen-blue on yumyum116#10](https://github.com/yumyum116/LeetCode_Arai60/pull/10/files#r2046736987)
> とりあえず毎回やるメイン作業である+=操作をしてしまう → その後、時々発生するキャパを溢れてたら辻褄を合わせる

```python
total_weight += weight
if total_weight > capacity:
    total_weight = weight
    days += 1
```
vs 事前チェック方式。Find Median from Data Stream（ヒープ2つ）でも同じパターン: まずpushしてからバランス調整。ただし本人も追記で「本当にこちらが良いか怪しい」と。
「容量を超えるなら次の日に回す」方が手作業には近い

### lower boundの初期値: max(weights) vs 0
[5ky7#44](https://github.com/5ky7/arai60/pull/44) / [tom4649#42](https://github.com/tom4649/Coding/pull/42)
> min_capacity = 0で始めてチェックを挟めば良い

`left=max(weights)`にすれば`weight > capacity`チェックが不要になる。`left=0`にする場合は判定関数内で個別の荷物がcapacityを超えるケースのガードが必要。

### Pythonのintオーバーフロー
[nodchip on yumyum116#10](https://github.com/yumyum116/LeetCode_Arai60/pull/10/files#r2050484831)
> `low_weight + (high_weight - low_weight) // 2` という書き方は、C言語等、intがオーバーフローするのを避けるための書き方です。Pythonではintは実質多倍長整数(メモリが許す限り桁数を伸ばせる)で、よほど大きな数でなければオーバーフローしません。そのため、`(low_weight + high_weight) // 2` と書いてよいと思います。


## Step3
```py
class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        if not weights:
            return 0
        
        def can_be_shipped(mid, days):
            total_weight = 0
            num_days = 1
            for weight in weights:
                if total_weight + weight > mid:
                    num_days += 1
                    total_weight = weight
                    continue
                
                total_weight += weight
            
            return num_days <= days

        left, right = max(weights), sum(weights)
        while left < right:
            mid = (left + right) // 2
            if can_be_shipped(mid, days):
                right = mid
            else:
                left = mid + 1
            
        return left
```