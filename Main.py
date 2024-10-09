import tkinter as tk
from tkinter import ttk
from collections import deque


class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v):
        self.graph.setdefault(u, []).append(v)
        self.graph.setdefault(v, []).append(u)

class Node:
    def __init__(self, node_id, x, y, circle_id, text_id):
        self.id = node_id
        self.x = x
        self.y = y
        self.circle_id = circle_id
        self.text_id = text_id


class Edge:
    def __init__(self, from_node_id, to_node_id, line_id):
        self.from_node_id = from_node_id
        self.to_node_id = to_node_id
        self.line_id = line_id


class GraphGUI:
    def __init__(self, master):
        self.master = master
        master.title("Graph Algorithms Visualization")

        # Modes
        self.mode = tk.StringVar()
        self.mode.set("draw_node")

        # Algorithm selection
        self.algorithm = tk.StringVar()
        self.algorithm.set("Recursive DFS")

        # Starting node selection
        self.start_node = tk.IntVar()

        # Node counter
        self.node_counter = 0

        # Data structures
        self.nodes = {}  # node_id: Node
        self.edges = []  # list of Edge
        self.graph = Graph()  # Using the Graph class provided

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create canvas
        self.canvas = tk.Canvas(self.main_frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create controls
        control_frame = tk.Frame(self.main_frame)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Modes
        modes_frame = tk.LabelFrame(control_frame, text="Mode")
        modes_frame.pack(pady=10)

        tk.Radiobutton(modes_frame, text="Draw Nodes", variable=self.mode, value="draw_node").pack(anchor=tk.W)
        tk.Radiobutton(modes_frame, text="Draw Edges", variable=self.mode, value="draw_edge").pack(anchor=tk.W)
        tk.Radiobutton(modes_frame, text="Move Nodes", variable=self.mode, value="move_node").pack(anchor=tk.W)

        # Algorithm selection
        alg_frame = tk.LabelFrame(control_frame, text="Algorithm")
        alg_frame.pack(pady=10)

        algorithms = ["Recursive DFS", "DFS", "BFS"]
        alg_menu = ttk.OptionMenu(alg_frame, self.algorithm, self.algorithm.get(), *algorithms)
        alg_menu.pack()

        # Starting node selection
        start_node_frame = tk.LabelFrame(control_frame, text="Start Node")
        start_node_frame.pack(pady=10)

        self.start_node_menu = ttk.OptionMenu(start_node_frame, self.start_node, None)
        self.start_node_menu.pack()

        # Run button
        run_button = tk.Button(control_frame, text="Run", command=self.run_algorithm)
        run_button.pack(pady=10)

        # Clear Canvas button
        clear_button = tk.Button(control_frame, text="Clear Canvas", command=self.clear_canvas)
        clear_button.pack(pady=10)

        # Bind events
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<B1-Motion>", self.canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.canvas_release)

        # For moving nodes
        self.selected_node_id = None
        self.dragging = False

        # For edge drawing
        self.edge_start_node = None

    def update_start_node_menu(self):
        menu = self.start_node_menu["menu"]
        menu.delete(0, "end")
        for node_id in self.nodes.keys():
            menu.add_command(label=str(node_id), command=lambda value=node_id: self.start_node.set(value))
        if self.nodes:
            self.start_node.set(next(iter(self.nodes)))
        else:
            self.start_node.set(None)

    def canvas_click(self, event):
        if self.mode.get() == "draw_node":
            self.add_node(event.x, event.y)
        elif self.mode.get() == "draw_edge":
            self.select_edge_node(event.x, event.y)
        elif self.mode.get() == "move_node":
            self.start_move_node(event.x, event.y)

    def add_node(self, x, y):
        node_id = self.node_counter
        self.node_counter += 1

        r = 20  # radius
        circle_id = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="lightblue")
        text_id = self.canvas.create_text(x, y, text=str(node_id))

        node = Node(node_id, x, y, circle_id, text_id)
        self.nodes[node_id] = node

        # Update start node menu
        self.update_start_node_menu()

    def select_edge_node(self, x, y):
        node_id = self.get_node_at_position(x, y)
        if node_id is not None:
            if self.edge_start_node is None:
                self.edge_start_node = node_id
                # Highlight the node
                self.canvas.itemconfig(self.nodes[node_id].circle_id, outline="red", width=2)
            else:
                from_node_id = self.edge_start_node
                to_node_id = node_id
                self.add_edge(from_node_id, to_node_id)
                # Remove highlight
                self.canvas.itemconfig(self.nodes[from_node_id].circle_id, outline="black", width=1)
                self.edge_start_node = None

    def get_node_at_position(self, x, y):
        overlapping = self.canvas.find_overlapping(x - 1, y - 1, x + 1, y + 1)
        for item in overlapping:
            for node_id, node in self.nodes.items():
                if item == node.circle_id or item == node.text_id:
                    return node_id
        return None

    def add_edge(self, from_node_id, to_node_id):
        # Avoid adding duplicate edges
        for edge in self.edges:
            if (edge.from_node_id == from_node_id and edge.to_node_id == to_node_id) or \
               (edge.from_node_id == to_node_id and edge.to_node_id == from_node_id):
                return  # Edge already exists
        from_node = self.nodes[from_node_id]
        to_node = self.nodes[to_node_id]
        line_id = self.canvas.create_line(from_node.x, from_node.y, to_node.x, to_node.y)
        edge = Edge(from_node_id, to_node_id, line_id)
        self.edges.append(edge)
        # Add edge to the graph data structure
        self.graph.add_edge(from_node_id, to_node_id)

    def start_move_node(self, x, y):
        node_id = self.get_node_at_position(x, y)
        if node_id is not None:
            self.selected_node_id = node_id
            self.dragging = True

    def canvas_drag(self, event):
        if self.mode.get() == "move_node" and self.dragging and self.selected_node_id is not None:
            node = self.nodes[self.selected_node_id]
            dx = event.x - node.x
            dy = event.y - node.y
            self.canvas.move(node.circle_id, dx, dy)
            self.canvas.move(node.text_id, dx, dy)
            node.x = event.x
            node.y = event.y
            self.update_edges(self.selected_node_id)

    def canvas_release(self, event):
        if self.mode.get() == "move_node" and self.dragging:
            self.dragging = False
            self.selected_node_id = None

    def update_edges(self, node_id):
        for edge in self.edges:
            if edge.from_node_id == node_id or edge.to_node_id == node_id:
                from_node = self.nodes[edge.from_node_id]
                to_node = self.nodes[edge.to_node_id]
                self.canvas.coords(edge.line_id, from_node.x, from_node.y, to_node.x, to_node.y)

    def run_algorithm(self):
        start_node_id = self.start_node.get()
        if start_node_id is None:
            print("Please select a starting node.")
            return

        algorithm = self.algorithm.get()

        # Reset colors
        for node in self.nodes.values():
            self.canvas.itemconfig(node.circle_id, fill="lightblue")
        for edge in self.edges:
            self.canvas.itemconfig(edge.line_id, fill="black")

        if algorithm == "Recursive DFS":
            visited = {}
            self.recursive_dfs(start_node_id, visited)
        elif algorithm == "DFS":
            self.dfs(start_node_id)
        elif algorithm == "BFS":
            self.bfs(start_node_id)

    def recursive_dfs(self, node_id, visited):
        visited[node_id] = True
        # Highlight the node
        self.canvas.itemconfig(self.nodes[node_id].circle_id, fill="yellow")
        self.master.update()
        self.master.after(500)  # Pause for visualization

        for neighbor in self.graph.graph.get(node_id, []):
            if neighbor not in visited:
                # Optionally highlight the edge
                self.highlight_edge(node_id, neighbor)
                self.recursive_dfs(neighbor, visited)

    def dfs(self, start_node_id):
        stack = [start_node_id]
        visited = {}

        while stack:
            node_id = stack.pop()
            if node_id not in visited:
                visited[node_id] = True
                # Highlight the node
                self.canvas.itemconfig(self.nodes[node_id].circle_id, fill="yellow")
                self.master.update()
                self.master.after(500)  # Pause for visualization

                for neighbor in reversed(self.graph.graph.get(node_id, [])):
                    stack.append(neighbor)

    def bfs(self, start_node_id):
        visited = {start_node_id: True}
        queue = deque([start_node_id])

        while queue:
            node_id = queue.popleft()
            # Highlight the node
            self.canvas.itemconfig(self.nodes[node_id].circle_id, fill="yellow")
            self.master.update()
            self.master.after(500)  # Pause for visualization

            for neighbor in self.graph.graph.get(node_id, []):
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited[neighbor] = True

    def highlight_edge(self, from_node_id, to_node_id):
        for edge in self.edges:
            if (edge.from_node_id == from_node_id and edge.to_node_id == to_node_id) or \
               (edge.from_node_id == to_node_id and edge.to_node_id == from_node_id):
                self.canvas.itemconfig(edge.line_id, fill="red")
                self.master.update()
                self.master.after(250)
                return

    def clear_canvas(self):
        # Clear the canvas
        self.canvas.delete("all")
        # Reset data structures
        self.nodes.clear()
        self.edges.clear()
        self.graph = Graph()
        self.node_counter = 0
        self.edge_start_node = None
        # Update start node menu
        self.update_start_node_menu()


if __name__ == '__main__':
    root = tk.Tk()
    app = GraphGUI(root)
    root.mainloop()
