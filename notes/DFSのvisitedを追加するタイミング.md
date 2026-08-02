---
tags:
  - leetcode
  - algorithm/graph
  - algorithm/dfs
  - algorithm/bfs
  - algorithm/recursion
  - algorithm/component
  - algorithm
---

# DFS/BFS で visited に追加するタイミング

## 結論

`visited` への追加は **push のタイミング**（= ノードをスタック／キューに積むとき）で行う。pop のタイミングで行うと、同じノードが複数回積まれる。

そして本質は「再帰か反復か」ではなく、**push と pop の間に時間差があるか**である。

- **再帰**: 再帰呼び出し = push + 即座に処理。push と pop が同時なので、時間差の窓が存在しない。よって「どのタイミングで marking するか」という問題自体が発生しない
- **反復**: push してから pop されるまでに他のノードが処理されうる。**その窓の間に、別のノードから同じノードが再び push されうる**

BFS のキューでも全く同じ話になる。

## 再帰版: 窓が無い

```py
def dfs(node, component):
    for neighbor in graph[node]:
        if neighbor in visited:
            continue

        visited.add(neighbor)
        dfs(neighbor, component)      # ← ここで部分木を全部処理し切ってから戻る
        component.append(neighbor)
```

`dfs(neighbor)` が完了するまで次の `neighbor` を見ない。したがって2つ目の隣接ノードを検査する時点で、1つ目の部分木に含まれる全ノードは既に `visited` に入っている。重複は起こりえない。

## 反復版: pop で marking すると重複する

```py
# NG: pop で marking
while stack:
    node = stack.pop()
    if node in visited:      # ← このガードが無いと二重処理
        continue

    visited.add(node)
    component.append(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            stack.append(neighbor)     # まだ visited に入っていないので何度でも積まれる
```

ノード X が A と B の両方に隣接していて、A と B が先に処理された場合、X は**2回スタックに積まれる**。ガードがあるので答えは合うが、

- スタックが最大 O(E) まで膨らむ（頂点数ではなく辺数のオーダー）
- `component.append` を push 側に書いていると **二重計上して答えが壊れる**

## 反復版: push で marking する（正しい形）

```py
visited.add(start)
component = []
stack = [start]
while stack:
    node = stack.pop()
    component.append(node)
    for neighbor in graph[node]:
        if neighbor in visited:
            continue

        visited.add(neighbor)      # ← push と同時に marking
        stack.append(neighbor)
```

積む瞬間に `visited` へ入れるので、同じノードが2回積まれない。スタックサイズは O(V) に収まり、pop 時のガードも不要になる。

**開始ノードだけは呼び出し前に `visited.add` しておく**必要がある（ループの中では隣接ノードしか marking しないため）。

## なぜ反復にするのか（再帰の危険性）

Python のデフォルト再帰上限は 1000。グラフが鎖状に伸びていると、再帰の深さがそのまま入力の形に晒される。

Accounts Merge（LeetCode 721、制約 `accounts.length <= 1000`）で実測した例:

```py
# 一本鎖 e0-e1-...-e1000 を作る入力（制約内）
accounts = [["X", "e%d" % i, "e%d" % (i+1)] for i in range(1000)]
```

| 探索の開始位置 | 最大再帰深さ | 結果 |
| --- | --- | --- |
| 鎖の中央 | 501 | OK（左右に分かれるので半分） |
| 鎖の端点 | 1000 | **RecursionError** |

さらに厄介なのは、開始位置を決めるのが**イテレーションの順序**である点。

- `for email in all_emails:`（set）→ ハッシュ順なので開始位置が不定 → **落ちたり落ちなかったりする**
- `for email in email_to_name:`（dict）→ 挿入順なので端点から必ず開始 → **常に落ちる**

フレーキーに落ちるより常に落ちる方が発見しやすいが、いずれにせよ再帰のままでは危険。

対して **Union-Find の `find` は union-by-size で木の高さが O(log n) に保証される**ので、再帰でも安全（要素1万件で深さ14程度）。同じ「再帰」でも、深さがデータ構造によって保証されているか入力形状に晒されているかで安全性が全く違う。

## 関連

- [[グラフ]]
- [[再帰]]