import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

class KruskalMSTApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Simulasi Kruskal's Algorithm")

        self.graph = nx.Graph()
        self.edges = []
        self.pos = None

        self.create_widgets()
        self.setup_graph()
        self.draw_initial_graph()  # langsung tampilkan graf awal

    def create_widgets(self):
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.button_run = ttk.Button(self.frame, text="Jalankan Kruskal", command=self.run_kruskal)
        self.button_run.pack(pady=10)

        # Frame untuk Text widget dan scrollbar langkah-langkah
        self.step_frame = ttk.Frame(self.frame)
        self.step_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=False)

        self.step_text = tk.Text(self.step_frame, height=10, width=80, wrap=tk.WORD)
        self.step_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.step_frame, orient=tk.VERTICAL, command=self.step_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.step_text.config(yscrollcommand=self.scrollbar.set)

        self.canvas_frame = ttk.Frame(self.frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

    def setup_graph(self):
        edges = [
            ("A", "B", 1890), ("B", "V1", 1320), ("B", "V2", 1080),
            ("B", "V3", 907), ("B", "V4", 809), ("B", "V5", 708),
            ("B", "V6", 702), ("B", "V7", 263), ("V1", "W1", 40),
            ("V1", "W2", 48), ("V1", "W3", 30), ("V2", "W2", 158),
            ("V4", "W4", 50), ("V4", "W5", 121), ("V5", "W4", 110),
            ("V5", "W5", 87), ("V6", "W6", 80), ("V6", "W7", 50),
            ("V6", "W8", 150), ("V7", "W8", 80)
        ]
        for u, v, w in edges:
            self.graph.add_edge(u, v, weight=w)
            self.edges.append((u, v, w))

        self.pos = nx.spring_layout(self.graph, seed=42)

    def draw_initial_graph(self):
        self.ax.clear()
        nx.draw(self.graph, self.pos, ax=self.ax, with_labels=True, node_color='lightblue', edge_color='gray')
        self.ax.set_title("Graf Awal")
        self.canvas.draw()

    def append_step_text(self, text):
        self.step_text.insert(tk.END, text + "\n")
        self.step_text.see(tk.END)  # scroll otomatis ke bawah

    def run_kruskal(self):
        self.step_text.delete("1.0", tk.END)  # Bersihkan dulu teks langkah
        self.ax.clear()
        nx.draw(self.graph, self.pos, ax=self.ax, with_labels=True, node_color='lightblue', edge_color='gray')
        self.canvas.draw()

        sorted_edges = sorted(self.edges, key=lambda x: x[2])
        mst = nx.Graph()
        parent = {node: node for node in self.graph.nodes()}

        def find(node):
            if parent[node] != node:
                parent[node] = find(parent[node])
            return parent[node]

        def union(u, v):
            u_root = find(u)
            v_root = find(v)
            if u_root != v_root:
                parent[v_root] = u_root
                return True
            return False

        total_weight = 0
        step_count = 1

        for u, v, weight in sorted_edges:
            self.ax.clear()
            nx.draw(self.graph, self.pos, ax=self.ax, with_labels=True,
                    node_color='lightgray', edge_color='lightgray')

            nx.draw(mst, self.pos, ax=self.ax, with_labels=True,
                    node_color='lightgreen', edge_color='red', width=2)

            nx.draw_networkx_edges(self.graph, self.pos, edgelist=[(u, v)],
                                   ax=self.ax, edge_color='blue', width=2, style='dashed')

            self.canvas.draw()

            # Tulis langkah baru ke text widget tanpa hapus yang lama
            self.append_step_text(f"Langkah {step_count}: Memeriksa edge ({u}, {v}) dengan bobot {weight}")
            if union(u, v):
                mst.add_edge(u, v, weight=weight)
                total_weight += weight
                self.append_step_text(f"  -> Edge diterima dan ditambahkan ke MST.")
            else:
                self.append_step_text(f"  -> Edge ditolak (membentuk siklus).")

            self.append_step_text(f"  Jumlah edge MST saat ini: {mst.number_of_edges()} dari {self.graph.number_of_nodes()-1}")
            self.append_step_text("-" * 60)

            self.master.update()
            step_count += 1
            time.sleep(1)  # jeda 1 detik

        initial_weight = sum(w for _, _, w in self.edges)
        saved = initial_weight - total_weight

        self.ax.set_title(f"Total kabel awal: {initial_weight} m\n"
                          f"Kabel MST: {total_weight} m\n"
                          f"Penghematan: {saved} m", fontsize=10)
        self.canvas.draw()

        self.append_step_text(f"Proses selesai!")
        self.append_step_text(f"Total kabel awal: {initial_weight} m")
        self.append_step_text(f"Total kabel MST: {total_weight} m")
        self.append_step_text(f"Penghematan: {saved} m")

if __name__ == "__main__":
    root = tk.Tk()
    app = KruskalMSTApp(root)
    root.mainloop()

