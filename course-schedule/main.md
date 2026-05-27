There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.
Return true if you can finish all courses. Otherwise, return false.
 
Example 1:
Input: numCourses = 2, prerequisites = [[1,0]]
Output: true
Explanation: There are a total of 2 courses to take. 
To take course 1 you should have finished course 0. So it is possible.

Example 2:
Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: false
Explanation: There are a total of 2 courses to take. 
To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible.
 
Constraints:
- 1 <= numCourses <= 2000
- 0 <= prerequisites.length <= 5000
- prerequisites[i].length == 2
- 0 <= ai, bi < numCourses
- All the pairs prerequisites[i] are unique.


## Answer
循環がなければTopological Sortで一本の順序に並べることができるが循環があるとそれができないので本問題は有向非巡回グラフにサイクルがあるかどうかを調べる問題となる

Kahn's Algorithm（BFS版トポロジカルソートの改変）
Time: O(V + E)
```py
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        graph = [[] for _ in range(numCourses)]
        # 入次数を管理する
        in_degree = [0] * numCourses
        for course, pre in prerequisites:
            graph[pre].append(course)
            in_degree[course] += 1
        
        # 入次数が0のノード
        queue = deque(i for i in range(numCourses) if in_degree[i] == 0)
        num_visited_node = 0
        while queue:
            node = queue.popleft()
            num_visited_node += 1
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                # node以外他に依存元がない場合はキューに加える
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return num_visited_node == numCourses
```

参考：BFS版トポロジカルソートは以下
```py
def topological_sort(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    graph = [[] for _ in range(numCourses)]
    # 入次数を管理する
    in_degree = [0] * numCourses
    for course, pre in prerequisites:
        graph[pre].append(course)
        in_degree[course] += 1
    
    # 入次数が0のノード
    queue = deque(i for i in range(numCourses) if in_degree[i] == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            # node以外他に依存元がない場合はキューに加える
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(order) != numCourses:
        return [] # 閉路あり
    
    return order
```

- DFSを用いて解く場合
「訪問済み」に加えて「訪問中」の状態を追加する。そして、あるノードの訪問中に再びそのノードが現れる時サイクルがあるとみなす。訪問済みのノードを再び訪問するのはサイクルではない

状態をsetで置く解法
Time: O(V + E)
Space: O(V) 最悪計算量
```py
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        graph = [[] for _ in range(numCourses)]
        for course, pre in prerequisites:
            graph[pre].append(course)

        visited = set()
        visiting = set()
        def has_cycle(node):
            """
                nodeを開始点とする部分グラフに閉路があるかどうかを判定する関数
            """
            if node in visiting:
                return True
            
            if node in visited:
                return False

            visiting.add(node)
            for neighbor in graph[node]:
                if has_cycle(neighbor):
                    return True
            
            visited.add(node)
            visiting.remove(node)
            return False
        
        for node in range(numCourses):
            if has_cycle(node):
                # このnodeから到達できる範囲に閉路がある
                return False
        
        return True
```

状態配列を１つだけ用いて数字で状態を分ける解法
```py
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        graph = [[] for _ in range(numCourses)]
        for course, pre in prerequisites:
            graph[pre].append(course)
        
        # 0: 未訪問, 1: 探索中, 2: 探索済み
        state = [0] * numCourses
        def has_cycle(node):
            if state[node] == 1: 
                # 再訪問
                return True
            
            if state[node] == 2:
                # 探索済み
                return False
            
            state[node] = 1
            for neighbor in graph[node]:
                if has_cycle(neighbor):
                    return True

            # 探索済みにマーク
            state[node] = 2
            return False

        return not any(has_cycle(i) for i in range(numCourses) if state[i] == 0)
```

- `any(iterable)` -> 1つでもTrueがあればTrue
- `all(iterable)` -> 全てTrueの時True
`any(has_cycle(i) for i in range(numCourses) if state[i] == 0)` -> anyの中身はgenerator型になる

- dfs版トポロジカルソート
    - nodeを`visited`に追加するタイミングは、`dfs`の最初で処理と`dfs`を呼び出す前の２パターンある

```py
def topological_sort(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    graph = [[] for _ in range(numCourses)]
    for course, pre in prerequisites:
        graph[pre].append(course)
    
    reversed_order = []
    visited = set()
    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor in visited:
                continue
            
            dfs(neighbor)
        
        reversed_order.append(node)

    for node in range(numCourses):
        if node in visited:
            continue
        
        dfs(node)
    
    return reversed_order[::-1]
```