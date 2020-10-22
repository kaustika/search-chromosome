from collections import deque, defaultdict
from typing import DefaultDict, List, Deque, Tuple


def dfs(
        graph: DefaultDict[str, List],
        initial: str,
        marks: DefaultDict[str, int],
        order: Deque = None,
        component: int = -1
       ) -> Tuple[Deque, DefaultDict[str, int]]:
    """

    :param graph:
    :param initial:
    :param marks:
    :param order:
    :param component:
    :return:
    """
    stack = deque()
    stack.append(initial)
    while stack:
        node = stack[-1]  # peek
        if marks[node] == 0:  # 0 if not visited, -1(or number of comp) if visited
            marks[node] = component
            stack.extend(adj for adj in graph[node] if marks[adj] == 0)
        if node == stack[-1]:
            if order is not None:
                if node not in order:
                    order.appendleft(node)
                # pop only when all adjacent are visited and placed to list
            stack.pop()
    return order, marks


def transpose(graph: DefaultDict[str, List]) -> DefaultDict[str, List]:
    """

    :param graph:
    :return:
    """
    transposed_graph = defaultdict(list)
    for node in graph.keys():
        for neighbour in graph[node]:
            transposed_graph[neighbour].append(node)
    return transposed_graph


def find_components(graph: DefaultDict[str, List]) -> DefaultDict[str, int]:
    """

    :param graph:
    :return:
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
            _, components = dfs(transposed_graph, node, components, component=comp_number)
            comp_number += 1
    return components
