from collections import deque, defaultdict
from typing import DefaultDict, List, Deque, Tuple


def dfs(
        graph: DefaultDict[int, List],
        initial: int,
        marks: DefaultDict[int, int],
        order: Deque = None,
        component: int = -1
       ) -> Tuple[Deque, DefaultDict[int, int]]:
    """
    Depth-first search of the graph.
    Traverses all the vertices in connected component, remembering
    times of vertices exiting stack. Marks vertices as belonging to the
    component if given its number.

    :param graph: adj. list representation - dict{node: list of adj. nodes};
    :param initial: vertex to start dfs from;
    :param marks: dict of marks of vertices;
                  If called to generate topological order of the graph, marks
                  is used to indicate if a vertex has been visited or not.
                  If called to generate marks of strongly connected components,
                  marks is where for each vertex we state its component's mark.
                  (0 if not visited, -1(or number of comp if given) else);
    :param order: topological order of the whole graph(all components) call
                  after another is accumulated here, starting from empty list;
    :param component: number of component to label all vertices in it;
    :return: order and marks with info about the vertices of the graph on
             which dfs has been called.
    """
    stack = deque()
    stack.append(initial)
    while stack:
        node = stack[-1]  # peek
        if marks[node] == 0:
            # 0 if not visited, -1(or number of comp) if visited
            marks[node] = component
            stack.extend(adj for adj in graph[node] if marks[adj] == 0)
        if node == stack[-1]:
            if order is not None:
                if node not in order:
                    order.appendleft(node)
            # pop only when all adjacent are visited and placed to list
            stack.pop()
    return order, marks


def transpose(graph: DefaultDict[int, List]) -> DefaultDict[int, List]:
    """
    Transposes adjacency list represented graph.

    :param graph: adj. list representation - dict{node: list of adj. nodes};
    :return: transposed graph adjacency list represented.
    """
    transposed_graph = defaultdict(list)
    for node in graph.keys():
        for neighbour in graph[node]:
            transposed_graph[neighbour].append(node)
    return transposed_graph


def find_components(graph: DefaultDict[int, List]) -> DefaultDict[int, int]:
    """
    Finds strongly connected components of the directed graph.

    :param graph: adj. list representation - dict{node: list of adj. nodes};
    :return: dict{vertex: its strongly connected component number}.
    """
    transposed_graph = transpose(graph)
    visited = defaultdict(int)
    order = deque()
    for node in graph.keys():
        order, visited = dfs(graph, node, visited, order)

    comp_number = 1
    components = defaultdict(int)
    for node in order:
        if components[node] == 0:
            _, components = dfs(
                                transposed_graph,
                                node,
                                components,
                                component=comp_number
                            )
            comp_number += 1
    return components
