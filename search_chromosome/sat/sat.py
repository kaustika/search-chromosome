from collections import deque, defaultdict
from typing import DefaultDict, List, Tuple, Dict
from search_chromosome.sat.components import find_components, dfs


class Input:
    def __init__(self):
        self.variables = []
        self.variable_table = dict()
        self.clauses = []

    def parse_and_add_clause(self, line):
        clause = []
        for literal in line.split():
            negated = 1 if literal.startswith('!') else 0
            variable = literal[negated:]
            if variable not in self.variable_table:
                self.variable_table[variable] = len(self.variables)
                self.variables.append(variable)
            encoded_literal = self.variable_table[variable] << 1 | negated
            clause.append(encoded_literal)
        self.clauses.append(tuple(set(clause)))

    @classmethod
    def from_file(cls, file):
        instance = cls()
        for line in file:
            line = line.strip()
            if len(line) > 0 and not line.startswith('#'):
                instance.parse_and_add_clause(line)
        return instance

    def literal_to_string(self, literal):
        s = '!' if literal & 1 else ''
        return s + self.variables[literal >> 1]


def negate(x):
    return x ^ 1


def is_negated(x) -> bool:
    return not (x & 1 == 0)


def graph_by_clauses(clauses: List[Tuple[int, int]]) -> DefaultDict[int, List]:
    graph = defaultdict(list)
    for clause in clauses:
        x, y = clause  # encoded literals
        graph[negate(x)].append(y)
        graph[negate(y)].append(x)
        graph[x].extend([])
        graph[y].extend([])
    return graph


def nodes_in_components(components: DefaultDict[int, int]) -> DefaultDict[int, List]:
    content = defaultdict(list)
    for node, comp in components.items():
        content[comp].append(node)
    return content


def components_to_condensate(
        graph: DefaultDict[int, List],
        components: DefaultDict[int, int]
) -> Tuple[DefaultDict[int, List], DefaultDict[int, List]]:
    content = nodes_in_components(components)
    condensate = defaultdict(list)
    for comp in content.keys():
        for node in content[comp]:
            adj_comps = [components[adj] for adj in graph[node]]
            condensate[comp].extend(adj_comps)
    return condensate, content


def solve_2_sat(formula: Input) -> Dict[str, bool]:
    top_order = deque()
    visited = defaultdict(int)
    answer, val_values = dict(), dict()

    graph = graph_by_clauses(formula.clauses)
    components = find_components(graph)
    condensate, content = components_to_condensate(graph, components)

    for node in condensate.keys():
        top_order, visited = dfs(condensate, node, visited, top_order)

    for component in top_order:
        for node in content[component]:
            answer[node] = True
            answer[negate(node)] = False

    for node in answer.keys():
        if not is_negated(node):  # not negated literals go to the answer
            val_values[formula.literal_to_string(node)] = answer[node]
    return val_values


if __name__ == "__main__":
    f = Input()
    f.parse_and_add_clause("x1 !x2")
    f.parse_and_add_clause("x3 !x4")
    # print(f.variables)       # ['x1', 'x2', 'x3', 'x4']
    # print(f.variable_table)  # {'x1': 0, 'x2': 1, 'x3': 2, 'x4': 3}
    # print(f.clauses)         # [(0, 3), (4, 7)]

    print(solve_2_sat(f))