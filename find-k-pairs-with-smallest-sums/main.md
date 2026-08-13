---
tags:
  - leetcode
---

## Step1
nums1, nums2の全ペアを計算するのは問題の制約上確実にTLEになるので, 合計値が最小のk個のペアが揃ったら即returnする方法を考えたい. 
nums1, nums2はソート済みであるので後ろのペアは見なくていい.
- 新しい組を追加したときに最小のk個が維持されるようにする => heapを用いる. 
- 単純な二重ループだとTLEするので, 枝刈りをしてループの回数を減らす.

以上の実装を行ったがTLEは解消されなかった.
```py
class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        pairs = []

        for i in range(len(nums1)):
            for j in range(len(nums2)):
                if pairs and nums1[i] > pairs[0][1] and nums2[j] > pairs[0][2] and len(pairs) == k:
                    break

                heapq.heappush(pairs, (- nums1[i] - nums2[j], nums1[i], nums2[j]))
                if len(pairs) > k:
                    heapq.heappop(pairs)

        return [[u, v] for _, u, v in pairs]
```

https://leetcode.com/problems/find-k-pairs-with-smallest-sums/solutions/6638440/unlock-the-min-heap-strategy-for-finding-3b61/
解答を見てみると, (i, j)に対して, (i + 1, j) or (i, j + 1)に遷移している. Dijkstraっぽい動き.
前から順にイテレーションしていくやり方だと, 次のペアが現在のペアの合計値より大きいとは限らないので非効率な探索になってしまう. 答えの長さがkになったら即打ち切るには,
各ループの中で、未探索のペアの中から最小の合計値を持つペアを加える必要がある. また, non decreasing orderなので(i, j)に対して, (i + 1, j) or (i, j + 1)が次の候補になる.（つまり隣接ノードをheapに
加えながら探索するのでDijkstraっぽい）
今回はheapを次の候補を探すための格納庫として使う. 前の問題のようにheap自体に答えを詰め込んでいくものだと決め打ちしてしまっていると解くことができない.
heapに追加されるノードが(i, j)だとして, (i-1, j), (i, j-1)の2ノードから到達できてしまうので,`visited`を用いてすでに探索したかどうかを記録しておく必要がある.

時間計算量: ループの回数×(ループ内でのpop, pushの計算量)と考えられる. ループの回数はO(k), heapはループ一回につき1回pop, 2回pushされるので多くてもサイズkであり、pop, pushの計算量はO(logk)
よって, O(klogk).
空間計算量: set + heap, O(k)
```py
class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        visited = set()
        visited.add((0, 0))
        min_heap = [(nums1[0] + nums2[0], 0, 0)]
        k_pairs_with_smallest_sum = []

        while min_heap and len(k_pairs_with_smallest_sum) < k:
            _, i, j = heapq.heappop(min_heap)
            k_pairs_with_smallest_sum.append([nums1[i], nums2[j]])

            # 境界条件
            if i + 1 < len(nums1) and (i + 1, j) not in visited:
                visited.add((i + 1, j))
                heapq.heappush(min_heap, (nums1[i + 1] + nums2[j], i + 1, j))
            if j + 1 < len(nums2) and (i, j + 1) not in visited:
                visited.add((i, j + 1))
                heapq.heappush(min_heap, (nums1[i] + nums2[j + 1], i, j + 1))

        return k_pairs_with_smallest_sum
```

# Step2
実はvisitedが不要なやり方がある. nums1の最初のk行だけpushしておくと, (i,j)に対して(i,j+1)を探索すれば良くなるので重複することがなくなる.
- 初期候補: (i,0)(i=0..k-1)
- nums1[k]以降は使われない. 実際(k,j)よりも(i,j)(i <= k-1)を選ぶほうが和が小さくなるのでそれでいい.

時間計算量: ループの回数はk回で, pop,pushの計算量はO(min(k, nums1))
```py
class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        if not nums1 or not nums2:
            return []

        min_heap = []
        k_pairs_with_smallest_sum = []

        for i in range(min(k, len(nums1))):
            heapq.heappush(min_heap, (nums1[i] + nums2[0], i, 0))

        while min_heap and len(k_pairs_with_smallest_sum) < k:
            _, i, j = heapq.heappop(min_heap)
            k_pairs_with_smallest_sum.append([nums1[i], nums2[j]])

            if j + 1 < len(nums2):
                heapq.heappush(min_heap, (nums1[i] + nums2[j + 1], i, j + 1))

        return k_pairs_with_smallest_sum
```
少しだけRuntimeが改善した. 

別のやり方として,(i+1, j) は j == 0 のときだけpushするというやり方がある. こうすることで, (i, j)(j != 0)は(i, j-1)からの遷移に限定されるので重複を防げる.
```py
class Solution:
    def kSmallestPairs(self, nums1, nums2, k):
        if not nums1 or not nums2:
            return []

        min_heap = [(nums1[0] + nums2[0], 0, 0)]
        k_pairs_with_smallest_sum = []
        while min_heap and len(k_pairs_with_smallest_sum) < k:
            _, i, j = heapq.heappop(min_heap)
            k_pairs_with_smallest_sum.append([nums1[i], nums2[j]])
            # (i, j+1) は常に push
            if j + 1 < len(nums2):
                heapq.heappush(min_heap, (nums1[i] + nums2[j + 1], i, j + 1))
            # (i+1, j) は j == 0 のときだけ push
            if j == 0 and i + 1 < len(nums1):
                heapq.heappush(min_heap, (nums1[i + 1] + nums2[j], i + 1, j))

        return k_pairs_with_smallest_sum


```
### コメントなどを見る
```py
if i + 1 < len(nums1) and (i + 1, j) not in visited:
    visited.add((i + 1, j))
    heapq.heappush(min_heap, (nums1[i + 1] + nums2[j], i + 1, j))
if j + 1 < len(nums2) and (i, j + 1) not in visited:
    visited.add((i, j + 1))
    heapq.heappush(min_heap, (nums1[i] + nums2[j + 1], i, j + 1))
```
ここの部分の関数化は書いている最中にちょっと思った.
https://discord.com/channels/1084280443945353267/1200089668901937312/1222573940610695341

https://discord.com/channels/1084280443945353267/1201211204547383386/1206515949579145216
リファクタリング、関数化

```py
class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        visited = set()
        visited.add((0, 0))
        min_heap = [(nums1[0] + nums2[0], 0, 0)]
        k_pairs_with_smallest_sum = []
        def add_to_heap_if_necessary(x, y):
            if x < len(nums1) and y < len(nums2) and (x, y) not in visited:
                heapq.heappush(min_heap, (nums1[x] + nums2[y], x, y))
                visited.add((x, y))
    
        # 問題文的にはlen(k_pairs_with_smallest_sum)はk以上あるが,そうではないない場合を考慮して以下のように書くほうが望ましい.
        while len(k_pairs_with_smallest_sum) < k and min_heap:
            _, i, j = heapq.heappop(min_heap)
            k_pairs_with_smallest_sum.append([nums1[i], nums2[j]])
            add_to_heap_if_necessary(i + 1, j)
            add_to_heap_if_necessary(i, j + 1)

        return k_pairs_with_smallest_sum
```


## Step3
```py
class Solution:
    def kSmallestPairs(self, nums1, nums2, k):
        visited = set()
        visited.add((0, 0))
        min_heap = [(nums1[0] + nums2[0], 0, 0)]
        k_pairs_with_smallest_sum = []

        def push_to_heap(x, y):
            if x < len(nums1) and y < len(nums2) and (x, y) not in visited:
                visited.add((x, y))
                heapq.heappush(min_heap, (nums1[x] + nums2[y], x, y))
    
        while len(k_pairs_with_smallest_sum) < k and min_heap:
            _, i, j = heapq.heappop(min_heap)
            k_pairs_with_smallest_sum.append([nums1[i], nums2[j]])
            push_to_heap(i + 1, j)
            push_to_heap(i, j + 1)
        
        return k_pairs_with_smallest_sum
```