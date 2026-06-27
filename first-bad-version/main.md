# 278. First Bad Version

You are a product manager and currently leading a team to develop a new product. Unfortunately, the latest version of your product fails the quality check. Since each version is developed based on the previous version, all the versions after a bad version are also bad.

Suppose you have n versions [1, 2, ..., n] and you want to find out the first bad one, which causes all the following ones to be bad.

You are given an API bool isBadVersion(version) which returns whether version is bad. Implement a function to find the first bad version. You should minimize the number of calls to the API.

Example 1:
Input: n = 5, bad = 4
Output: 4
Explanation:
call isBadVersion(3) -> false
call isBadVersion(5) -> true
call isBadVersion(4) -> true
Then 4 is the first bad version.

Example 2:
Input: n = 1, bad = 1
Output: 1

1 <= bad <= n <= 2^31 - 1

# Step1

2^31だと, 大体10^9程度なのでO(n)だとTLEする。
それぞれのバージョンについて、BadであればTrue, BadでなければFalseを割り当てると、
[False, False, ... True, True...] 初めてTrueになるインデックス + 1が初めてBadになるバージョンである。単調性があるので二分探索が使える

最初以下のように書いてしまったが、なぜか通った。
おそらく`isBadVersion(0)`がFalseを返すように設計されているからだろう

Time: O(logN)

```py
class Solution:
    def firstBadVersion(self, n: int) -> int:
        left = 0
        right = n
        while left < right:
            mid = (left + right) // 2
            if not isBadVersion(mid):
                left = mid + 1
            else:
                right = mid

        return left
```

正確には以下のように初期値を設定する

```py
class Solution:
    def firstBadVersion(self, n: int) -> int:
        left = 1
        right = n + 1
        while left < right:
            mid = (left + right) // 2
            if not isBadVersion(mid):
                left = mid + 1
            else:
                right = mid

        return left
```

上記の回答が最適解な理由

- n 個のバージョンの中で False/True の境界が1か所、それがどこにあるか特定するには、情報理論的に最低でも log2(n)回の二択判定が要る

この log2(n) という下界は次のように示せる。呼び出し回数がこれより少なくできない理由を2通りで説明できる。

### 決定木による数え上げ

`isBadVersion` を呼んで True/False を見て次の行動を決めるどんなアルゴリズムも、実行は二分木で表せる。ノードが1回の問い合わせ、枝が True/False の2本、葉が答えを確定して返す瞬間。

n = 5 で実際に二分探索が生成する木は次のようになる。

```
                    isBadVersion(3)?
                   /                \
               True                  False
                |                       |
          isBadVersion(2)?        isBadVersion(5)?
            /        \              /          \
         True       False        True         False
          |        return 3        |        (答えは6、到達しない)
    isBadVersion(1)?        isBadVersion(4)?
      /        \              /        \
   True       False        True       False
  return 1   return 2     return 4    return 5
```

葉は return 1〜5 の5枚必要になる。なぜなら5通りの入力（答えが1〜5）をそれぞれ違う葉に運ばないと、同じ葉に着いた2つのうち片方で必ず誤答するから。たとえば答え=1 と答え=2 は最後の `isBadVersion(1)` の返り値だけで分かれている。よって葉は最低 n 枚必要。

一方、深さ d の二分木が持てる葉は最大 2^d 枚。この2つを合わせると

```
n ≤ 葉の枚数 ≤ 2^d
```

から `2^d ≥ n`、すなわち `d ≥ log2(n)`。n が「区別すべき答えの数 = 必要な葉の数」から来て、2^d が「深さ d の木が持てる葉の最大数」から来ている。

右下の「答えは6」の枝は、version 5 すら bad でない場合に対応するが、問題は version n が必ず fail すると保証しているので、有効な入力では到達しない。

### 敵対者論法

意地悪な出題者を想像する。出題者は答えを最初に固定せず、質問に対して残る候補が多い方の答えを返す。

候補が C 個あるとき、`isBadVersion(mid)` という1回の質問は候補集合を必ず2グループに分ける。True を返す候補の集合と False を返す候補の集合で、合計は C。2つの数を足して C なら大きい方は必ず C/2 以上なので、出題者は大きい方が残る答えを返せる。mid をどう選んでもこの性質は消せない。

たとえば候補 {1,2,3,4,5} に mid=3 と聞くと {1,2,3} と {4,5} に分かれ、出題者は True と答えて3個残す。mid=4 だと {1,2,3,4} と {5} に分かれ、4個残せてもっと悪い。

よって1回の質問で確実に減らせるのは多くても半分。C を1個に絞るには C → C/2 → C/4 → ... → 1 と半分にする操作が log2(n) 回要る。

### なぜ1ビットで半分が限界か

質問する前から各候補がどちらの答えを返すかは決まっている。二択の答えは候補集合を必ず2グループに分割し、合計は C 個なので大きい方は必ず C/2 以上ある。最悪ケースではその大きい方が残る。だから減らせるのは多くても C/2 まで。

逆に mid を真ん中に選ぶと2グループがちょうど半々になり、最悪でも半分を常にちょうど半分にできる。これが二分探索が下界 log2(n) をぴったり達成して最適である理由。

もし API が True/False/わからない の3値を返すなら、1回で1/3に絞れるので下界は log3(n) になる。`isBadVersion` は二択しか返さないから底が2になる。

## 補足: badという入力について

`bad` は問題の答え、つまり「最初に不良になるバージョンの番号」であり、テストケースを定義するために与えられている。自分が書く関数の入力ではない。

入力には2つのレイヤーがある。

1. 自分の関数が受け取るもの: `n`（バージョンの総数）と API `isBadVersion(version)`
2. 採点システムが内部で持つもの: `bad`（正解）

採点システムは内部的に `isBadVersion(version)` を `version >= bad` で実装している。だから自分のコードから `bad` を直接参照することはできず、`isBadVersion` を呼んで False から True に切り替わる境界を探すことになる。

## 補足: isBadVersion(0)について

最初の `left = 0` 版が通ったのは、`isBadVersion(0)` が `0 >= bad`（`bad >= 1`）で必ず False を返すから、という推論で正しい。

ただしこれは保証された仕様ではなく実装詳細に依存している。問題文の契約は「バージョンは [1, ..., n]」なので、`isBadVersion(0)` は契約の外側を叩いている。今回は偶然 False が返って助かったが、本物のサービスなら存在しないバージョン 0 への問い合わせは例外を投げるかもしれない。さらに問題は呼び出し回数の最小化を求めているのに、必ず False と分かっている 0 への呼び出しを1回無駄にしている。n = 1 で並べると、`left = 1` 版は `isBadVersion(1)` の1回だけ、`left = 0` 版は `isBadVersion(0)` を余分に1回挟む。動くから良いではなく、契約の中だけで動かす方が筋が良い。

`left = 1, right = n + 1` は、答えの取りうる最小値と最大値+1を端に置く lower_bound の定石で、契約内に収まっている。

## 補足: オーバーフローについて

`mid = (left + right) // 2` は Python では問題ないが、C++ や Java では `left + right` が int の上限を超えうる。その場合は `mid = left + (right - left) // 2` と書く。

# Step2

まとめ

### 全バージョンが good のとき何を返すか、という設計判断

[naoto-iwase#68](https://github.com/naoto-iwase/leetcode/pull/68/changes)

> すべてのversionがfineなときは分かりやすく-1を返すことにする。（未来の次のバージョンを返すのは違和感がある。）
> 「不良が必ず存在する」という前提を外したときに `n+1`（存在しないバージョン）を返すのは不自然なので、明示的に -1 を返す。シグネチャの意味づけまで踏み込んだ判断。

### 不変条件の等号の入れ方で4パターンあり、返り値の考えやすさが変わる

[naoto-iwase#68](https://github.com/naoto-iwase/leetcode/pull/68/changes)

> 不変条件の設定の仕方は等号を含めるかどうかで2x2=4パターンあるが…2つ目に書いた方は、4パターンの中で唯一 mid = (left + right + 1) // 2 の+1が必要だったりする。
> `left = mid`（mid を縮めない側）を使う実装では、`mid` が下に偏ると無限ループするため `+1` で切り上げが必要になる。最終的に `i < left` と `i >= right` の不変条件にすると返り値が `right` で素直になる、と Step3 で結論づけている。境界設計を体系的に整理した良い記録。

### left/right は「左の何か」が抜けた名前 — 業務日誌のたとえ

[huyfififi#14](https://github.com/huyfififi/coding-challenges/pull/14)

> 二分探索をする仕事をシフト制でやるとして、職場に行ってみたら「左が100で右が200」とだけ書いてある業務日誌があったら昨日働いていた人に電話しませんか。「左と右ってどういう意味なのか。」…本当は、「左が100」で表現したいことは「..., 98, 99 までは good を確認したが 100 とそれ以降は未確認」…
> 変数名が表すべきは「位置」ではなく「どこまで確認済みか」という不変条件。ブリーフィング（＝コメントや docstring で不変条件を共有）しておけば短い名前でも電話せずに済む、という命名と不変条件の本質を突いた説明。

### left_i にしても解決にならない — 知りたいのはそこではない

[huyfififi#14](https://github.com/huyfififi/coding-challenges/pull/14)

> left を left_i にするというのは、電話をしたときに「あー、ごめん、左はもちろん、左のインデックスという意味だよ!」と返事をするようなもので、知りたいところはそこではないので、ほとんど読む助けにならないのですね。
> `i`（index）を足しても「good確認済みの最大か / 未確認の最小か」という肝心の意味は伝わらない。命名で足すべき情報の質を見極める指摘。

### good_left / bad_right という名前は「good の左端」と誤読されうる

[kitano-kazuki#83](https://github.com/kazuki-official/leetcode/pull/83/changes)

> good*leftというネーミングですが、goodの左端？ということを想起させる可能性があり、若干わかりにくい気がしました。bad_rightについても同様です。…(last*)good*version と(first*)bad_versionがの方が意味的には正しいと思います。
> ポインタが指すのは「最後に good と確認した版」「最初に bad と確認した版」なので、`last_good_version` / `first_bad_version` の方が意味と一致する。位置（left/right）ではなく意味（last good / first bad）で命名するという指針。

# Step3

```py
class Solution:
    def firstBadVersion(self, n: int) -> int:
        # 不変条件: [1, left)はgood確定 / [right, n)はbad確定
        # 最初のbad versionは常に[left, right]の中にいる
        left = 1
        right = n + 1
        while left < right:
            mid = (left + right) // 2
            if not isBadVersion(mid):
                left = mid + 1
            else:
                right = mid

        if left == n + 1: # 全部goodのケース
            return -1

        return left
```

left / rightを意味で命名する場合、区間を調整する必要がある
n = 1の場合はwhileループに入らないエッジケースなので最初に処理する。また、全部がgoodのケースは、上記と異なりループの外でチェックしないと検知できない。(first_bad_version = nとおいているため、nがbadである前提なので)

```py
class Solution:
    def firstBadVersion(self, n: int) -> int:
        if isBadVersion(1):
            return 1

        if not isBadVersion(n): # 全部goodのケース
            return -1

        last_good_version = 1
        first_bad_version = n
        while first_bad_version - last_good_version > 1:
            mid = (first_bad_version + last_good_version) // 2
            if isBadVersion(mid):
                first_bad_version = mid
            else:
                last_good_version = mid

        return first_bad_version
```
