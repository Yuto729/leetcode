---
tags:
  - leetcode
date: 2026-08-14
url: https://leetcode.com/problems/merge-k-sorted-lists/
difficulty: Hard
---

# 23. Merge k Sorted Lists

You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order.

Merge all the linked-lists into one sorted linked-list and return it.

Example 1:
Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
Explanation: The linked-lists are:
[
1->4->5,
1->3->4,
2->6
]
merging them into one sorted linked list:
1->1->2->3->4->4->5->6

Example 2:
Input: lists = []
Output: []

Example 3:
Input: lists = [[]]
Output: []

## Step1

1 -> 4 -> 5
1 -> 3 -> 4
2 -> 6

2つだとした場合 -> two pointerで解ける
n個の場合はn pointer?
list.length = k
毎回比べるk個がある。

- 1,1,2 -> 1が抜ける -> 4,1,2
- 1が抜ける -> 4,3,2
- 2が抜ける -> 4,3,6....
  len(list) <= 500

計算量 = O(k^2 \* n) -> 10^10 終わらないか
while ...: O(n \* k)
min = min([..]) O(k) -> ここの部分を最適化する　ヒープかな？ -> O(logk)になる log2(10^4) = 10くらい
全体で10^8くらいか...

ヒープ使えばいいのかこれ
tupleのヒープで第二要素が比較されるの忘れてた. グローバルでカウントされるインデックスを用意して、タプルの第二要素にインデックスを入れる。別でインデックスに対応するノードをhashmapで持っておけばインデックスからノードが引けるのでok

30分くらいかかった
time: O(k n logk)

```py
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        heap = []
        i = 0
        number_to_node = {}
        for root in lists:
            if root is None:
                continue

            heapq.heappush(heap, (root.val, i))
            number_to_node[i] = root
            i += 1

        dummy = ListNode()
        node = dummy
        while heap:
            min_value, number = heapq.heappop(heap)
            min_node = number_to_node[number]
            node.next = min_node
            node = min_node
            if min_node.next is not None:
                i += 1
                number_to_node[i] = min_node.next
                heapq.heappush(heap, (min_node.next.val, i))

        return dummy.next
```

## Step2

## Step3
