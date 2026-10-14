---
tags:
  - leetcode
date: 2026-08-17
url: https://leetcode.com/problems/maximum-profit-in-job-scheduling/
difficulty: Hard
---

# 1235. Maximum Profit in Job Scheduling

We have `n` jobs, where every job is scheduled to be done from `startTime[i]` to `endTime[i]`, obtaining a profit of `profit[i]`.

You're given the `startTime`, `endTime` and `profit` arrays, return the maximum profit you can take such that there are no two jobs in the subset with overlapping time range.

If you choose a job that ends at time `X` you will be able to start another job that starts at time `X`.

Example 1:
![](https://assets.leetcode.com/uploads/2019/10/10/sample1_1584.png)

Input: startTime = [1,2,3,3], endTime = [3,4,5,6], profit = [50,10,40,70]
Output: 120
Explanation: The subset chosen is the first and fourth job.
Time range [1-3]+[3-6] , we get profit of 120 = 50 + 70.

Example 2:
![](https://assets.leetcode.com/uploads/2019/10/10/sample22_1584.png)

Input: startTime = [1,2,3,4,6], endTime = [3,5,10,6,9], profit = [20,20,100,70,60]
Output: 150
Explanation: The subset chosen is the first, fourth and fifth job.
Profit obtained 150 = 20 + 70 + 60.

Example 3:
![](https://assets.leetcode.com/uploads/2019/10/10/sample3_1584.png)

Input: startTime = [1,1,1], endTime = [2,3,4], profit = [5,6,4]
Output: 6

## Step1

DPで解くと良さそう

- dp[i] = (time=iまでに収まる中で最大のProfit) とすると、以下のように更新できる

- dp[i] = max(A, B)
  - A = max_jについて(time=iにちょうど終わる1つの仕事の開始時刻をs_ijとして、s_ijまでに収まる中で最大のProfit + s_ijから始まってiに終わる仕事の利益)
  - B = i-1までに収まる最大のProfit

- time=iにちょうど終わる仕事を全て見つけるには、endTimeを並び替えた上で、二分探索を用いる。`bisect_right`を用いて、一番後ろを探し、前に向かって走査。iで終わる範囲を超えたら打ち切る

- dpの空間計算量はO(max_end_time)となるが、max_end_time <= 10^9なので空間計算量が大きい。存在しない終了時刻は最初から走査しないようにする。座標圧縮みたいなことをやる
  - endTime を並び替えて、前から順に走査し、dp[end_timeのindex]を埋めていく
  - 並び替えると、startTimeとの対応が消えてしまうので、元のインデックスとのタプルにしてから並び替えるか、それぞれの終了時刻と元のインデックスの対応関係をDictにしておく。今回は後者を選んだ
    - 書いていて、同じ終了時刻の仕事はループ間でスキップしたいので、上記Dictのキー（ユニーク）を並び替えて走査対象にする。

```py
class Solution:
    def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
        end_time_to_indices = defaultdict(list)
        for i, end_time in enumerate(endTime):
            end_time_to_indices[end_time].append(i)

        end_times = sorted(end_time_to_indices.keys())
        max_profit_before = [0] * len(end_times)
        # time = endTime[i]にちょうど終わる
        max_profit_before[0] = profit[0]
        for i in range(1, len(end_times)):
            end_time = end_times[i]
            indices = end_time_to_indices[end_time]
            for j in indices:
                start_time = startTime[j]
                max_profit_before[end_time] = max(max_profit_before[end_time_set[i - 1]], max_profit_before[start_time] + profit[j])

        return max_profit_before[-1]
```

- max_profit_before[start_time]だと座標圧縮後のインデックスに対応できていない。しかし対応しようとして以下の点に気が付く

- s_ijに終了時刻が収まる範囲での最大値を圧縮後だと記録できないから、max_profit_beforeに対応するエントリがなく、無理だと思って一度止まったが、
  ヒントを軽くみて理解した。

      - s_ij以下で最大の終了時刻をend_timesから求める。すでにmax_profit_beforeのその最大の終了時刻に対応する最大値は求まっているはずなので、それを用いて利益を計算する
      - 上記の計算には二分探索を用いることができる（end_timesはソートされているので）

Acceptするまで1時間くらいかかってしまった。Hardはまだスラスラ解けない

Time: O(nlogn) ソート+各jobでの二分探索

```py
class Solution:
    def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
        end_time_to_indices = defaultdict(list)
        for i, end_time in enumerate(endTime):
            end_time_to_indices[end_time].append(i)

        end_times = sorted(end_time_to_indices.keys())
        max_profit_before = [0] * len(end_times)
        # time = endTime[i]にちょうど終わる
        for i in range(len(end_times)):
            end_time = end_times[i]
            indices = end_time_to_indices[end_time]
            for j in indices:
                start_time = startTime[j]
                # start_time以下で最大のend_timeのインデックス
                max_end_index_before_start = bisect_right(end_times, start_time) - 1
                if max_end_index_before_start < 0:
                    # start_timeより前に終わる仕事はない
                    # i=0のときは、max_profit_before[-1]=0と比較
                    max_profit_before[i] = max(max_profit_before[i - 1], max_profit_before[i], profit[j])
                    continue

                # max_profit_before[i] = max(max_profit_before[i - 1], profit[j])こう書いていた
                # 2段階でmaxを取らないといけないときは一つずつ解決していった方がミスらなく良さそう
                max_profit_before[i] = max(max_profit_before[i - 1], max_profit_before[i], max_profit_before[max_end_index_before_start] + profit[j])

        return max_profit_before[-1]
```

### ミス一覧

- max_profit_before[0] = profit[0] で初期化し、i=1からループ
  - end_times[0] に複数ジョブが属していても、その中の profit[0]（インデックス0のジョブ）だけを無条件に採用している。同じバケット内の他のジョブ（indices に入っている他の j）の可能性を一切見ていない。上の反例だと max_profit_before[0]=100になってほしいのに、profit[0]=100はたまたま正しいが、profit[0]=10, profit[1]=100の並びだとmax_profit_before[0]=10になり誤り。

  - i>=1 のループ内も次の項目と同じバグが残っている。

- if 分岐、else 分岐ともに max(max_profit_before[i - 1], ...) の2引数のみで、max_profit_before[i] 自身（＝同じバケット内で直前の j まで求めた暫定最良値）を比較対象に入れていない。

### 他の解法

### フォローアップ

## Step2

## Step3
