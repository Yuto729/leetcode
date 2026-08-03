---
tags:
  - leetcode
  - review
  - algorithm
  - algorithm/binary-search
  - algorithm/recursion
  - cs/complexity
---
2025-11-22 〜 2026-07-27 の `main.md` 95 本を走査し、つまずきの記述（ヒント/答えを見た・AIに聞いた・30分以上かかった・TLE後に自力で改善できなかった・詰まった）を抽出して分類したもの。

## 総括

弱点は分野そのものより、次の3つの「型」に集約される。

1. **述語・状態を自分で定義する設計フェーズ** — 二分探索（何が単調か）と DP（何を状態に持つか）。手法名さえ与えられれば書ける、というノートの残り方が両方に共通している。[[不変条件と境界条件の設計]] / [[二分探索]]
2. **ナイーブ → 最適化 の跳躍** — TLE に当たった後、自力で計算量を落とせず外部ヒントに頼るケースが 2025-12 から 2026-07 まで途切れず出ている。**時系列で改善していない唯一の項目**。
3. **再帰 → 反復の機械的変換** — [[再帰]]。コーディング面接マニュアルが明示的に評価点として挙げている項目なので優先度が高い。

一方、DFS/BFS の素直な適用・ハッシュ・木の基本走査・文字列処理は 2026-06 以降つまずきの記述がほぼ消えており、改善済みと見てよい。

## 1. 二分探索 — 最大の弱点（しかも直近）

| 問題 | 日付 | 記述 |
| --- | --- | --- |
| [[capacity-to-ship-packages-within-d-days/main\|Capacity to Ship Packages Within D Days]] | 2026-05-30 | DP で TLE →「二分探索だけどやり方がわからないので聞いてみる」 |
| [[median-of-two-sorted-arrays/main\|Median of Two Sorted Arrays]] | 2026-06-02 | 「全然わからないので AI に教えてもらう」 |
| [[search-in-rotated-sorted-array/main\|Search in Rotated Sorted Array]] | 2026-04-20 | 40分、途中で「正解できなさそうなのでヒントをもらった」 |
| [[find-minimum-in-rotated-sorted-array/main\|Find Minimum in Rotated Sorted Array]] | 2026-04-19 | 「あと少し発想が足りなかったのでヒントをもらう」 |

共通するのは、答えそのものではなく **「何に対する単調な述語を引くか」を自分で決める段階**。
[[search-insert-position/main|Search Insert Position]] に書いたループ不変条件の議論、および Find Minimum に引用した nodchip コメント「目的を設定し、目的に必要な手段を決め、手段を粒度の大きい部分から小さい部分に向かって検討していく、という思考ができていない」と完全に一致する。

## 2. ナイーブ解 → 最適化の一段目が自力で越えられない

| 問題 | 日付 | 記述 |
| --- | --- | --- |
| [[minimum-window-substrin/main\|Minimum Window Substring]] | 2026-07-25 | TLE →「考えてもわからなかったので AI にヒント」（Two Pointer で1パス） |
| [[word-ladder/main\|Word Ladder]] | 2025-12-30 | 8000ms →「考えてもわからなかったので Claude にヒント」（逆向き生成 + set） |
| [[find-k-pairs-with-smallest-sums/main\|Find K Pairs with Smallest Sums]] | 2025-12-06 | 枝刈りしても TLE →「解答を見てみると」 |
| [[kth-largest-element-in-a-stream/main\|Kth Largest Element in a Stream]] | 2025-12-04 | 3082ms、heap で「途中で詰まってしまった」 |

AC はするが、**計算量を落とすフェーズで止まる**のが一貫パターン。直近 2026-07 でも再発している。

## 3. DP の状態設計（1次元で足りない型）

| 問題 | 日付 | 記述 |
| --- | --- | --- |
| [[paint-fence/main\|Paint Fence]] | 2026-03-29 | 「1つの DP 配列だけでは解けなかった」→ AI ヒント |
| [[longest-increasing-subsequence/main\|Longest Increasing Subsequence]] | 2026-03-31 | 「具体的な解法が思いつかなかったので AI に聞いてみる」 |
| [[best-time-to-buy-and-sell-stock-ii/main\|Best Time to Buy and Sell Stock II]] | 2026-04-12 | 「複雑に考えて思いつかなかったので解法を AI に教えてもらう」 |
| [[word-break/main\|Word Break]] | 2026-04-13 | 40分。「詰まった点: for ループの範囲 / 各所スライスのインデックス」 |
| [[coin-change/main\|Coin Change]] | 2026-04-16 | 26分。`-1` を返す分岐漏れ、初期化ミス |
| [[maximum-subarray/main\|Maximum Subarray]] | 2026-04-01 | 分割統治（4値マージ）の「理解に時間がかかった」 |

遷移そのものより、**遷移に必要な状態を1本の DP 配列に押し込もうとして詰まる**型。

## 4. 木・再帰 ↔ 反復変換

| 問題 | 日付 | 記述 |
| --- | --- | --- |
| [[balanced-binary-tree/main\|Balanced Binary Tree]] | 2026-06-24 | iterative 版が書けず、AI ヒントを4段階（post-order・高さの保持・処理済み判定・打ち切り） |
| [[split-bst/main\|Split BST]] | 2026-04-28 | 「iterative で解こうとしたが状態遷移が多くわからなかったのでヒント」 |
| [[lowest-common-ancestor-of-a-binary-tree/main\|Lowest Common Ancestor of a Binary Tree]] | 2026-07-22 | 30分 |
| [[construct-binary-tree-from-preorder-and-inorder-traversal/main\|Construct Binary Tree from Preorder and Inorder]] | 2026-03-28 | 冒頭から「AI にヒントをもらう」 |
| [[merge-two-binary-trees/main\|Merge Two Binary Trees]] | 2026-01-01 | 「中々うまくいかなかったので Claude にヒントをもらいながら」 |

再帰は書ける。**明示スタックへの機械的変換（post-order / 訪問済みフラグ）が定着していない**のが 2026-06 でも出ている。

## 5. BFS / グラフ

| 問題 | 日付 | 記述 |
| --- | --- | --- |
| [[01-matrix/main\|01 Matrix]] | 2026-06-04 | 「BFS でやろうとしてハマってしまい30分以上」（多始点 BFS） |
| [[clone-graph/main\|Clone Graph]] | 2026-06-29 | 訪問済み隣接ノードへの辺がコピーされない等で詰まる |

関連: [[DFSのvisitedを追加するタイミング]] / [[グラフ]]

## 6. Two Pointer / Sliding Window

| 問題 | 日付 | 記述 |
| --- | --- | --- |
| [[container-with-most-water/main\|Container With Most Water]] | 2026-05-25 | 「色々考えたがわからなかった。Two Pointer らしいというヒントを見て思いついた」 |
| [[minimum-size-subarray-sum/main\|Minimum Size Subarray Sum]] | 2026-04-28 | 36分 |
| [[longest_substring_without_repeating_characters/main\|Longest Substring Without Repeating Characters]] | 2025-11-22 | 「一旦解答を見てみる」 |

## 7. スタック / データ構造設計

| 問題 | 日付 | 記述 |
| --- | --- | --- |
| [[implement-queue-using-stacks/main\|Implement Queue using Stacks]] | 2026-06-25 | 「わからないので AI にヒント」（償却 O(1) の2スタック） |
| [[time-based-key-value-store/main\|Time Based Key-Value Store]] | 2026-07-22 | 30分 |

## 8. 累積和・ハッシュ

| 問題 | 日付 | 記述 |
| --- | --- | --- |
| [[subarray-sum-equals-k/main\|Subarray Sum Equals K]] | 2025-12-24 | 「累積和（ヒントを見た）」＋「答えを見ながら書いた」 |

関連: [[部分配列系問題のパターン]]

## 9. 実装・コーナーケース系（考え方ではなく手が遅い）

| 問題 | 日付 | 記述 |
| --- | --- | --- |
| [[zigzag-conversion/main\|Zigzag Conversion]] | 2026-05-10 | 45分＋簡略化のヒント |
| [[string-to-integer-atoi/main\|String to Integer (atoi)]] | 2026-05-10 | 「数々のコーナーケースに引っ掛かり30分」 |
| [[generate-parentheses/main\|Generate Parentheses]] | 2026-05-04 | 15分・2回再提出（nonlocal、引数の破壊的更新） |
| [[is-subsequence/main\|Is Subsequence]] | 2026-05-07 | 内側ループの早期 break 忘れで WA |

## 参考: トリッキー枠（今回の対象外）

- [[k-th-symbol-in-grammar/main|K-th Symbol in Grammar]]（2026-04-26）「Give up し、AI に聞く」— 再帰の対称性を見抜く発想問題
- [[next-permutation/main|Next Permutation]]（2026-05-10）「ヒントなどをみながらの考察」— 手順暗記型
- [[median-of-two-sorted-arrays/main|Median of Two Sorted Arrays]] — 1. にも挙げたが Hard 分類なので優先度は下げてよい
