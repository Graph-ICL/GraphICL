import networkx as nx
from networkx.algorithms import isomorphism
import re
import itertools
from collections import deque
from collections import defaultdict


def extract_edges_a(input_str):

    edges_start = input_str.find("edges are:")
    if edges_start == -1:
        raise ValueError("'edges are:' ")
    

    edges_str = input_str[edges_start + len("edges are:"):].split(".")[0].strip()
    

    edges = []
    for edge in edges_str.split(")"): 
        edge = edge.strip()  
        if not edge:  
            continue
   
        edge = edge.lstrip("(")
        nodes = edge.split(",")
        if len(nodes) != 2: 
            continue
        try:
        
            u = int(nodes[0].strip())
            v = int(nodes[1].strip())
            edges.append((u, v))
        except ValueError:
        
            continue
    return edges


def extract_edges_b(input_str):

    edges_start = input_str.find("edges are:")
    if edges_start == -1:
 
    

    edges_str = input_str[edges_start + len("edges are:"):].split(".")[0].strip()
    

    edges = []
    for edge in edges_str.split():

        edge = edge.strip("()")
        if not edge:
            continue
        nodes = edge.split("->")
        if len(nodes) != 2: 
            continue
        try:

            u = int(nodes[0].strip())
            v = int(nodes[1].strip())
            edges.append((u, v))
        except ValueError:
 
            continue
    return edges


def extract_edges_c(input_str):

    edges_start = input_str.find("edges are:")
    if edges_start == -1:
 
    

    edges_str = input_str[edges_start + len("edges are:"):].split(".")[0].strip()
    
    # 解析边
    edges = []
    for edge in edges_str.split():
        # 去掉括号并分割节点和权重
        edge = edge.strip("(),")
        if not edge:  # 如果边为空，跳过
            continue
        parts = edge.split(",")
        if len(parts) != 3:  # 确保边的格式正确
            continue
        try:
            # 将节点和权重转换为整数
            u = int(parts[0].strip())
            v = int(parts[1].strip())
            w = int(parts[2].strip())
            edges.append((u, v, w))
        except ValueError:
            # 如果转换失败，跳过该边
            continue
    return edges


def extract_edges_d(input_str):
    """
    字符串中建图 (i->j,k) 式
    :param input_str: 输入字符串
    :return: 边的列表
    """
    # 使用正则表达式提取所有 (i->j,k) 格式的数据
    matches = re.findall(r'\(\s*(\d+)\s*->\s*(\d+)\s*,\s*(\d+)\s*\)', input_str)

    # 将提取的数据转换为列表
    edges = [(int(i), int(j), int(k)) for i, j, k in matches]
    return edges


def extract_edges_subgraph(input_str):
    """
    字符串中建图 (i->j) 式
    :param input_str: 输入字符串
    :return: 图 G 边的列表和子图 G' 边的列表
    """
    # 提取图 G 的边信息
    g_edges_matches = re.findall(r'\(\s*(\d+)\s*->\s*(\d+)\s*\)', input_str)

    # 将提取的数据转换为列表
    g_edges = [(int(u), int(v)) for u, v in g_edges_matches]

    # 找到 G 边的部分
    edges_start = input_str.find("edges are:")
    if edges_start == -1:
        raise ValueError("输入字符串中没有找到 'edges are:' 部分")
    # 找到 G' 边的部分
    edges_start = input_str.find("edges are:",edges_start + 1)
    if edges_start == -1:
        raise ValueError("输入字符串中没有找到 'edges are:' 部分")

    # 提取子图 G' 的边信息
    g_prime_edges_matches = re.findall(r'\(\s*([a-o])\s*->\s*([a-o])\s*\)', input_str[edges_start:])

    # 将提取的数据转换为列表
    g_prime_edges = [(u, v) for u, v in g_prime_edges_matches]

    return g_edges, g_prime_edges

### "from a to b" 提取 node1: a 和 node2: b
def extract_nodes(input_str):
    """
    从问题中提取节点
    :param question: 问题字符串，例如 "Is there a path between node 3 and node 8?"
    :return: 节点 1 和节点 2
    """
    # 找到边的部分
    edges_start = input_str.find("edges are:")
    if edges_start == -1:
        raise ValueError("输入字符串中没有找到 'edges are:' 部分")
    
    # 提取边的字符串
    question = input_str[edges_start + len("edges are:"):].split(".")[1].strip()

    # 找到 "node X and node Y" 的部分
    node_part = question.split("node")[1:]  # 分割字符串，提取节点部分
    if len(node_part) < 2:
        raise ValueError("问题中没有找到两个节点")
    
    # 提取节点
    node1 = int(node_part[0].strip().split()[0])  # 提取第一个节点
    number2 = re.search(r"\d+", node_part[1].strip().split()[0]).group()
    node2 = int(number2)  # 提取第二个节点
    return node1, node2

def extract_node_weights(input_str):
    """
    字符串中提取节点权重信息 [i, k] i 代表节点编号,k 代表节点权重
    :param input_str: 输入字符串
    :return: 节点权重的列表
    """
    # 使用正则表达式提取所有 [i, k] 格式的数据
    matches = re.findall(r'\[\s*(\d+)\s*,\s*(\d+)\s*\]', input_str)

    # 将提取的数据转换为列表
    node_weights = [[int(i), int(k)] for i, k in matches]
    return node_weights

def extract_node_num(input_str):
    """
    从输入字符串中提取节点的数量
    :param input_str: 输入字符串
    :return: 节点的数量
    """
    # 提取节点编号范围
    node_range_match = re.search(r'nodes are numbered from (\d+) to (\d+)', input_str)
    if node_range_match:
        start_node = int(node_range_match.group(1))
        end_node = int(node_range_match.group(2))
        num_nodes = end_node - start_node + 1
    else:
        num_nodes = 0  # 如果没有找到节点范围，默认节点数为 0
    return num_nodes


### cycle 问题
def has_cycle(edges):
    """
    判断无向图中是否存在环
    :param edges: 图的边列表，例如 [(0, 1), (1, 2), (2, 0)]
    :return: Yes 或 No
    """
    # 创建无向图
    G = nx.Graph()
    G.add_edges_from(edges)

    # 检测是否存在环
    try:
        # 如果找到环，返回 Yes
        nx.find_cycle(G)
        return "### Yes"
    except nx.NetworkXNoCycle:
        # 如果没有环，返回 No
        return "### No"

# 示例输入
# edges = [(0, 1), (1, 2), (2, 0)]  # 这是一个有环的图
# edges = [(0, 1), (1, 2)]  # 这是一个无环的图
 


### connect 问题
def are_nodes_connected(edges, node1, node2):
    """
    判断无向图中两个节点是否连通
    :param edges: 图的边列表，例如 [(0, 1), (1, 2)]
    :param node1: 第一个节点
    :param node2: 第二个节点
    :return: Yes 或 No
    """
    # 创建无向图
    G = nx.Graph()

    # 添加所有节点（确保所有节点都存在）
    all_nodes = set()
    for u, v in edges:
        all_nodes.add(u)
        all_nodes.add(v)
    G.add_nodes_from(all_nodes)

    # 添加边
    G.add_edges_from(edges)

    # 检查节点是否存在于图中
    if node1 not in G or node2 not in G:
        return "### No"  # 如果节点不存在，直接返回 No

    # 判断两个节点是否连通
    if nx.has_path(G, node1, node2):
        return "### Yes"
    else:
        return "### No"

# # 示例输入
# edges = [(0, 1), (1, 2), (2, 3)]  # 图的边
# node1 = 0  # 第一个节点
# node2 = 3  # 第二个节点

# # 判断是否连通
# result = are_nodes_connected(edges, node1, node2)
# print(f"节点 {node1} 和节点 {node2} 是否连通: {result}")


### bipartite 问题
def is_bipartite(edges):
    """
    判断有向图是否是二分图
    :param edges: 图的边列表，例如 [(0, 1), (1, 2)]
    :return: Yes 或 No
    """
    # 创建有向图
    G = nx.DiGraph()
    G.add_edges_from(edges)

    # 将有向图转换为无向图（二分图判断通常针对无向图）
    G_undirected = G.to_undirected()

    # 判断是否是二分图
    if nx.is_bipartite(G_undirected):
        return "### Yes"
    else:
        return "### No"

# # 示例输入
# edges = [(0, 1), (1, 2), (2, 3)]  # 图的边

# # 判断是否是二分图
# result = is_bipartite(edges)
# print("图是否是二分图:", result)


### topology 问题
def topological_sort(edges):
    """
    计算有向图的拓扑排序
    :param edges: 图的边列表，例如 [(0, 1), (1, 2)]
    :return: 拓扑排序的节点列表
    """
    # 创建有向图
    G = nx.DiGraph()
    G.add_edges_from(edges)

    # 计算拓扑排序
    try:
        sorted_nodes = list(nx.topological_sort(G))
        return "### " + str(sorted_nodes)
    except nx.NetworkXUnfeasible:
        return "### The graph has rings and cannot be topologically sorted"
        检查图中是否有环
    # if not nx.is_directed_acyclic_graph(G):
    #     return "### The graph has rings and cannot be topologically sorted"

    # # 计算所有拓扑排序
    # all_sorts = list(nx.all_topological_sorts(G))
    # return "### " + str(all_sorts)

# # 示例输入
# edges = [(0, 1), (1, 2), (2, 3)]  # 图的边

# # 计算拓扑排序
# result = topological_sort(edges)
# print("拓扑排序结果:", result)


### shortest path 问题
def shortest_path_weight(edges, node1, node2):
    """
    计算无向加权图中两个节点之间的最短路径的权重
    :param edges: 图的边列表，例如 [(0, 1, 3), (0, 3, 1), (1, 2, 4)]
    :param node1: 第一个节点
    :param node2: 第二个节点
    :return: 最短路径的权重
    """
    # 创建无向图
    G = nx.Graph()

    # 添加所有节点（确保所有节点都存在）
    all_nodes = set()
    for u, v, w in edges:
        all_nodes.add(u)
        all_nodes.add(v)
    G.add_nodes_from(all_nodes)

    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    # 检查节点是否存在于图中
    if node1 not in G or node2 not in G:
        return "### There is no path between nodes"  # 如果节点不存在，直接返回

    # 计算最短路径的权重
    try:
        weight = nx.dijkstra_path_length(G, node1, node2)
        return "### " + str(weight)
    except nx.NetworkXNoPath:
        return "### There is no path between nodes"

# # 示例输入
# edges = [(0, 1, 3), (0, 3, 1), (1, 2, 4)]  # 图的边（u, v, w）
# node1 = 1  # 第一个节点
# node2 = 3  # 第二个节点

# # 计算最短路径的权重
# result = shortest_path_weight(edges, node1, node2)
# print(f"节点 {node1} 和节点 {node2} 之间的最短路径的权重:", result)


### triangle 问题
def max_weight_of_triangle(node_weights, edges):
    """
    计算三个相互连接的节点的权重之和的最大值
    :param node_weights: 节点的权重列表，例如 [[0, 2], [1, 3], [2, 1], [3, 4]]
    :param edges: 图的边列表，例如 [(0, 1), (1, 2), (2, 0), (2, 3)]
    :return: 最大权重和
    """
    # 创建无向图
    G = nx.Graph()
    for u, v in edges:
        G.add_edge(u, v)

    # 将节点权重存储为字典
    weights = {node: weight for node, weight in node_weights}

    max_sum = -float("inf")  # 初始化最大权重和

    # 遍历所有三元组
    for u in G.nodes:
        for v in G.neighbors(u):
            for w in G.neighbors(v):
                if G.has_edge(u, w):  # 检查是否形成三角形
                    # 计算权重和
                    current_sum = weights[u] + weights[v] + weights[w]
                    if current_sum > max_sum:
                        max_sum = current_sum

    return "### "+ str(max_sum) if max_sum != -float("inf") else "### No triples satisfy the condition"

# # 示例输入
# node_weights = [[0, 2], [1, 3], [2, 1], [3, 4]]  # 节点的权重
# edges = [(0, 1), (1, 2), (2, 0), (2, 3)]  # 图的边

# # 计算最大权重和
# result = max_weight_of_triangle(node_weights, edges)
# print("三个相互连接的节点的权重之和的最大值:", result)

### maximum flow 问题
def max_flow(edges, source, target):
    """
    计算有向图中两个节点之间的最大流
    :param edges: 图的边列表，例如 [(0, 1, 2), (1, 2, 3)]
    :param source: 源节点
    :param target: 汇节点
    :return: 最大流的值，格式为 "### <value>" 或 "### 0"
    """
    # 创建有向图
    G = nx.DiGraph()

    # 添加所有节点（确保所有节点都存在）
    all_nodes = set()
    for u, v, w in edges:
        all_nodes.add(u)
        all_nodes.add(v)
    G.add_nodes_from(all_nodes)

    # 添加边
    for u, v, w in edges:
        G.add_edge(u, v, capacity=w)

    # 检查是否存在从 source 到 target 的路径
    if source not in G or target not in G:
        return "### 0"

    # 计算最大流
    flow_value, flow_dict = nx.maximum_flow(G, source, target)
    return "### " + str(flow_value)

# # 示例输入
# edges = [(0, 1, 2), (1, 2, 3), (2, 3, 1)]  # 图的边（u, v, w）
# source = 0  # 源节点
# target = 3  # 汇节点

# # 计算最大流
# result = max_flow(edges, source, target)
# print(f"节点 {source} 和节点 {target} 之间的最大流:", result)

### hamilton 问题
def has_hamiltonian_path(edges, num_nodes):
    """
    判断无向图中是否存在哈密顿路径（动态规划）
    :param edges: 图的边列表，例如 [(0, 1), (1, 2)]
    :param num_nodes: 图的节点数量
    :return: Yes 或 No
    """
    # 构建 NetworkX 图
    G = nx.Graph()
    G.add_edges_from(edges)
    
    # 边界条件判断
    if num_nodes == 0:
        return "### No"
    if num_nodes == 1:
        return "### Yes"
    
    # 检查图是否连通
    if not nx.is_connected(G):
        return "### No"
    
    # 构建邻接表
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # 动态规划表
    dp = [[False] * num_nodes for _ in range(1 << num_nodes)]

    # 初始化：单个节点的路径
    for i in range(num_nodes):
        dp[1 << i][i] = True

    # 状态转移
    for mask in range(1 << num_nodes):  # 遍历所有子集
        for u in range(num_nodes):
            if dp[mask][u]:  # 如果当前状态有效
                for v in graph[u]:  # 遍历邻居
                    if not (mask & (1 << v)):  # 如果 v 未被访问
                        dp[mask | (1 << v)][v] = True

    # 检查是否存在哈密顿路径
    for u in range(num_nodes):
        if dp[(1 << num_nodes) - 1][u]:
            return "### Yes"
    return "### No"

# # 示例输入
# edges = [(0, 1), (1, 2), (2, 3)]  # 图的边
# num_nodes = 4  # 节点数量

# # 判断是否存在哈密顿路径
# result = has_hamiltonian_path(edges, num_nodes)
# print("是否存在哈密顿路径:", result)

### subgraph 问题
def is_subgraph(G_edges, G_prime_edges):
    """
    判断有向图 G' 是否是 G 的子图（精确匹配）
    :param G_edges: 大图 G 的边列表，例如 [(0, 1), (1, 2)]
    :param G_prime_edges: 子图 G' 的边列表，例如 [(a, b)]
    :return: Yes 或 No
    """
    # 创建大图 G 和子图 G'
    G = nx.DiGraph()
    G.add_edges_from(G_edges)

    G_prime = nx.DiGraph()
    G_prime.add_edges_from(G_prime_edges)

    # 获取节点列表
    G_nodes = list(G.nodes())
    G_prime_nodes = list(G_prime.nodes())

    # 如果子图的节点数大于大图的节点数，直接返回 No
    if len(G_prime_nodes) > len(G_nodes):
        return "### No"

    # 生成所有可能的映射
    for mapping_nodes in itertools.permutations(G_nodes, len(G_prime_nodes)):
        # 创建映射字典
        mapping = {G_prime_nodes[i]: mapping_nodes[i] for i in range(len(G_prime_nodes))}
        # 检查子图的边是否在大图中存在
        is_valid = True
        for edge in G_prime_edges:
            mapped_edge = (mapping[edge[0]], mapping[edge[1]])
            if mapped_edge not in G_edges:
                is_valid = False
                break
        # 如果找到有效的映射，返回 Yes
        if is_valid:
            return f"### Yes"
    # 如果没有找到有效的映射，返回 No
    return "### No"

# # 示例输入
# G_edges = [(0, 1), (1, 2), (2, 3)]  # 大图 G 的边
# G_prime_edges = [(0, 1), (1, 2)]  # 子图 G' 的边

# # 判断子图同构
# result = is_subgraph(G_edges, G_prime_edges)
# print("子图 G' 是否是大图 G 的子图（精确匹配）:", result)


