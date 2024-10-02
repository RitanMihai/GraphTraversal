from collections import deque


class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append(v)

    def recursive_dfs(self, start, visited={}):
        visited[start] = True

        print(start, end=" ")
        for neighbor in self.graph.get(start, []):
            if neighbor not in visited:
                self.recursive_dfs(neighbor, visited)

    def dfs(self, start):
        stack = [start]
        visited = {}

        while len(stack) > 0:
            node = stack.pop()
            if node not in visited:
                print(node, end=" ")

                visited[node] = True

                for neighbor in reversed(self.graph.get(node, [])):
                    stack.append(neighbor)

    def bfs(self, start):
        visited = {start: True}
        queue = deque([start])

        while queue:
            node = queue.popleft()
            print(node, end=" ")

            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited[neighbor] = True
