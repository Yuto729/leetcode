# 238. Product of Array Except Self

Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operation.

Example 1:
Input: nums = [1,2,3,4]
Output: [24,12,8,6]

Example 2:
Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]

Follow up: Can you solve the problem in O(1) extra space complexity? (The output array does not count as extra space for space complexity analysis.)

## Step1

割り算を使ってはいけないので、掛け算だけで達成することを考える。
O(n)で解きたいので、まず配列の要素を順番に舐めていく。現在の要素より前の要素の積を計算していけば一部は計算できる。残りの要素をかける必要があるが、配列を逆から舐めていって同じように今まで出てきた要素の積を取って先ほど計算した値にかければ、「自分以外の要素の積」が計算できそう。
時間計算量O(n)かつ空間計算量O(1)で解ける。

前からみるのと後ろからみるのを組み合わせる方法はよく見かける

```py
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        ans = [1] * len(nums)
        left = 1
        for i in range(len(nums)):
            ans[i] = left
            left *= nums[i]

        right = 1
        for i in range(len(nums) - 1, -1, -1):
            ans[i] = ans[i] * right
            right *= nums[i]

        return ans
```

test

- 0じゃないケースは問題なし
- 0が1つ入ってる時 -> left, rightが途中から0になる。0の位置の時だけleftかつrightが0ではない
- 0が2つ以上入ってる時 -> left もしくは rightが常に0

## Step2

- https://github.com/kazuki-official/leetcode/pull/100
  空間計算量がO(1)じゃないバージョン。意図がわかりやすい

```py
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        prefix_product = [1] * len(nums)
        for i in range(1, len(nums)):
            prefix_product[i] = prefix_product[i - 1] * nums[i - 1]

        suffix_product = [1] * len(nums)
        for i in range(len(nums) - 2, -1, -1):
            suffix_product[i] = suffix_product[i + 1] * nums[i + 1]

        product_except_self = [None] * len(nums)
        for i in range(len(nums)):
            product_except_self[i] = prefix_product[i] * suffix_product[i]

        return product_except_self
```

- https://github.com/tom4649/Coding/pull/121
  以下の命名がわかりやすい
  left -> prefix_product
  right -> suffix_product

## Step3

```py
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        product_except_self = [1] * len(nums)
        prefix_product = 1
        for i in range(len(nums)):
            product_except_self[i] = prefix_product
            prefix_product *= nums[i]

        suffix_product = 1
        for i in range(len(nums) - 1, -1, -1):
            product_except_self[i] *= suffix_product
            suffix_product *= nums[i]

        return product_except_self
```
