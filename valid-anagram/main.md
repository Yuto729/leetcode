# Valid Anagram

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
                # ここを0にしてた
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

空間計算量が増える？ただ最大はそれでも10^4