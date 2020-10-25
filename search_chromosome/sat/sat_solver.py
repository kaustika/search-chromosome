from collections import deque, defaultdict
from typing import DefaultDict, List, Tuple, Dict
from search_chromosome.sat.components import find_components, dfs


class TwoSatException(Exception):
    """
    Base class for other exceptions.
    """
    pass


class NoSolution(TwoSatException):
    """
    Raised when CNF formula has no solution.
    It happens when x and !x are in the same strongly connected component.
    """
    def __init__(self, message="This CNF formula has no solution!"):
        self.message = message
        super().__init__(self.message)


class Input:
    """

    """
    def __init__(self):
        self.variables = []
        self.variable_table = dict()
        self.clauses = []

    def parse_and_add_clause(self, line):
        """

        :param line:
        :return:
        """
        clause = list()
        for literal in line.split():
            negated = 1 if literal.startswith('!') else 0
            variable = literal[negated:]
            if variable not in self.variable_table:
                self.variable_table[variable] = len(self.variables)
                self.variables.append(variable)
            encoded_literal = self.variable_table[variable] << 1 | negated
            clause.append(encoded_literal)
        self.clauses.append(tuple(clause))

    @classmethod
    def from_file(cls, file):
        """

        :param file:
        :return:
        """
        instance = cls()
        with open(file) as f:
            for line in f:
                line = line.strip()
                if len(line) > 0 and not line.startswith('#'):
                    instance.parse_and_add_clause(line)
        return instance

    def literal_to_string(self, literal):
        """

        :param literal:
        :return:
        """
        s = '!' if literal & 1 else ''
        return s + self.variables[literal >> 1]


def negate(x):
    """

    :param x:
    :return:
    """
    return x ^ 1


def is_negated(x) -> bool:
    """

    :param x:
    :return:
    """
    return not (x & 1 == 0)


def graph_by_clauses(clauses: List[Tuple[int, int]]) -> DefaultDict[int, List]:
    """

    :param clauses:
    :return:
    """
    graph = defaultdict(list)
    for clause in clauses:
        x, y = clause  # encoded literals
        graph[negate(x)].append(y)
        graph[negate(y)].append(x)
        graph[x].extend([])
        graph[y].extend([])
    return graph


def nodes_in_components(components: DefaultDict[int, int]) -> DefaultDict[int, List]:
    """

    :param components:
    :return:
    """
    content = defaultdict(list)
    for node, comp in components.items():
        content[comp].append(node)
    return content


def components_to_condensate(
        graph: DefaultDict[int, List],
        components: DefaultDict[int, int]
) -> Tuple[DefaultDict[int, List], DefaultDict[int, List]]:
    """

    :param graph:
    :param components:
    :return:
    """
    content = nodes_in_components(components)
    condensate = defaultdict(list)
    for comp in content.keys():
        for node in content[comp]:
            adj_comps = [components[adj] for adj in graph[node]]
            condensate[comp].extend(adj_comps)
    return condensate, content


def solve_2_sat(formula: Input) -> Dict[str, bool]:
    """

    :param formula:
    :return:
    """
    top_order = deque()
    visited = defaultdict(int)
    answer, var_values = dict(), dict()

    graph = graph_by_clauses(formula.clauses)
    components = find_components(graph)
    condensate, content = components_to_condensate(graph, components)

    for node in condensate.keys():
        top_order, visited = dfs(condensate, node, visited, top_order)

    for component in top_order:
        nodes_of_comp = content[component]
        for node in nodes_of_comp:
            if components[negate(node)] == components[node]:
                raise NoSolution
            answer[node] = True
            answer[negate(node)] = False

    for node in answer.keys():
        if not is_negated(node):  # not negated literals go to the answer
            var_values[formula.literal_to_string(node)] = answer[node]
    return var_values
