# 4. Median of Two Sorted Arrays

Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.
The overall run time complexity should be O(log (m+n)).
 
Example 1:
Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.

Example 2:
Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.

Constraints:
- nums1.length == m
- nums2.length == n
- 0 <= m <= 1000
- 0 <= n <= 1000
- 1 <= m + n <= 2000
- -10^6 <= nums1[i], nums2[i] <= 10^6

## Step1
マージソートのように２つの配列を統合し、その後中央値を計算する。
Time: O(m + n)
Space: O(m + n)
```py
class Solution:
   def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        p1 = 0
        p2 = 0
        sorted_arr = []
        while p1 < len(nums1) and p2 < len(nums2):
            if nums1[p1] <= nums2[p2]:
                sorted_arr.append(nums1[p1])
                p1 += 1
            else:
                sorted_arr.append(nums2[p2])
                p2 += 1
        
        if p1 < len(nums1):
            sorted_arr.extend(nums1[p1:])
        else:
            sorted_arr.extend(nums2[p2:])
        
        length = len(sorted_arr)
        if length % 2 == 0:
            return (sorted_arr[length // 2] + sorted_arr[length // 2 - 1]) / 2
        
        return sorted_arr[length // 2]
```
O(log (m+n))にしたい。ボトルネックはマージしているところ。マージ操作なしで中央値を求められないか？
全然わからないのでAIに教えてもらう
- 二分探索か分割統治法
- 「中央値を求める」->「両配列を合わせて左半分と右半分に分割する位置を見つける」
    - なるほど、これならいけそうだ。発想の転換

条件: 左半分の要素数 = 右半分の要素数 & max(左) <= min(右)
- 上記の条件を満たす分割点(nums1側の分割点i, nums2側の分割点j)を見つける
    - 上記の1つ目の条件より、iを決めればjは自動的に決まる
    - 左半分サイズ = (m + n + 1) // 2, i + jがこれに等しいので、j = (m + n + 1) // 2 - i

以下を満たすようなiを見つけたい。
max(左) = max(nums1[i - 1], nums2[j - 1])
min(右) = min(nums1[i], nums2[j])
-> nums1[i - 1] < nums2[j] かつ nums2[j - 1] < nums1[i]
述語: nums1[i - 1] < nums2[j] かつ nums2[j - 1] < nums1[i]とすると、

Ex. [1,2,5] [3,4,6]で考えてみる
結合: [1,2,5,3,4,6]