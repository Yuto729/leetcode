# Accounts Merge

Given a list of accounts where each element accounts[i] is a list of strings, where the first element accounts[i][0] is a name, and the rest of the elements are emails representing emails of the account.

Now, we would like to merge these accounts. Two accounts definitely belong to the same person if there is some common email to both accounts. Note that even if two accounts have the same name, they may belong to different people as people could have the same name. A person can have any number of accounts initially, but all of their accounts definitely have the same name.

After merging the accounts, return the accounts in the following format: the first element of each account is the name, and the rest of the elements are emails in sorted order. The accounts themselves can be returned in any order.

Ex.

Input: accounts = [["John","johnsmith@mail.com","john_newyork@mail.com"],["John","johnsmith@mail.com","john00@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]
Output: [["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]

Explanation:
The first and second John's are the same person as they have the common email "johnsmith@mail.com".
The third John and Mary are different people as none of their email addresses are used by other accounts.
We could return these lists in any order, for example the answer [['Mary', 'mary@mail.com'], ['John', 'johnnybravo@mail.com'], 
['John', 'john00@mail.com', 'john_newyork@mail.com', 'johnsmith@mail.com']] would still be accepted.

## Step1

Union Findっぽいと思ったが、Union Findを忘れていた。他の解法が思いつかないのでヒントを見る。

> Hint 1
> For every pair of emails in the same account, draw an edge between those emails. The problem is about enumerating the connected components of this graph.

なるほど、全mailでグラフを作成して、連結成分を列挙すれば良いのか。
「同じメールを含むアカウントは同一人物」という同値関係に基づいてアカウントをグルーピングする。
アカウントの集合を以下のように簡略化して考えてみる。

- [1,a,c,b]
- [2,b,e]
- [3,c,d]
- [4,f,g]

こんな感じのグラフになる（各辺は双方向エッジ）
a - c - d
|
b - e

f - g
連結成分は2個で、アカウントも2個だけになる

- 同じアカウントのメール同士は双方向のエッジで繋げ、グラフを構築する
- 重複なしのメールのリストを作り、これを走査して連結成分を見つけていく
- 連結成分が1つ見つかったら、並び替えてアカウント名とともに整理する

### 実装1

N=accounts.length, L=accounts[i].length
Time: O(NLlog(NL)) 最悪計算量
Space: O(NL^2) 総当たりでグラフを構築しているため

```py
class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        graph = defaultdict(list) # リストにし忘れていた。
        email_to_name = {}
        for account in accounts:
            name = account[0]
            for email in account[1:]:
                email_to_name[email] = name
            if len(account) == 2: # これ考慮するの忘れてた & len(account) == 1にしてた
                graph[account[1]] = []
                continue

            for i, j in itertools.combinations(range(1, len(account)), 2):
                graph[account[i]].append(account[j]) # リストにし忘れ
                graph[account[j]].append(account[i])

        visited = set()
        def dfs(node, path):
            for neighbor in graph[node]:
                if neighbor in visited:
                    continue

                visited.add(neighbor)
                path.append(neighbor)
                dfs(neighbor, path)

        emails = list(graph.keys())
        merged_accounts = []
        for email in emails:
            if email in visited: # 完全に忘れてた
                continue

            visited.add(email)
            path = [email]
            dfs(email, path)
            merged_account = [email_to_name[email]]
            merged_account.extend(sorted(path))
            merged_accounts.append(merged_account)

        return merged_accounts
```

- `len(account) == 2`の分岐が書きづらすぎるのでシンプルにしたい
  - `graph.keys()`を全メール一覧として扱っていることが原因
  - グラフ一覧は別のループで構築すればこの分岐は必要なくなる
  - 「全メールの集合」と「グラフの構築」は別の関心事

- 1アカウントの全メール同士を総当たりで辺にしているが、k件のメールに対してO(k^2)の辺ができる。連結成分を求めるだけなら全部が繋がっていればいいので、先頭のメールとその他のメールを繋げるだけで良い O(k)
  - 先頭のメールアドレスを経由して同じアカウント内のその他のメールアドレスに辿り着ける構造であればok
  - エッジは双方向である必要がある
  - 総当たりと同値関係が同じになる最も簡単なグラフ構造にするのが良い
    - つまり**全域木**

- `path`を変更しているが、returnして呼び出し側で受け取る方が良い

- 命名
  - `path` -> 集めているのは連結成分であって、経路ではないので`component`や`group`の方がいい

### 実装1 改善

上記の点を反映

```py
class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        graph = defaultdict(list)
        email_to_name = {}
        for account in accounts:
            name = account[0]
            for email in account[1:]:
                email_to_name[email] = name
            first_email = account[1]
            for email in account[2:]:
                graph[first_email].append(email)
                graph[email].append(first_email)

        visited = set()
        def dfs(node, component):
            for neighbor in graph[node]:
                if neighbor in visited:
                    continue

                visited.add(neighbor)
                component.append(neighbor)
                dfs(neighbor, component)

        merged_accounts = []
        for email in email_to_name.keys():
            if email in visited:
                continue

            visited.add(email)
            component = [email]
            dfs(email, component)
            merged_account = [email_to_name[email]]
            merged_account.extend(sorted(component))
            merged_accounts.append(merged_account)

        return merged_accounts
```

### 実装2

この問題は要するに、アカウントが互いに素になるようにグルーピングする問題なので、Union Findが使える。

忘れていたが、Union Findは、

- 「グループの代表者を管理するデータ構造」
- union(x, y)
  - x, yどちらかの代表元に統一する
- find(x)
  - xが属するグループの代表元を親を辿って見つける

- 連結成分アルゴリズムもUnion Findも「同値関係による分割」を求めることができる。

- Union FindはDFS/BFSと異なり、辺が全て揃っている必要がない。オンラインでunion操作ができ、グラフを作らなくていいのでメモリ効率も良い。逆に、グループの情報しか持たないので、経路を求めたりすることはできない

Union by Size

Time: 同じ
Space: 同じ

Union Findは、

- 経路圧縮 + union by sizeの最適化で、n要素のとき、
  - findの償却計算量はO(α(n)) αは逆アッカーマン関数。ものすごく増加が遅い
  - 最悪はO(logn) union by sizeの場合、木の高さがlog(n)に抑えられるので

```py
class UnionFind:
    def __init__(self, elements):
        self.parent = {elem: elem for elem in elements}
        self.size = {elem: 1 for elem in elements}

    def find(self, x):
        while self.parent[x] != x:
            x = self.parent[x]

        return x

    def union(self, x, y):
        parent_x = self.find(x)
        parent_y = self.find(y)
        if self.size[parent_x] >= self.size[parent_y]:
            # parent_yをparent_xにつける
            self.parent[parent_y] = parent_x
            self.size[parent_x] += self.size[parent_y]
        else:
            self.parent[parent_x] = parent_y
            self.size[parent_y] += self.size[parent_x]

class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        all_emails = set()
        for account in accounts:
            for email in account[1:]:
                all_emails.add(email)

        uf = UnionFind(all_emails)
        email_to_name = {}
        for account in accounts:
            name = account[0]
            first_email = account[1]
            email_to_name[first_email] = name
            for email in account[2:]:
                email_to_name[email] = name
                uf.union(first_email, email)

        rep_to_emails = defaultdict(list)
        for email in all_emails:
            rep = uf.find(email)
            rep_to_emails[rep].append(email)

        result = []
        for rep, emails in rep_to_emails.items():
            account = [email_to_name[rep]]
            account.extend(sorted(emails))
            result.append(account)

        return result
```

- findに経路圧縮を入れるとより良くなる

圧縮前

```py
def find(self, x):
    if self.parent[x] == x:
        return x

    return self.find(self.parent[x])
```

圧縮後

```py
def find(self, x):
    if self.parent[x] != x:
        self.parent[x] = self.find(self.parent[x])

    return self.parent[x]
```

- 命名
  - `parent_x`, `parent_y`というより`root_x`, `root_y` (代表元)が適切
- `union`で、x,yがすでに同じ集合にあるときもスキップせず処理をしているので、サイズを余計に加算してしまうバグがある

### 実装2 改善

上記を少し改善

```py
class UnionFind[T]:
    def __init__(self, elements: Iterable[T]):
        self.parent = {elem: elem for elem in elements}
        self.size = {elem: 1 for elem in elements}

    def find(self, x: T) -> T:
        if x != self.parent[x]:
            self.parent[x] = self.find(self.parent[x])

        return self.parent[x]

    def union(self, x: T, y: T) -> None:
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            # すでに同じ集合にあるときはスキップ。サイズが加算されてしまうのを防ぐ
            return False

        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x

        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        return True

class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        email_set = set()
        for account in accounts:
            for email in account[1:]:
                email_set.add(email)

        uf = UnionFind(email_set)
        email_to_name = {}
        for account in accounts:
            name = account[0]
            first_email = account[1]
            email_to_name[first_email] = name
            for email in account[2:]:
                uf.union(first_email, email)
                email_to_name[email] = name

        email_groups = defaultdict(list)
        for email in email_set:
            root_email = uf.find(email)
            email_groups[root_email].append(email)

        merged_accounts = []
        for root_email, emails in email_groups.items():
            account = [email_to_name[root_email]]
            account.extend(sorted(emails))
            merged_accounts.append(account)

        return merged_accounts
```

### 類題

今まで解いたことのある中で似ている問題

- count-connected-components
- number-of-islands / max-area-of-island

上記の問題はDFS / UnionFindで解ける。今回のと合わせて以下のようなパターンになっている

- 連結成分を数える -> union findならクラスに連結成分の個数を保持する変数を持たせる(初期値は全要素数と一致)
- 連結成分のサイズを求める -> union by sizeのsizeで計算できる
- 連結成分そのものを求める -> parentのキーを走査して、同じrootの要素でグルーピングする

他にはグラフの閉路検出などでunion findを使える

- course-schedule
  - 有向グラフなのでトポロジカルソートを使う

## Step2

- https://github.com/huyfififi/coding-challenges/pull/48
  - Union Findで、自分とは違うやり方をしている
    - 自分: メールをUFの要素としている
    - 上記: アカウントのインデックスを要素として、共通するメールアドレスを持つアカウント同士をインデックスを介してUnionする

```py
for account_index, (_, *emails) in enumerate(accounts):
    for email in emails:
        if email in mail_to_account_index:
            union_find.union(account_index, mail_to_account_index[email])
        else:
            mail_to_account_index[email] = account_index
```

- https://github.com/tom4649/Coding/pull/108
  - union find
    - 本問題は、同じアカウント内でもアドレスの重複を無くさないといけないので、書き方によってはsetを通すことが必要になる

## Step3

dfs

```py
class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        graph = defaultdict(list)
        email_to_name = {}
        for name, *emails in accounts:
            for email in emails:
                email_to_name[email] = name
            first_email = emails[0]
            for email in emails[1:]:
                graph[email].append(first_email)
                graph[first_email].append(email)

        visited = set()
        def collect_component(node, component):
            for neighbor in graph[node]:
                if neighbor in visited:
                    continue

                visited.add(neighbor)
                component.append(neighbor)
                collect_component(neighbor, component)

        merged_accounts = []
        for email in email_to_name.keys():
            if email in visited:
                continue

            component = [email]
            visited.add(email)
            collect_component(email, component)
            merged_accounts.append([email_to_name[email], *sorted(component)])

        return merged_accounts
```

UnionFind

```py
class UnionFind:
    def __init__(self, n):
        self.parent = [i for i in range(n)]
        self.size = [1] * n

    def find(self, x):
        if self.parent[x] == x:
            return x

        self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False

        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        return True

class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        uf = UnionFind(len(accounts))
        email_to_account_index = defaultdict(int)
        for account_index in range(len(accounts)):
            _, *emails = accounts[account_index]
            for email in emails:
                if email in email_to_account_index:
                    uf.union(account_index, email_to_account_index[email])
                    continue

                email_to_account_index[email] = account_index

        account_index_to_emails = defaultdict(list)
        for account_index in range(len(accounts)):
            root_account_index = uf.find(account_index)
            _, *emails = accounts[account_index]
            account_index_to_emails[root_account_index].extend(emails)

        merged_accounts = []
        for account_index, emails in account_index_to_emails.items():
            merged_accounts.append([accounts[account_index][0], *sorted(set(emails))])

        return merged_accounts
```

- `email_to_account_index`にdefaultdictを使うのは危ない気も
