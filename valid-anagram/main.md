# Valid Anagram
Given two strings s and t, return true if t is an anagram of s, and false otherwise.
 
Example 1:
Input: s = "anagram", t = "nagaram"
Output: true

Example 2:
Input: s = "rat", t = "car"
Output: false

Constraints:
- 1 <= s.length, t.length <= 5 * 10^4
- s and t consist of lowercase English letters.
 
Follow up: What if the inputs contain Unicode characters? How would you adapt your solution to such a case?

## Step1
anagramかどうかを調べる問題
- 長さが1以上10^4オーダー以下
- lower caseのアルファベットのみ
sを走査して、アルファベットをカウントする。そしてtを先頭から走査して同じくカウントして、カウントした結果自体が一致していればAnagramとみなせる

凡ミスに気が付かず、10分かかった

Time: O(N)
Space: O(26)
```py
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        letter_to_count = {}
        for c in s:
            if c not in letter_to_count:
                # memo: ここを0にしてた
                letter_to_count[c] = 1
                continue

            letter_to_count[c] += 1

        for c in t:
            if c not in letter_to_count:
                return False

            letter_to_count[c] -= 1
        
        for val in letter_to_count.values():
            if val != 0:
                return False
        
        return True
```

面接ではいきなり書くことはないと思うが、以下のように書ける
```py
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return Counter(s) == Counter(t)
```

```py
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return sorted(s) == sorted(t)
```

Follow up: What if the inputs contain Unicode characters? How would you adapt your solution to such a case?

空間計算量が増える？ただ最大はそれでも10^4. 上記フォローアップの意味がよくわからなかったのでAIに聞いてみる

> このフォローアップの想定は C++/Java など「文字列がバイト列 / UTF-16 コード単位」である言語。
> Python の `str` は最初から**コードポイント列**なので、`Counter(s) == Counter(t)` はコード変更不要で動く。空間も O(26) → O(ユニーク文字数) になるだけで本質的な問題はない (強いて言えば NFC 正規化を入れないと `"é"` (U+00E9) と `"e" + U+0301` が別物扱いになる、というくらい)。
>
> 一方、C++ の典型解は固定長配列 + ASCII 前提で書く:
> ```cpp
> int count[26] = {0};
> for (char c : s) count[c - 'a']++;
> ```
> - `std::string` はバイト列なので、UTF-8 で 1 文字が 1〜4 バイトに分かれる。`s[i]` が「1文字」を指さなくなる
> - `c - 'a'` のインデックスが負や 200 超になって即 UB
> - 配列を 256 に広げても、`"é"` (UTF-8: `0xC3 0xA9`) はバイトごとに別カウントされてしまい、アナグラム判定として正しくない
>
> よって UTF-8 をコードポイントへデコードし (`char32_t` / ICU)、`std::unordered_map<char32_t, int>` に置き換えるという実装方針の変更が必要になる。Java も `charAt` が UTF-16 コード単位なのでサロゲートペア (絵文字等) で割れる → `codePointAt` + `HashMap` 化が必要。
>
> まとめ:
> - Python で解いた場合: ロジック変更不要。正規化 (NFC) の扱いだけ仕様確認
> - C++/Java で解いた場合: 固定長配列 + ASCII 前提が崩れるので hash map + コードポイント単位に切り替える


### 余談
Pythonでは`str`はコードポイントの列である（https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str）
ので、以下のように他の言語とは挙動が異なる

| 文字列 | C++ `s.size()` (UTF-8 バイト) | Java `s.length()` (UTF-16単位) | Python `len(s)` (コードポイント) |
|---|---|---|---|
| `"abc"` | 3 | 3 | 3 |
| `"café"` | 5 | 4 | 4 |
| `"😀"` | 4 | 2 | 1 |

C++ では `s[3]` が `'é'` の片割れバイト、Java では `s.charAt(0)` がサロゲートの片割れになるが、Python は `s[0]` で `'😀'` がそのまま 1 文字として取れる。よって `Counter(s)` がそのままコードポイント単位カウントになる。

AIによると、以下のような内部実装になっているらしい (PEP 393: https://peps.python.org/pep-0393/)

>CPython の `str` は **「文字列内の最大コードポイントに応じて 1/2/4 バイトの固定幅配列」** で持つ。

| 最大コードポイント | 内部表現 | 1文字あたり |
|---|---|---|
| ≤ U+00FF | Latin-1 | 1 バイト |
| ≤ U+FFFF | UCS-2 | 2 バイト |
| ≤ U+10FFFF | UCS-4 | 4 バイト |

固定幅なので `s[i]` が O(1) かつ 1 コードポイント保証。代償としてメモリは UTF-8 より食う (絵文字 1 個で全体が 4 バイト/文字化) ので、I/O 時は `encode("utf-8")` / `decode("utf-8")` で変換する設計。

これは CPython の実装詳細であり、PyPy は UTF-8 + インデックステーブル、Jython は JVM の UTF-16 を流用、と実装ごとに方法は違う。言語仕様レベルで保証されているのは「`str` はコードポイント列」という点のみ。

## Step2

他の人のPRから学びになるポイントをまとめる。

### 早期return: tの走査中にカウントが負になった時点でFalse

[huyfififi#7](https://github.com/huyfififi/coding-challenges/pull/7#discussion_r2042939710)

> kzhra-sanなどのように引き算で解くとSpaceはnまたはmのどちらかだけで済みますね。このとき、片方で作った辞書or配列から減算していって、途中で負になったらその時点でFalse、最後まで負になることがなければTrueという最後までやらない方法もあります。

sのカウントを1つ作り、tを走査しながらデクリメント。負になったら即Falseする
- 空間が O(unique(s)) のみ、かつ平均的に早く抜けられる
- 自分の解答も2回ループしてからvalues走査しているので、これを1ループで処理する版に書き換える練習をすると良さそう。最初に長さチェック`len(s) != len(t): return False`を入れることで、valuesループを消すことができる。

### `defaultdict` の `==` は内部的に `dict` と同じ

[azriel1rf#2](https://github.com/azriel1rf/leetcode-prep/pull/2#discussion_r1972858697)

> defaultdictはdictを継承しており、個別にeqを実装してないためdictと同じだと考えていい。
> https://github.com/python/cpython/blob/3.13/Modules/_collectionsmodule.c#L2802

- `cnt1 == cnt2` で OK。`==` の内部で早期 return も効く

### C++ 特有: 文字コードがアルファベット順とは限らない (EBCDIC)

[eito2002#2](https://github.com/eito2002/LeetCode/pull/2#discussion_r2231079831)

> EBCDIC ではアルファベットの文字コードがアルファベット順になっておらず、このコードが正しく動かないようです。ただし、ASCII 等、近年使用されているほとんどの文字コードでは ... 意図通り動きます。ここまで意識できているとよいと思います。

- `s[i] - 'a'` は ASCII 互換であることに暗黙に依存している. C/CppではEBCDICかASCIIかは環境依存
    - PythonはUnicodeコードポイントの列
    - GoやRustなどはUTF-8でエンコーディングされたバイト列らしい

- 加えて `char` が signed/unsigned かは実装定義で、Unicode などが混じると UB

### Unicode 正規化 (NFC/NFKC)

[huyfififi#7](https://github.com/huyfififi/coding-challenges/pull/7)

```
"café" == "café"  # False
```

- 見た目同じでもコードポイント列が違う → `unicodedata.normalize("NFKC", s)` で揃える
- Pythonでも「気にすべきこと」が残るのはこれ。

### Python の `count()` は O(n)

[huyfififi#7](https://github.com/huyfififi/coding-challenges/pull/7)

> `for c in set(s): if s.count(c) != t.count(c)` の方法は時間計算量 O(n^2)

- https://github.com/python/cpython/blob/main/Objects/stringlib/fastsearch.h
Cpython
    - 以上がcountメソッドの実装らしい
    
---

## Step3

```py
class Solution:                                                     
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
            
        char_to_count = {}
        for c in s:
            char_to_count[c] = char_to_count.get(c, 0) + 1
        
        for c in t:
            if c not in char_to_count:
                return False
            
            char_to_count[c] -= 1
            if char_to_count[c] < 0:
                return False
        
        return True
```

### 過去に解いた類題

- group-anagrams
- first-unique-character-in-a-string
- top-k-frequent-elements
- intersection-of-two-arrays