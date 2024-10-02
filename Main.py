from graph.Graph import Graph

if __name__ == '__main__':
    graph = Graph()

    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(1, 4)
    graph.add_edge(2, 3)
    graph.add_edge(2, 5)
    graph.add_edge(3, 4)

    graph.recursive_dfs(0)
    print()
    graph.dfs(0)
    print()
    graph.bfs(0)