#!/usr/bin/env python3
"""graphs.html（Python 版）完整自學充實。冪等。輸出以 pythonds3 實跑取得。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from enrich_lib_py import card, ensure_style, insert_end_of_section, run_py

PAGE = Path.home() / "ds-python-selfstudy/graphs.html"
s = PAGE.read_text()
s = ensure_style(s)
PDS = "import sys; sys.path.insert(0, '/home/phonchi/ds_cpp/_python_backup/Slides/pythonds3')\n"

C_REP = """from pythonds3.graphs import Graph

g = Graph()
g.add_edge(0, 1, 5); g.add_edge(0, 5, 2); g.add_edge(1, 2, 4)
g.add_edge(2, 3, 9); g.add_edge(3, 4, 7); g.add_edge(3, 5, 3)
g.add_edge(4, 0, 1); g.add_edge(5, 4, 8); g.add_edge(5, 2, 1)

for v in g:
    for w in v.get_neighbors():
        print(f"({v.get_key()}, {w.get_key()}, {v.get_neighbor(w)})", end=" ")
print()"""

rep = f'''<h3 id="dx-rep">講義完整範例：Graph 類別的使用畫面</h3>
{card("講義 08 · 建頂點、加邊、走訪相鄰串列", C_REP, run_py(PDS + C_REP),
note="每組 (from, to, weight) 對應一條有向邊。add_edge 會自動把不存在的頂點補進圖裡，這就是相鄰串列版（dict of dict）的「用多少存多少」。")}'''
s, c1 = insert_end_of_section(s, "representation", rep, 'id="dx-rep"')

C_BFS = """from pythonds3.basic import Queue
from pythonds3.graphs import Graph

def build_graph(words):
    buckets = {}
    the_graph = Graph()
    for word in words:
        for i, _ in enumerate(word):
            bucket = f"{word[:i]}_{word[i + 1:]}"
            buckets.setdefault(bucket, set()).add(word)
    for similar_words in buckets.values():
        for word1 in similar_words:
            for word2 in similar_words - {word1}:
                the_graph.add_edge(word1, word2)
    return the_graph

def bfs(start):
    start.distance = 0
    start.previous = None
    vert_queue = Queue()
    vert_queue.enqueue(start)
    while vert_queue.size() > 0:
        current = vert_queue.dequeue()
        for neighbor in current.get_neighbors():
            if neighbor.color == "white":
                neighbor.color = "gray"
                neighbor.distance = current.distance + 1
                neighbor.previous = current
                vert_queue.enqueue(neighbor)
        current.color = "black"

def traverse(starting_vertex):
    current = starting_vertex
    while current:
        print(current.key, end="")
        if current.previous:
            print("->", end="")
        current = current.previous

g = build_graph(["fool", "cool", "pool", "poll", "pole", "pall", "fall",
                 "fail", "foil", "foul", "pope", "pale", "sale", "sage", "page"])
bfs(g.get_vertex("fool"))
traverse(g.get_vertex("sage"))
print()
for key in sorted(g.get_vertices()):        # 單字（與 fool 的距離）
    print(f"{key}({g.get_vertex(key).distance})", end=" ")
print()"""

bfs = f'''<h3 id="dx-bfs">講義完整範例：Word Ladder 的實際執行</h3>
{card("講義 08 · build_graph + bfs + traverse：從 fool 爬到 sage", C_BFS, run_py(PDS + C_BFS), out_label="實跑輸出（回溯路徑可能因探索順序略異，長度必為 6 步）",
note="bucket 建圖是亮點：po_l 這種「挖一格」的鍵把只差一字母的字放進同一桶，避免 O(n²) 兩兩比對。traverse 印的是 previous 鏈：BFS 建好的其實是一棵「最短路徑樹」，任何字回溯到 fool 都是最短路。")}'''
s, c2 = insert_end_of_section(s, "bfs", bfs, 'id="dx-bfs"')

C_DFS = """from pythonds3.graphs import Graph

class DFSGraph(Graph):
    def __init__(self):
        super().__init__()
        self._time = 0

    def dfs(self):
        for vertex in self:
            vertex.color = "white"
            vertex.previous = -1
        for vertex in self:
            if vertex.color == "white":
                self.dfs_visit(vertex)

    def dfs_visit(self, start):
        start.color = "gray"
        self._time = self._time + 1
        start.discovery_time = self._time
        for next_vertex in start.get_neighbors():
            if next_vertex.color == "white":
                next_vertex.set_previous(start)
                self.dfs_visit(next_vertex)
        start.color = "black"
        self._time = self._time + 1
        start.closing_time = self._time

g = DFSGraph()
g.add_edge('A', 'B'); g.add_edge('B', 'C')
g.add_edge('A', 'D'); g.add_edge('B', 'D')
g.add_edge('D', 'E'); g.add_edge('E', 'B')
g.add_edge('E', 'F'); g.add_edge('F', 'C')
g.dfs()

print(f"{'Key':^5}|{'Discover':^10}|{'Closing':^9}|{'Previous':^10}")
for key in sorted(g.get_vertices()):
    v = g.get_vertex(key)
    prev = v.previous.key if v.previous not in (None, -1) else ""
    print(f"{key:^5}|{v.discovery_time:^10}|{v.closing_time:^9}|{prev:^10}")"""

dfs = f'''{card("講義 08 · DFSGraph：discovery / closing time 全表", C_DFS, run_py(PDS + C_DFS),
note='<span id="dx-dfs"></span>對照括號性質：C 的 [3,4] 完全包在 B 的 [2,11] 裡（C 是 B 的子孫）；每個頂點的區間要嘛互相包住、要嘛完全分開，絕不交錯。E→B 那條邊指向還是灰色的祖先，是一條 back edge：它宣告圖裡有循環。')}'''
s, c3 = insert_end_of_section(s, "dfs", dfs, 'id="dx-dfs"')

C_DIJ = """from pythonds3.graphs import Graph
from pythonds3.trees.priority_queue import PriorityQueue

def dijkstra(graph, start):
    pq = PriorityQueue()
    start.distance = 0
    pq.heapify([(v.distance, v) for v in graph])
    while pq:
        distance, current_v = pq.delete()
        for next_v in current_v.get_neighbors():
            new_distance = current_v.distance + current_v.get_neighbor(next_v)
            if new_distance < next_v.distance:
                next_v.distance = new_distance
                next_v.previous = current_v
                pq.change_priority(next_v, new_distance)   # decrease-key！

def find_path(graph, start_key, end_key):
    current = graph.get_vertex(end_key)
    path = []
    while current is not None and current != graph.get_vertex(start_key):
        path.append(current.key)
        current = current.previous
    if current is None:
        return "No path"
    path.append(start_key)
    path.reverse()
    return path

g = Graph()   # 講義的 6 頂點範例圖（雙向邊）
for a, b, w in [('u','v',2), ('v','w',3), ('w','z',5), ('u','x',1), ('u','w',5),
                ('x','v',2), ('x','w',3), ('x','y',1), ('y','w',1), ('y','z',1)]:
    g.add_edge(a, b, w); g.add_edge(b, a, w)

dijkstra(g, g.get_vertex('u'))
for key in sorted(g.get_vertices()):   # 頂點: 距離 (previous)
    v = g.get_vertex(key)
    print(f"{key}: {v.distance} ({v.previous.key if v.previous else ''})")
print(" -> ".join(find_path(g, 'u', 'z')))"""

dij = f'''{card("講義 08 · dijkstra + find_path 的使用畫面", C_DIJ, run_py(PDS + C_DIJ),
note='<span id="dx-dij"></span>最生動的一格是 w：直達邊 u→w 權重 5，但演算法最後給它 3（u→x→y→w）。「先到的不一定是最短的」，所以 Dijkstra 允許在頂點還在優先佇列裡時<strong>下修</strong>它的距離（change_priority 就是 decrease-key）。u 到 z 的最短路是 u → x → y → z，總長 3。')}'''
s, c4 = insert_end_of_section(s, "dijkstra", dij, 'id="dx-dij"')

C_PRIM = """import sys as _sys
from pythonds3.graphs import Graph
from pythonds3.trees.priority_queue import PriorityQueue

def prim(graph, start):
    pq = PriorityQueue()
    for vertex in graph:
        vertex.distance = _sys.maxsize
        vertex.previous = None
    start.distance = 0
    pq.heapify([(vertex.distance, vertex) for vertex in graph])
    while not pq.is_empty():
        distance, current_v = pq.delete()
        for next_v in current_v.get_neighbors():
            new_distance = current_v.get_neighbor(next_v)   # 只看邊權，不累加
            if next_v in pq and new_distance < next_v.distance:
                next_v.previous = current_v
                next_v.distance = new_distance
                pq.change_priority(next_v, new_distance)

g = Graph()   # 講義的廣播範例圖（雙向邊）
for a, b, w in [('A','B',2), ('A','C',3), ('B','D',1), ('B','C',1),
                ('B','E',4), ('D','E',1), ('C','F',5), ('E','F',1), ('F','G',1)]:
    g.add_edge(a, b, w); g.add_edge(b, a, w)

prim(g, g.get_vertex('A'))
print("MST edges:", end=" ")
for key in sorted(g.get_vertices()):
    v = g.get_vertex(key)
    if v.previous is not None:
        print(f"({v.previous.key},{v.key})", end=" ")
print()"""

prm = f'''{card("講義 08 · prim 的使用畫面：長出 MST", C_PRIM, run_py(PDS + C_PRIM),
note='<span id="dx-prm"></span>六條邊、總權重 2+1+1+1+1+1 = 7，就是廣播訊息要走的樹。跟 Dijkstra 只差一行：new_distance 只看<strong>單條邊權</strong>、不累加路徑；「樹外頂點的入場券隨時可以換更便宜的」正是 Prim 的核心。')}'''
s, c5 = insert_end_of_section(s, "prim", prm, 'id="dx-prm"')

PAGE.write_text(s)
print("inserted:", [n for n, ok in zip("rep bfs dfs dij prim".split(), [c1, c2, c3, c4, c5]) if ok])
