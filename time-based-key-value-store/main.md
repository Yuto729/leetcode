# time-based-key-value-store

Design a time-based key-value data structure that can store multiple values for the same key at different time stamps and retrieve the key's value at a certain timestamp.

Implement the TimeMap class:

TimeMap() Initializes the object of the data structure.
void set(String key, String value, int timestamp) Stores the key key with the value value at the given time timestamp.
String get(String key, int timestamp) Returns a value such that set was called previously, with timestamp_prev <= timestamp. If there are multiple such values, it returns the value associated with the largest timestamp_prev. If there are no values, it returns "".

ex.
TimeMap timeMap = new TimeMap();
timeMap.set("foo", "bar", 1); // store the key "foo" and value "bar" along with timestamp = 1.
timeMap.get("foo", 1); // return "bar"
timeMap.get("foo", 3); // return "bar", since there is no value corresponding to foo at timestamp 3 and timestamp 2, then the only value is at timestamp 1 is "bar".
timeMap.set("foo", "bar2", 4); // store the key "foo" and value "bar2" along with timestamp = 4.
timeMap.get("foo", 4); // return "bar2"
timeMap.get("foo", 5); // return "bar2"

## Step1

普通のハッシュマップにtimestampという概念を追加する。`get`ではkeyに対して、指定したtimestamp以下のtimestampを持つvalueを返す
30分くらいかかってしまった

時間計算量: set -> O(N), get -> 最悪計算量はO(MlogN), N;setの回数, M;getの回数

```py
class TimeMap:

    def __init__(self):
        self.store = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.store:
            self.store[key] = [[timestamp, value]]
            return

        self.store[key].append([timestamp, value])

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""

        values = self.store[key]
        left = 0
        right = len(values)
        while left < right:
            mid = (left + right) // 2
            if values[mid][0] < timestamp:
                left = mid + 1
            else:
                right = mid

        if left < len(values) and values[left][0] == timestamp:
            return values[left][1]

        if left > 0 and values[left - 1][0] < timestamp:
            return values[left - 1][1]

        return ""
```

- bisect_rightの方が簡単。bisect_rightは使わないが、実装はそれ相当

```py
class TimeMap:

    def __init__(self):
        self.store = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.store:
            self.store[key] = [[timestamp, value]]
            return

        self.store[key].append([timestamp, value])

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""

        values = self.store[key]
        left = 0
        right = len(values)
        while left < right:
            mid = (left + right) // 2
            if values[mid][0] <= timestamp:
                left = mid + 1
            else:
                right = mid

        if left > 0:
            return values[left - 1][1]

        return ""
```

AIレビュー

- 二分探索のロジックがgetに直接埋め込まれているが、別関数に切り出した方がいい
- `values[mid][0]`, `values[mid][1]` のようにインデックスでアクセスしているのは可読性の観点でどうか
- `values`という命名の妥当性

インデックスアクセスの代わりにNamedTupleを用いる。dataclassが通常のオブジェクトなのに対してタプルとして振る舞うことができる。タプルと同じくイミュータブル
書き直し

```py
class Entry(NamedTuple):
    timestamp: int
    value: str

class TimeMap:

    def __init__(self):
        self.store: dict[str, list[Entry]] = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append(Entry(timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""

        entries = self.store[key]
        idx = self._bisect_right(entries, timestamp)
        if idx > 0:
            return entries[idx - 1].value

        return ""

    def _bisect_right(self, entries, timestamp):
        left, right = 0, len(entries)
        while left < right:
            mid = (left + right) // 2
            if entries[mid].timestamp <= timestamp:
                left = mid + 1
            else:
                right = mid

        return left
```

entryを探すところまで関数化して、`_find_entry_at_or_before(self, entries, timestamp)`というメソッドにしてもよさそう

## Step3

```py
class Entry(NamedTuple):
    timestamp: int
    value: str

class TimeMap:

    def __init__(self):
        self.store = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append(Entry(timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""

        entries = self.store[key]
        # timestamp以下で最大のtimestampを持つentryを探す
        idx = bisect.bisect_right(entries, timestamp, key=lambda e: e.timestamp) - 1
        if idx < 0:
            return ""

        return entries[idx].value
```
