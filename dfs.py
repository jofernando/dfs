import networkx as nx

class Graph(nx.Graph):
    def dfs_path(self, start, target, path = [], visited = set()):
        path.append(start)
        visited.add(start)
        if start == target:
            return path
        for neighbour in self.adj[start]:
            if neighbour not in visited:
                result = self.dfs_path(neighbour, target, path, visited)
                if result is not None:
                    path = []
                    visited = set()
                    return result
        path.pop()
        return None