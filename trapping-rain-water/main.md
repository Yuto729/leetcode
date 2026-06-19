# 42. Trapping Rain Water
Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

Example 1:
Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.

Example 2:
Input: height = [4,2,0,3,2,5]
Output: 9

Constraints:
- n == height.length
- 1 <= n <= 2 * 10^4
- 0 <= height[i] <= 10^5

Approach
ex. height = [0,1,0,2,1,0,1,3,2,1,2,1]で考える
- i番目には水がどれくらい積み上がるかを考えて、それぞれのiについて足せばいけそう
- 例えば、
    - heightでi=2の時 -> 1積み上がる（height[2] = 0で、両側がそれぞれ1と2であり、その小さい方とheight[2]の差分だけ積み上がる）
    - i=4の時 -> 1積み上がるが、これはheight[4]より高いところを左右に対して見ていくと,i=3, i=7の時であり、1と3の小さい方をとって1
    - i=5の時、2積み上がる -> 左右に見ていくと、height[3]=2とheight[7]=3が基準になっていて、そのうち小さい方とheight[5]の差分が2となっていそう
    -> 左右に見ていったときの最大値を使っている？

-> iの左右を見ていって、一番高い壁を探し、そのうちの小さい方の一番上まで水が貯まる。height[i]の上に溜まるので、差分が加算されることになる。iごとに加算していくので重複はない

上記の作業をコードにする
```py
class Solution:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        left = [0] * n
        right = [0] * n
        max_height = 0
        for i in range(n):
            left[i] = max_height
            max_height = max(max_height, height[i])
        max_height = 0
        for i in range(n - 1, -1, -1):
            right[i] = max_height
            max_height = max(max_height, height[i])
        
        result = 0
        for i in range(n):
            result += max(min(left[i], right[i]) - height[i], 0)
        return result
"""
height = [0,1,0,2,1,0,1,3,2,1,2,1]

left  = [0,0,1,1,2,2,2,2,3,3,3,3] right = [3,3,3,3,3,3,3,2,2,2,1,0]
// i = 0, result = 0
// i = 1, result = 0
// i = 2, result = 1
// i = 3, result = 1
// i = 4, result = 2
// i = 5, result = 4
// i = 6, result = 5
// i = 7, result = 5
// i = 8, result = 5
// i = 9, result = 6
// i = 10, result = 6 <- answer
"""
```

> 空間を O(1) にできますか?
> 左端 left と右端 rightにポインタを置きます。それぞれの側でこれまで見た最大値 left_max, right_max を持っておきます。

- left_max < right_maxの時、leftの位置に溜まる水はその時のleft_maxで決まる。
-> right_maxが今後更新されても`min(left_max, right_max)`の結果は変わらないので

不変条件：
- [0, left), (right, n-1]のセルについてはたまる水量がresultに加算済み
- left_max -> leftより厳密に左の最大値
- right_max -> rightより厳密に右の最大値
- [left, right]が未処理範囲
    - left > rightになった時に未処理範囲がなくなり、ループから抜ける

```py
class Solution:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        left_max_height = 0
        right_max_height = 0
        left = 0
        right = len(height) - 1
        result = 0
        while left <= right:
            if left_max_height < right_max_height:
                result += max(left_max_height - height[left], 0)
                left_max_height = max(left_max_height, height[left])
                left += 1
            else:
                result += max(right_max_height - height[right], 0)
                right_max_height = max(right_max_height, height[right])
                right -= 1
        
        return result

"""
height = [4,2,0,3,2,5]
l = 0, r = 5 ans = 0
l = 0, r = 4 ans = 0
l = 1, r = 4 ans = 2
l = 2, r = 4, ans = 6
l = 3, r = 4 ans = 7
l = 4, r = 4, ans = 9
"""
```
Two Pointerのleft, rightの意味について気になったので、過去に解いたSliding Window, Two Pointer系を思い出してみる

## 単調スタック解法

- 単調減少するスタックを使う
- DP / Two Pointer は「列ごとに垂直に水を積む」のに対し、stack は「段ごとに水平に水を積む」イメージ
- Largest Rectangle in Histogram と同じ系統の発想

```py
class Solution:
    def trap(self, height: List[int]) -> int:
        stack = []  # 高さが減少するインデックス
        result = 0
        for i, h in enumerate(height):
            while stack and height[stack[-1]] < h:
                bottom = stack.pop()
                if not stack:
                    break
                left = stack[-1]
                width = i - left - 1
                bounded_height = min(height[left], h) - height[bottom]
                result += width * bounded_height
            stack.append(i)
        return result
```

不変条件 (ループ先頭 = `i` を処理する直前):
- スタック内のインデックスに対応する高さは広義単調減少
- `j ∈ stack` ⟺ `j < i` かつ `height[k] <= height[j]` for all `k ∈ (j, i)`
  (= `j` の右側にある既処理セルは全て `j` 以下 = まだ「右側により高い壁」が見つかっていない)
- `result` には pop 済み `bottom` の上に溜まる長方形が全て加算済み

`bottom` が pop される瞬間に言えること:
- 左の最も近い `bottom` より高い壁 = `stack[-1]` (単調性より)
- 右の最も近い `bottom` より高い壁 = 現在の `i` (pop 条件より)
- → この左右の壁で囲まれた水平一段の水を正確に計算できる

計算量: Time O(n) (各要素は最大1回 push/pop)、Space O(n)

## Two Pointer 系の整合したコードの書き方 

trapping rain water / longest substring without repeating / palindrome 等を通して整理。

### 最初に決める3点セット
| 決めること | 選択肢 |
|---|---|
| (A) 区間の表現 | `[l, r]` 両閉 / `[l, r)` 右開 / `(l, r]` 左開 / `(l, r)` 両開 |
| (B) 不変条件 | 区間が満たす性質 (dup-free, palindrome, sorted など) |
| (C) 補助データの範囲 | `seen`, `sum`, `max` 等が反映する区間 |

この3つが互いに整合していれば、ループ条件・初期化・更新順序が自然に決まる。

### 区間表現が決めるもの
- 長さ: `[l,r]` → `r-l+1`、`[l,r)` または `(l,r]` → `r-l`、`(l,r)` → `r-l-1`
- ループ条件: 中央の1セルも処理必須 → `<=`、不要・自明 → `<`
- 初期化: 両閉なら `[0, n-1]`、右開なら `[0, 0)` (空 window から拡張)、左開なら `(-1, 0]` (センチネル)

### パターン別テンプレート

**A. 両端から中央へ (`[l, r]` + `<=`)**: palindrome, two sum sorted, trapping rain water
```
l, r = 0, n - 1
while l <= r:
    # 不変条件: [l, r] は未処理
    ...
```

**B. Sliding Window (`[l, r)` + `<`)**: 最長部分文字列など
```
l = r = 0
while r < n:
    # 不変条件: [l, r) が条件を満たす window
    while not can_extend(s[r]):
        state.remove(s[l]); l += 1
    state.add(s[r]); r += 1
    ans = max(ans, r - l)
```

### trapping rain water の Two Pointer 2版の比較
| 版 | 区間 | ループ条件 | 補助データ (max) の範囲 | 必要な対処 |
|---|---|---|---|---|
| `<=` 版 | `[l, r]` 未処理 | `l <= r` | `l` より厳密に左 | `max(..., 0)` 必要 |
| `<` 版 | `(l, r)` 未処理 | `l < r` | `l` を含む | 初期化で両端を取り込み、`max(..., 0)` 不要 |

`<` 版:
```py
if not height: return 0
l, r = 0, n - 1
left_max, right_max = height[l], height[r]
result = 0
while l < r:
    if left_max < right_max:
        l += 1
        left_max = max(left_max, height[l])
        result += left_max - height[l]
    else:
        r -= 1
        right_max = max(right_max, height[r])
        result += right_max - height[r]
return result
```

## 不変条件 (loop invariant) について
- 標準的な定義は「反復の境目 (ループ本体実行の前後) で成り立つ」
- ループ本体の途中で一時的に崩れていてもよい
- 3点で成立を確認: 初期化 / 保存 (本体実行で保たれる) / 終了 (条件偽の時に事後条件を導く)


## 練習
Two Pointer解法
```py
class Solution:
    def trap(self, height: List[int]) -> int:
        left = 0
        right = len(height) - 1
        left_max = 0
        right_max = 0
        result = 0
        while left <= right:
            if left_max < right_max:
                result += max(left_max - height[left], 0)
                left_max = max(left_max, height[left])
                left += 1
            else:
                result += max(right_max - height[right], 0)
                right_max = max(right_max, height[right])
                right -= 1
        
        return result
"""
[4,2,0,3,2,5]
init: l=0 r=5
以下変化した変数
1: r_max=5, r=4
2: l_max=4, l=1
3: result+=2 → 2 l=2
4: result+=4 → 6 l=3
5: result+=1 → 7 l=4
6: result+=2 → 9
"""
```