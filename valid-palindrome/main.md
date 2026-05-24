A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.

Given a string s, return true if it is a palindrome, or false otherwise.
 
Example 1:
Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.

Example 2:
Input: s = "race a car"
Output: false
Explanation: "raceacar" is not a palindrome.

Example 3:
Input: s = " "
Output: true
Explanation: s is an empty string "" after removing non-alphanumeric characters.
Since an empty string reads the same forward and backward, it is a palindrome.

Constraints:
- 1 <= s.length <= 2 * 10^5
- s consists only of printable ASCII characters.

## Step1
- convert uppercase to lowercase
- remove non-alphanumeric characters (letters and numbers以外)
- same forward and backward

19msくらい. もうちょい早くできそう. 一個のループでかける
```py
class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = s.strip()
        if not s:
            return True
        
        # remove and converting
        def convert_and_remove(s):
            preprocessed_s = []
            for c in s:
                if 'A' <= c <= 'Z':
                    i = string.ascii_uppercase.find(c)
                    preprocessed_s.append(string.ascii_lowercase[i])
                    continue
                
                if not ('0' <= c <= '9' or 'a' <= c <= 'z'):
                    continue
                
                preprocessed_s.append(c)
            
            return "".join(preprocessed_s)
        
        def check_if_parindrome(s):
            left = 0
            right = len(s) - 1
            while left < right:
                if s[left] != s[right]:
                    return False

                right -= 1
                left += 1

            return True

        
        preprocessed_s = convert_and_remove(s)
        return check_if_parindrome(preprocessed_s)
```

あまり実行時間が変わらない
- convert_to_valid_charの中身に書き方のバリエーションがあるように思える

```py
class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = s.strip()
        if not s:
            return True
        
        def convert_to_valid_char(c):
            if 'A' <= c <= 'Z':
                i = string.ascii_uppercase.find(c)
                return string.ascii_lowercase[i]
         
            if not ('0' <= c <= '9' or 'a' <= c <= 'z'):
                return ""
            
            return c
            
        left = 0
        right = len(s) - 1
        while left < right:
            left_char = convert_to_valid_char(s[left])
            right_char = convert_to_valid_char(s[right])
            if left_char == "":
                left += 1
                continue

            if right_char == "":
                right -= 1
                continue
            
            if left_char != right_char:
                return False
            
            left += 1
            right -= 1
        
        return True
```

`ord`で直接変換してみた
```py
def convert_to_valid_char(c):
    if 'A' <= c <= 'Z':
        return chr(ord('a') + (ord(c) - ord('A')))
    
    if not ('0' <= c <= '9' or 'a' <= c <= 'z'):
        return ""
    
    return c
```

なかなか速くならないのでAIに聞いてみる
> Pythonでは組み込み関数（C実装）を使うのが一番速いです。
確かに忘れていた
```py
class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = s.strip()
        if not s:
            return True
        
        def convert_to_valid(s):
            filtered = []
            # 組み込み関数
            for c in s.lower():
                # 組み込み関数
                if not c.isalnum():
                    continue
                
                filtered.append(c)
            return filtered

        def check_if_parindrome(s):
            left = 0
            right = len(s) - 1
            while left < right:
                if s[left] != s[right]:
                    return False

                right -= 1
                left += 1

            return True 
        left = 0
        right = len(s) - 1
        filtered = convert_to_valid(s)
        return check_if_parindrome(filtered)
```


メモ: Pythonの文字形式判定メソッド

- `c.isascii()`
  - ASCII範囲（U+0000 〜 U+007F、計128文字）かどうか
  - 制御文字・スペース・記号・英数字すべて含む
  - 例: `'A'`, `'5'`, `' '`, `'\n'` → True / `'あ'`, `'²'` → False
- `c.isalpha()`
  - Unicode上の文字（letter）
  - 例: `'A'`, `'あ'`, `'漢'`, `'四'`, `'é'` → True / `'5'`, `'²'` → False
  - 漢数字「四」も letter 扱いで True
- `c.isdecimal()`
  - 10進位取り記数法に使える数字
  - 一番厳しい
  - 例: `'5'`, `'０'`（全角）, `'٥'`（アラビア） → True / `'²'`, `'½'`, `'Ⅳ'`, `'四'`, `'①'` → False
  - `int(c)` が成功する文字とほぼ一致
- `c.isdigit()`
  - 数字記号（位取り不可も含む）
  - `isdecimal()` ⊂ `isdigit()`
  - 例: `'5'`, `'²'`, `'①'` → True / `'½'`, `'Ⅳ'`, `'四'` → False
- `c.isnumeric()`
  - 数値を表す文字すべて（分数・ローマ数字・漢数字も含む）
  - `isdigit()` ⊂ `isnumeric()`
  - 一番緩い
  - 例: `'5'`, `'²'`, `'½'`, `'Ⅳ'`, `'四'`, `'①'` → True
- `c.isalnum()`
  - `isalpha() or isdecimal() or isdigit() or isnumeric()` のいずれか
  - 一番緩い英数字判定
  - 「四」「²」「½」も True になる
- 包含関係
  - 数字: `isdecimal()` ⊂ `isdigit()` ⊂ `isnumeric()`
  - 英数字: `isalnum()` = `isalpha() ∪ isnumeric()`

## Step2

### `str.isalnum()` のUnicode挙動に注意

[huyfififi#5](https://github.com/huyfififi/coding-challenges/pull/5)

> `str.isalnum()`は`str.isalpha()`, `str.isdecimal()`, `str.isdigit()`, `str.isnumeric()`から成り立っている。`"四".isalnum()` も `"²".isalnum()` も `True` を返し、これは [a-zA-Z0-9] という直感に反する。面接時に面接官とすり合わせを行った方がいい。

- https://docs.python.org/3/library/stdtypes.html#str.isalnum

問題文の "alphanumeric" を厳密に [a-zA-Z0-9] に絞りたい場合は `isalnum()` ではなく正規表現 `re.match(r"[a-zA-Z0-9]", c)` や `c.isascii() and c.isalnum()` が良さそう。

### 3つの実装方式の実行時間比較（回文 vs 非回文）

[naoto-iwase#63](https://github.com/naoto-iwase/leetcode/pull/63)

> 回文の場合は[::-1]が、C実装とかの恩恵で速く、非回文の場合は逆に[::-1]だけはearly returnが効かないので遅い、という解釈です。

3手法（two_pointer / `all(... for i in range(half))` / `s == s[::-1]`）を入力サイズ100〜100,000で比較した結果:
- 回文: `[::-1]`が圧倒的に速い（C実装でメモリ連続コピー＋一括比較）
- 非回文: two_pointerが圧倒的に速い（early returnが効く、`[::-1]`は最後まで作って比較）

[::-1]は空間計算量がO(n)になる

### Computer Science: 文字列の編集に強いデータ構造（Rope, Piece Table）

[ryosuketc#5](https://github.com/ryosuketc/leetcode_grind75/pull/5)

> Rope というデータ構造を思い出します。これは、木構造で文字列を管理して編集されていない部分木を共有します。split, concatenate が O(log n) でできます。Piece Table はテキストエディターなどで使われるもので、変更履歴を追いかけていくものです。

- Rope: 木構造で文字列管理、split/concatが O(log n)。長文の編集に強い。
- Piece Table: VS Code等のテキストエディタで使われる。元バッファ+追加バッファへのポインタ列で編集履歴を表現。

---

## Step3
正規表現で厳密に取り出す
```py
class Solution:
    def isPalindrome(self, s: str) -> bool:
        filtered = re.findall(r"[a-z0-9]", s.lower())
        left = 0
        right = len(filtered) - 1
        while left < right:
            if filtered[left] != filtered[right]:
                return False
            
            left += 1
            right -= 1
        
        return True
```

O(1)スペース版
```py
class Solution:
    def isPalindrome(self, s: str) -> bool:
        left, right = 0, len(s) - 1
        while left < right:
            while left < right and not (s[left].isascii() and s[left].isalnum()):
                left += 1
            while left < right and not (s[right].isascii() and s[right].isalnum()):
                right -= 1
        
            if s[left].lower() != s[right].lower():
                return False
            
            left += 1
            right -= 1

        return True
```
edgeケース
".," // left = 1, right = 1で終端。Trueを返すので正解

## 過去解いた類題

- [move-zeroes]
- [two-sum]
- [longest_substring_without_repeating_characters]