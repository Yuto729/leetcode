# Flood Fill
You are given an image represented by an m x n grid of integers image, where image[i][j] represents the pixel value of the image. You are also given three integers sr, sc, and color. Your task is to perform a flood fill on the image starting from the pixel image[sr][sc].

To perform a flood fill:

Begin with the starting pixel and change its color to color.
Perform the same process for each pixel that is directly adjacent (pixels that share a side with the original pixel, either horizontally or vertically) and shares the same color as the starting pixel.
Keep repeating this process by checking neighboring pixels of the updated pixels and modifying their color if it matches the original color of the starting pixel.
The process stops when there are no more adjacent pixels of the original color to update.
Return the modified image after performing the flood fill.

Ex1.
Input: image = [[1,1,1],[1,1,0],[1,0,1]], sr = 1, sc = 1, color = 2
Output: [[2,2,2],[2,2,0],[2,0,1]]

Constraints
- m == image.length
- n == image[i].length
- 1 <= m, n <= 50
- 0 <= image[i][j], color < 2^16
- 0 <= sr < m
- 0 <= sc < n

## Step1
再帰関数の設計は、start pixelとcolorを渡して、隣接pixelをチェックしてstart pixelと同じ色なら再帰する。start pixelの色がすでに目的の色と同じならreturnする。
すでに色を変えたところに再び訪れることはない
最後にreturnを書けば再帰が収束する

- 一部sr, scをnew_sr, new_scに置き換え忘れてしまったところがあった.
- deepcopyしないと配列の中身が書き換えられてしまう

Time: O(m*n) 各セルを最大一回しか訪問しない
Space: O(m*n) 全セルが同じ色でシグザグに連結している時の最悪計算量
最大50*50 = 2500 > 1000(Pythonのデフォルト再帰制限)なのでオーバーフローする可能性がある

```py
class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        if not image:
            return [[]]
        
        new_image = copy.deepcopy(image)
        m = len(new_image)
        n = len(new_image[0])
        def flood_fill_from(sr, sc, color):
            original = new_image[sr][sc]
            if original == color:
                return

            new_image[sr][sc] = color
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dr, dc in directions:
                new_sr = sr + dr
                new_sc = sc + dc
                if not (0 <= new_sr < m and 0 <= new_sc < n):
                    continue
                
                if image[new_sr][new_sc] != original:
                    continue
                
                flood_fill_from(new_sr, new_sc, color)
            
            return
        
        flood_fill_from(sr, sc, color)
        return new_image
```
### test case
- image = [[1,1,1],[1,1,0],[1,0,1]], sr = 1, sc = 1, color = 2
- image = [[0,0,0],[0,0,0]], sr = 0, sc = 0, color = 0
- image = [[1,1,1],[1,1,1],[1,1,1]], sr = 1, sc = 1, color = 2
- image = [[1,1,1],[1,1,0],[1,0,1]], sr = 0, sc = 0, color = 2
- image = [[0]], sr = 0, sc = 0, color = 1
- image = [[1,1,1,1],[1,1,0,1],[1,0,1,1]], sr = 1, sc = 1, color = 2 ** 16 - 1

## コードレビュー
1. パラメータ名のシャドウイング
外側の `sr`, `sc` を内側の関数でも使っているのは混乱の元です。
```python
def flood_fill_from(sr, sc, color):  # 外のsr, scを隠してしまう
```
→ `r, c` など別名を使うのが無難です。
2. `image` と `new_image` の混在
ネストした関数の中で `image`（元の配列）と `new_image`（コピー）が混在しています:
```python
original = new_image[sr][sc]   # new_image から読む
...
if image[new_sr][new_sc] != original:  # image で確認
```
これは「訪問済みかどうかは `new_image` で判定（色が変わっていれば訪問済み）、隣接チェックは元の `image` で行う」という意図ですが、読み手には伝わりにくいです。

3. 末尾の `return` は不要
```python
            return  # ← 書かなくて良い
        
        flood_fill_from(sr, sc, color)
        return  # ← 同様
```

- floodfillが、入力が変更されることが前提ならin-placeで良い
    - 副作用があっても良い前提で変更した`image`を返すのはちょっと違和感。

- 2Dならdeepcopyじゃなくて、`[row[:] for row in image]`でも十分
    - `[row[:] for row in image]`は内側のリストもコピーするかつ配列の要素（整数）はイミュータブルなので問題ない
    - deepcopyは配列の要素、つまりintもコピーするのでオーバーヘッドが大きい
    - shallow copyだと内側のリストは共有されるので要素の変更が伝播する
    - 3D以上の配列だと要素の変更は伝播する。コピーされるのは内側の2Dリストまでなので、2Dリストの各要素、つまりさらに内側のリストは共有されてしまっているため

### follow up
- 再帰のオーバーフローは大丈夫？配列のサイズが大きくなったら？
    - BFS, BFS（スタック）など

スタックを用いる
```py
class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        if not image:
            return [[]]
        
        new_image = [row[:] for row in image]
        m = len(new_image)
        n = len(new_image[0])
        stack = [(sr, sc)]
        while stack:
            r, c = stack.pop()
            original = new_image[r][c]
            if original == color:
                continue

            new_image[r][c] = color
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dr, dc in directions:
                new_r = r + dr
                new_c = c + dc
                if not (0 <= new_r < m and 0 <= new_c < n):
                    continue
                
                if new_image[new_r][new_c] != original:
                    continue
            
                stack.append((new_r, new_c))
        
        return new_image
```

## Step2

### キューに積む前に色を塗り替えると関数呼び出し回数が減る

[huyfififi#9](https://github.com/huyfififi/coding-challenges/pull/9)

> queueやcall stackに積む数を減らすために、新しい要素をqueue・call stackに入れる前に`visited`のフラグを立てておく（今回の場合色を先に塗り替えておく）こと

塗りつぶすマスを `k` とすると:
- 積む前にチェック: 関数呼び出し `k` 回
- 積んでからチェック: 関数呼び出し `4k` 回

計算量は変わらないが、呼び出しのオーバーヘッドが違う。BFSのシンプルな書き方にもなる。

### 範囲チェックを関数に切り出す

[kitano-kazuki#76](https://github.com/kitano-kazuki/leetcode/pull/76)

> 配列外参照していないかどうかの判定であり、比較的すぐわかりやすい判定の部類だと思うので、early return などせず単に
> ```python
> return 0 <= row < num_rows and 0 <= col < num_col
> ```

`is_in_bounds` などに切り出すとループ内がすっきり

## Step3
- `if color_to_replace == color:`を忘れずに
    - visitedを使うDFSと違って、「色が変わったか」で訪問済みを判定しているので、色が変わらないケースでDFSが破綻する
    
```py
class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        m, n = len(image), len(image[0])
        color_to_replace = image[sr][sc]
        if color_to_replace == color:
            return image

        image[sr][sc] = color
        stack = [(sr, sc)]
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        while stack:
            r, c = stack.pop()
            for dr, dc in directions:
                new_r = r + dr
                new_c = c + dc
                if not (0 <= new_r < m and 0 <= new_c < n):
                    continue
                
                if image[new_r][new_c] != color_to_replace:
                    continue
                
                image[new_r][new_c] = color
                stack.append((new_r, new_c))
        
        return image
```

## 類題

- [number-of-islands](../number-of-islands/)
- [max-area-of-island](../max-area-of-island/)
- [count-connected-components](../count-connected-components/)