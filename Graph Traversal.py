import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
from matplotlib.animation import FuncAnimation

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append(v)

    def bfs(self, start):
        visited = set()
        queue = deque([start])
        traversal_order = []
        traversal_path = []
        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                visited.add(vertex)
                for neighbor in self.graph.get(vertex, []):
                    if neighbor not in visited:
                        traversal_path.append((vertex, neighbor))
                        queue.append(neighbor)
                traversal_order.append(vertex)
        return traversal_order, traversal_path

    def dfs(self, start, visited=None, traversal_order=None, traversal_path=None):
        if visited is None:
            visited = set()
        if traversal_order is None:
            traversal_order = []
        if traversal_path is None:
            traversal_path = []
        visited.add(start)
        traversal_order.append(start)
        for neighbor in self.graph.get(start, []):
            if neighbor not in visited:
                traversal_path.append((start, neighbor))
                self.dfs(neighbor, visited, traversal_order, traversal_path)
        return traversal_order, traversal_path


# Visualization Function
def visualize_graph(graph, traversal_order, traversal_path, title, interval=2000):  # Default interval is 2 seconds
    # Create a NetworkX graph
    G = nx.DiGraph()
    for u in graph.graph:
        for v in graph.graph[u]:
            G.add_edge(u, v)

    # Use a spring layout for better positioning of nodes
    pos = nx.spring_layout(G, seed=42)  # Seed ensures consistent layout

    fig, ax = plt.subplots(figsize=(8, 6))

    # Draw edges (initially gray)
    edge_artists = nx.draw_networkx_edges(G, pos, ax=ax, edge_color="gray")

    # Draw nodes
    nodes = nx.draw_networkx_nodes(G, pos, ax=ax, node_color="blue", node_size=500)
    labels = nx.draw_networkx_labels(G, pos, ax=ax, font_color="white")

    # Animate traversal
    def update(frame):
        current_node = traversal_order[frame]
        visited_nodes = traversal_order[:frame + 1]
        visited_edges = traversal_path[:frame]

        # Highlight the current node
        nodes.set_facecolor(["red" if node == current_node else "blue" for node in G.nodes])

        # Highlight the traversal path (edges)
        for i, edge in enumerate(G.edges):
            if edge in visited_edges or (edge[1], edge[0]) in visited_edges:  # Handle undirected edges
                edge_artists[i].set_color("green")
            else:
                edge_artists[i].set_color("gray")

        # Update the title to show traversal order
        ax.set_title(f"{title} Traversal: {visited_nodes}", fontsize=14)

    ani = FuncAnimation(fig, update, frames=len(traversal_order), interval=interval, repeat=False)
    plt.show()


# Example Usage
if __name__ == "__main__":
    g = Graph()
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(2, 3)
    g.add_edge(3, 3)

    print("BFS Traversal:")
    bfs_order, bfs_path = g.bfs(2)
    print("Order:", bfs_order)
    print("Path:", bfs_path)

    print("\nDFS Traversal:")
    dfs_order, dfs_path = g.dfs(2)
    print("Order:", dfs_order)
    print("Path:", dfs_path)

    # Visualize BFS with path
    visualize_graph(g, bfs_order, bfs_path, "BFS", interval=2000)

    # Visualize DFS with path
    visualize_graph(g, dfs_order, dfs_path, "DFS", interval=2000)