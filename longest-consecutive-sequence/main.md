# 128. Longest Consecutive Sequence
Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence.
You must write an algorithm that runs in O(n) time.

Example 1:
Input: nums = [100,4,200,1,3,2]
Output: 4
Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. Therefore its length is 4.

Example 2:
Input: nums = [0,3,7,2,5,8,4,6,0,1]
Output: 9

Example 3:
Input: nums = [1,0,1,2]
Output: 3

Constraints:
- 0 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9

## Approach
問題文にはO(n)と書いてあるが、まずナイーブな方法で実装してみる。連続する部分が探しやすいように最初にソートをする。そしてスライディングウィンドウで数字が連続する部分の最大の長さを求めていくが、以下の点に気を付ける

- 同じ数字が出た時は、カウントを増やさない
- `sorted_nums[i] != sorted_nums[i-1] + 1`と`sorted_nums[i] == sorted_nums[i - 1]`の順番
- 結果の初期値を1にすることで、要素が一個しかないケースに対応する. 要素が0個のケースは例外として切り出した

Time: O(nlogn)
Space: O(n) sortedを使うので
```py
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0

        sorted_nums = sorted(nums)
        n = len(sorted_nums)
        result = 1
        current_length = 1
        for i in range(1, n):
            if sorted_nums[i] == sorted_nums[i - 1]:
                continue
            
            if sorted_nums[i] != sorted_nums[i - 1] + 1:
                current_length = 1
                continue

            current_length += 1
            result = max(result, current_length)
        
        return result
```
テストケース (エッジケースに注意)
- [0,3,7,2,5,8,4,6,0,1]
- [0,1,1,2]
- [0]
- []

- `sorted_nums[i] != sorted_nums[i - 1] + 1`の部分だが、これだと条件としては微妙で、実際にリセットするべき条件は、前が0で今見ているのが2のように1つ以上離れるときなので、以下のように書く方が条件が背反になるので良いのだろう
`if sorted_nums[i] > sorted_nums[i - 1] + 1`

- setで重複を弾けば、処理がシンプルになる
Time: O(n + klog k) k: ユニーク要素の個数。最悪は変わらないが、重複が多ければソート部分と後ろの走査部分が楽になる

Space: O(n)だが、setの構築の分だけ余計にメモリ消費する。

```py
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0

        sorted_nums = sorted(set(nums)) # memo: sortedはiterableを引数にとり、listを返す
        result = 1
        start = 0
        for i in range(1, len(sorted_nums)):
            if sorted_nums[i]  == sorted_nums[i - 1] + 1:
                result = max(result, i - start + 1)
            else:
                start = i

        return result
```

条件の部分を多少変えてみる。i番目が連続部分列に含まれない時に最大値とスタート位置を更新する
この方法だと、最後にスタート位置が更新されてからループを抜けるまでの連続部分列の長さを考慮に入れていないので、ループから出た後にも更新する必要がある。
nums[i]を部分列に含まないのに最大値を更新しているので分かりにくい

```py
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0

        sorted_nums = sorted(set(nums))
        result = 1
        start = 0
        for i in range(1, len(sorted_nums)):
            if sorted_nums[i]  != sorted_nums[i - 1] + 1:
                result = max(result, i - start)
                start = i
        
        # ループ後にもう一度確定しないと、最後の連続列が反映されない
        result = max(result, len(sorted_nums) - start)

        return result
```

O(n)解法
- 1passは無理そう。2passで考える。事前にあると良い情報は、numsにどんな数字があるか。そして数字の検索がO(1)でできると良い。dictかsetを使う

考え方
- 重複をなくした`num_set`を走査する。各要素 xについて`x+1, x+2, ....`が`num_set`の中にあるかを確認し、consequtive sequenceの長さを引き伸ばす。存在しなくなったらマックスを更新する。
- 上記をナイーブに実装すると、すでに確認したconsecutive sequenceの部分列を走査してしまう可能性がある（つまり重複）。最悪計算量がO(n^2)になる
    - そこで、重複がなくなるように今見ている要素がconsecutive sequenceの先頭である時だけ長さを引き伸ばす操作をする。

時間計算量: O(n)
- 先頭で要素は、スキップされるのでループに入らない
- whileループで訪問される要素は、各連続列につき先頭から末尾まで1回ずつだけ。全体で各要素は高々1回しか触れない。
set構築はO(n)である

```py
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        num_set = set(nums)
        n = len(nums)
        max_len = 0
        for num in num_set:
            current = num
            if num - 1 in num_set:
                continue

            length = 1
            while current + 1 in num_set:
                length += 1
                current += 1
            max_len = max(max_len, length)
        
        return max_len
```
他の解法
- Union-Find
- Hash map

## 練習
```py
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        num_set = set(nums)
        max_len = 0
        for num in num_set:
            if num - 1 in num_set:
                continue
            
            current = num
            current_length = 1
            while current + 1 in num_set:
                current += 1
                current_length += 1

            max_len = max(max_len, current_length)
        
        return max_len
```
### run
nums = [0,3,7,2,5,8,4,6,0,1]
num_set = [0,3,7,2,8,4,6,1]
// num = 0
init current_length=1
while loop
- 1 in num_set current_length=2
- 2 in ....
- 3 in ....
...
- 8 in num_set current_length=9
return 9

エッジケース
nums = [] -> 0になる
nums = [1] -> 1になる