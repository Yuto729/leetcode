---
tags:
  - leetcode
date: 2026-09-06
url: https://leetcode.com/problems/contains-duplicate/
difficulty: Easy
---

# 217. Contains Duplicate

Given an integer array `nums`, return `true` if any value appears at least twice in the array, and return `false` if every element is distinct.

Example 1:
Input: nums = [1,2,3,1]

Output: true

Explanation:

The element 1 occurs at the indices 0 and 3.

Example 2:
Input: nums = [1,2,3,4]

Output: false

Explanation:

All elements are distinct.

Example 3:
Input: nums = [1,1,1,3,3,4,3,2,4,2]

Output: true

## Step1

time; O(n)
space: O(n)

```py
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        return len(set(nums)) != len(nums)
```

time: O(nlogn)
space: O(1)

```py
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        nums.sort()
        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1]:
                return True

        return False
```

time: O(n)かつspace: O(1)はないっぽい

## Step2

## Step3
