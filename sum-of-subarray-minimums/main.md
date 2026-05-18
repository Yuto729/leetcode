メガベンチャーのコーディングテストで出てきた問題の類題

出てきた問題* int型の配列numsが引数になっている。任意のインデックスiに対して、nums[i]が部分配列内で最大の値をとる唯一の要素であり、部分配列の最初または最後の要素がnums[i]となる部分配列の個数を各iについて記録した配列を答えとして返す関数を作成する
Ex. [3,4,1,6,2] -> [1,3,1,5,1]


類題
907. Sum of Subarray Minimums
https://leetcode.com/problems/sum-of-subarray-minimums

ナイーブに解く
```py
class Solution:
    def sumSubarrayMins(self, arr: List[int]) -> int:
        result = 0
        MODULO = 10 ** 9 + 7
        # iで終わるsubarray
        for i in range(len(arr)):
            min_of_subarray = arr[i]
            for j in range(i, -1, -1):
                min_of_subarray = min(min_of_subarray, arr[j])
                result += min_of_subarray
        
        return result % MODULO
```

最適化をする
- 各iに対して、「arr[i]が最小となるサブ配列の個数を数える」
    - arr[i]を最小値として含むサブ配列は左右にどこまで伸ばせるかで決まる
    - arr[i]より小さい要素が左に現れる直前までの距離 -> left[i]
    - arr[i]より小さい要素が右に現れるまでの直前の距離 -> right[i]
- arr[i]が最小になるサブ配列の数はleft[i] * right[i]でもとまる

Time: O(n) -> スタックに追加されてpopされる回数はたかだか各要素に対して一回だけなので、`stack.pop()`をforループ全体に均して考えると、O(n)になる。
Space: O(n)
```py
class Solution:
    def sumSubarrayMins(self, arr: List[int]) -> int:
        n = len(arr)
        MOD = 10 ** 9 + 7
        # arr[i]より小さい直近の左インデックス（なければ-1）
        left = [0] * n
        # arr[i]より小さい直近の右インデックス（なければ-1）
        right = [0] * n
        stack = []
        for i in range(n):
            while stack and arr[i] <= arr[stack[-1]]:
                stack.pop()
            left[i] = stack[-1] if stack else -1
            stack.append(i)
        
        stack = []
        for i in range(n - 1, -1, -1):
            # 重複を除去するために条件を強める
            while stack and arr[i] < arr[stack[-1]]:
                stack.pop()
            right[i] = stack[-1] if stack else n
            stack.append(i)
        
        result = 0
        for i in range(n):
            count = (i - left[i]) * (right[i] - i)
            result += arr[i] * count
        
        return result % MOD
```

不変条件
leftループについて
- スタックについて、自分より前に入れた要素は自分より必ず小さい -> つまりarr[stack[0]] < arr[stack[1]] ... arr[stack[-1]]
- stackに入れたインデックスは昇順になる。
- stackに残っているindex jは、「jから見て右にまだarr[j]以下の要素が出現していない」候補
stack[-1]がarr[i]より狭義に小さい直近の左indexになる。

## 単調スタック (Monotonic Stack) の使い所

以下のような「各要素について、左右の **最も近い** 〜な要素を求めたい」問題で威力を発揮する。

- **Next Greater / Next Smaller Element**: 各要素より大きい/小さい直近の要素を求める
- **寄与度 (contribution) で総和を分解する問題**: 「全サブ配列の min/max/特定の関数の総和」を、各要素が担当する範囲の積で表現する
- **ヒストグラム系**: 棒グラフを覆う最大長方形、各棒について左右の「これより低い棒」までの距離
- **区間の境界探索**: 各 index `i` について、ある条件を満たす最遠/最近の index を O(1) amortized で取得

### 判断のサイン

1. 「全サブ配列 / 全区間に対する集計」が要求されている
2. ナイーブが O(N²) で TLE
3. 各要素について「左右に伸ばせる範囲」が個別に決まり、その積/和で答えが構成できる
4. データ構造に index を積むと、新しい要素が来たときに **単調性を保つために pop** できる

### 増加/減少の使い分け

| 求めたいもの | スタック | pop条件 |
|------|--------|---------|
| Next Smaller (より小さい直近) | 増加スタック | top >= cur で pop |
| Next Greater (より大きい直近) | 減少スタック | top <= cur で pop |
| 同値の重複回避 | 片側を strict, もう片側を non-strict | 上記参照 |

## 類題

- **LC 84. Largest Rectangle in Histogram**: 各棒について「左右でこれより低い棒」までの距離を求めて面積の最大を取る。本問の双子。
- **LC 85. Maximal Rectangle**: 84 を 2D に拡張。各行をヒストグラムとして処理。
- **LC 496. Next Greater Element I** / **LC 503. Next Greater Element II** (循環): 単調スタックの基本形。
- **LC 739. Daily Temperatures**: 各日について次に温度が上がる日までの日数。Next Greater の典型。
- **LC 901. Online Stock Span**: ストリーミングで Next Greater を更新。
- **LC 2104. Sum of Subarray Ranges**: 本問 (min) と max の差の総和。本問の解法を min/max 両方で動かす。
- **LC 1856. Maximum Subarray Min-Product**: 各要素が最小となる範囲 × その範囲の和の最大。本問とprefix sumの組合せ。
- **LC 42. Trapping Rain Water**: 単調スタックでも解ける（two pointerが主流だが）。
