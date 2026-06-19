Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.

Symbol       Value
I             1
V             5
X             10
L             50
C             100
D             500
M             1000
For example, 2 is written as II in Roman numeral, just two ones added together. 12 is written as XII, which is simply X + II. The number 27 is written as XXVII, which is XX + V + II.

Roman numerals are usually written largest to smallest from left to right. However, the numeral for four is not IIII. Instead, the number four is written as IV. Because the one is before the five we subtract it making four. The same principle applies to the number nine, which is written as IX. There are six instances where subtraction is used:

I can be placed before V (5) and X (10) to make 4 and 9. 
X can be placed before L (50) and C (100) to make 40 and 90. 
C can be placed before D (500) and M (1000) to make 400 and 900.
Given a roman numeral, convert it to an integer.

Example 1:
Input: s = "III"
Output: 3
Explanation: III = 3.

Example 2:
Input: s = "LVIII"
Output: 58
Explanation: L = 50, V= 5, III = 3.

Example 3:
Input: s = "MCMXCIV"
Output: 1994
Explanation: M = 1000, CM = 900, XC = 90 and IV = 4.
 
Constraints:
- 1 <= s.length <= 15
- s contains only the characters ('I', 'V', 'X', 'L', 'C', 'D', 'M').
- It is guaranteed that s is a valid roman numeral in the range [1, 3999].

Approach

Time: O(N)
Space: O(1)
```py
class Solution:
    def romanToInt(self, s: str) -> int:
        n = len(s)
        roman_to_integer = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        }
        result = 0
        i = 0
        while i < n:
            c = s[i]
            if c == 'I':
                if i < n - 1 and (s[i + 1] == 'V' or s[i + 1] == 'X'):
                    result += roman_to_integer[s[i + 1]] - roman_to_integer[s[i]]
                    i += 2
                    continue

            if c == 'X':
                if i < n - 1 and (s[i + 1] == 'L' or s[i + 1] == 'C'):
                    result += roman_to_integer[s[i + 1]] - roman_to_integer[s[i]]
                    i += 2
                    continue

            if c == 'C':
                if i < n - 1 and (s[i + 1] == 'D' or s[i + 1] == 'M'):
                    result += roman_to_integer[s[i + 1]] - roman_to_integer[s[i]]
                    i += 2
                    continue
            
            result += roman_to_integer[s[i]]
            i += 1
        
        return result
```

test cases
- LVIII
i   result
0   50
1   55
2   56
3   57
4   58

- MCMXCIV
i   result
0   1000
1   1900
3   1990
5   1994
7   return 1994

edge cases
- I

Follow Up
Got it, continuing the follow-up in English.

1. What's the time and space complexity of your solution?
- Time: O(N)
- Space: O(1)

2. What would happen if the input were an invalid Roman numeral, say `"IIII"` or `"IC"`? The problem guarantees valid input, but if you were to add validation, where and how would you add it?

- 同じローマ数字が4つ以上繰り返すのは禁止
- １つ前のチャンクは現在のチャンクより小さくなければならない
- 減算ペアの前にはそのペアの大きい方の文字以上のものがあってはいけない

```py


```

別の方法
- 完全な正規性チェックは正規表現か変換結果を逆変換して元と一致するか確認する
```py
def romanToInt(self, s):
    result = ....
    if int_to_roman(result) != s:
        raise ValueError("non-canonical")
    
    return result
```

3. Suppose we flip the problem: given an integer in [1, 3999], return the Roman numeral string. How would you approach it? Just the approach, no code needed.


リファクタリング