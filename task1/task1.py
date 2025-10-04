from collections import deque, defaultdict
from copy import deepcopy

# Вершини терміналів 
terminals = ["Термінал 1", "Термінал 2"]

# Вершини складів 
warehouses = ["Склад 1", "Склад 2", "Склад 3", "Склад 4"]

# Вершини магазинів 
stores = [f"Магазин {i}" for i in range(1, 15)]

# Ребра з пропускними здатностями 
edges = [
    ("Термінал 1", "Склад 1", 25),
    ("Термінал 1", "Склад 2", 20),
    ("Термінал 1", "Склад 3", 15),
    ("Термінал 2", "Склад 3", 15),
    ("Термінал 2", "Склад 4", 30),
    ("Термінал 2", "Склад 2", 10),
    ("Склад 1", "Магазин 1", 15),
    ("Склад 1", "Магазин 2", 10),
    ("Склад 1", "Магазин 3", 20),
    ("Склад 2", "Магазин 4", 15),
    ("Склад 2", "Магазин 5", 10),
    ("Склад 2", "Магазин 6", 25),
    ("Склад 3", "Магазин 7", 20),
    ("Склад 3", "Магазин 8", 15),
    ("Склад 3", "Магазин 9", 10),
    ("Склад 4", "Магазин 10", 20),
    ("Склад 4", "Магазин 11", 10),
    ("Склад 4", "Магазин 12", 15),
    ("Склад 4", "Магазин 13", 5),
    ("Склад 4", "Магазин 14", 10),
]

base_nodes = terminals + warehouses + stores
SRC = "Джерело"
SINK = "Сток"
nodes = [SRC] + base_nodes + [SINK]

idx = {name: i for i, name in enumerate(nodes)}
n = len(nodes)

# Матриця пропускних здатностей 
C = [[0] * n for _ in range(n)]
for u, v, c in edges:
    C[idx[u]][idx[v]] = c

# Додаємо ребра Джерело → Термінали 
out_sum = defaultdict(int)
for u, v, c in edges:
    if u in terminals:
        out_sum[u] += c
for t in terminals:
    C[idx[SRC]][idx[t]] = out_sum[t]

# Додаємо ребра Магазини → Сток 
incoming_store = {}
for u, v, c in edges:
    if v in stores:
        incoming_store[v] = c
for s in stores:
    C[idx[s]][idx[SINK]] = incoming_store.get(s, 0)

def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True
    parent[source] = -1

    while queue:
        current_node = queue.popleft()
        for neighbor in range(len(capacity_matrix)):
            # чи є залишкова пропускна здатність?
            if (not visited[neighbor] and
                capacity_matrix[current_node][neighbor] - flow_matrix[current_node][neighbor] > 0):
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)
    return False

def edmonds_karp(capacity_matrix, source, sink):
    num_nodes = len(capacity_matrix)
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]  # початковий потік = 0
    parent = [-1] * num_nodes
    max_flow = 0

    # поки існує збільшуючий шлях — нарощуємо потік
    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        # знаходимо вузьке місце на знайденому шляху
        path_flow = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, capacity_matrix[u][v] - flow_matrix[u][v])
            v = u
        # оновлюємо потоки вздовж шляху враховуючи зворотні ребра)
        v = sink
        while v != source:
            u = parent[v]
            flow_matrix[u][v] += path_flow
            flow_matrix[v][u] -= path_flow
            v = u
        max_flow += path_flow

    return max_flow, flow_matrix

max_flow, F = edmonds_karp(C, idx[SRC], idx[SINK])
print(f"Oптимальний потік досягнуто — він дорівнює {max_flow} одиниць.")
print("Це означає, що алгоритм знайшов максимально можливий обсяг постачання для цієї мережі, і далі збільшити його неможливо без зміни пропускних здатностей каналів.")

original_nodes = base_nodes[:]
names = nodes[:]
F_left = deepcopy(F)
terminal_store = defaultdict(int)

def next_positive_neighbors(Fmat, u_name):
    ui = idx[u_name]
    for v_i in range(n):
        if Fmat[ui][v_i] > 0:
            yield names[v_i]

def find_t_to_store_path(Fmat, t_name):
    stack = [(t_name, [t_name])]
    visited = set()
    while stack:
        u, path = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        if u in stores:
            return path
        for v in next_positive_neighbors(Fmat, u):
            if v not in path and v != SRC and v != SINK:
                stack.append((v, path + [v]))
    return None

for t in terminals:
    while True:
        path = find_t_to_store_path(F_left, t)
        if not path:
            break
        bneck = float('inf')
        for i in range(len(path)-1):
            u = idx[path[i]]
            v = idx[path[i+1]]
            bneck = min(bneck, F_left[u][v])
        for i in range(len(path)-1):
            u = idx[path[i]]
            v = idx[path[i+1]]
            F_left[u][v] -= bneck
        terminal_store[(t, path[-1])] += bneck

rows = []
for t in terminals:
    for s in stores:
        rows.append((t, s, int(terminal_store.get((t, s), 0))))

print("\nТермінал\tМагазин\tФактичний Потік (од.)")
for (t, s, f) in rows:
    print(f"{t}\t{s}\t{f}")

terminal_totals = defaultdict(int)
for (t, s), f in terminal_store.items():
    terminal_totals[t] += f

print("\nСума поставок по терміналах:")
for t in terminals:
    print(f"{t}: {terminal_totals[t]}")

print("\nНасичені ребра (flow == capacity):")
for u, v, c in edges:
    if F[idx[u]][idx[v]] == c:
        print(f"{u} -> {v}: {c}")

store_totals = {}
for s in stores:
    s_i = idx[s]
    tot = 0
    for u_name in nodes:
        tot += max(0, F[idx[u_name]][s_i])
    store_totals[s] = tot

least = sorted(store_totals.items(), key=lambda x: x[1])[:5]
print("\nМагазини з найменшою поставкою:")
for name, val in least:
    print(f"{name}: {val}")
