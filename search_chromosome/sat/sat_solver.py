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
    Conjunctive normal form formula representation.
    """
    def __init__(self):
        self.variables = []
        self.variable_table = dict()
        self.clauses = []

    def parse_and_add_clause(self, line):
        """
        Parse conjunct from line and add its clause to the formula.

        :param line: line to be parsed;
        :return: -
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
        Parse conjuncts from each line of file and
        add its clause to the formula.
        One line - one conjunct with two variables.

        :param file: path to file;
        :return: -
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
        Transform literal to its string form.

        Looking up the variable in a literal is a matter of dividing by two,
        which is the same as a bit-wise shift to the right.
        """
        s = '!' if is_negated(literal) else ''
        return s + self.variables[literal >> 1]


def negate(x):
    """
    Switches a literal from negated to unnegated and back by
    doing a bit-wise XOR with the number one.

    :param x: literal;
    :return: !x.
    """
    return x ^ 1


def is_negated(x) -> bool:
    """
    Checks if a literal is negated or not by doing a bit-wise AND with 1.

    :param x: literal;
    :return: True if negated, else False.
    """
    return not (x & 1 == 0)


def graph_by_clauses(clauses: List[Tuple[int, int]]) -> DefaultDict[int, List]:
    """
    Builds adj. list represented implication graph from clauses of the CNF.

    :param clauses: clauses of the formula;
    :return: implication graph.
    """
    graph = defaultdict(list)
    for clause in clauses:
        x, y = clause  # encoded literals
        graph[negate(x)].append(y)
        graph[negate(y)].append(x)
        graph[x].extend([])
        graph[y].extend([])
    return graph


def nodes_in_components(
        components: DefaultDict[int, int]
) -> DefaultDict[int, List]:
    """
    Forms a dict where for each component's number we
    have all the vertices in it.

    :param components: dict{vertex: number of its component};
    :return: dict{component number: [vertices inside component]}.
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
    Build condensate of the given implication graph.

    :param graph: implication graph adj. list represented;
    :param components: components: dict{vertex: number of its component};
    :return: condensate graph.
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
    Resolves 2-SAT problem
    (if no solution exists NoSolution exception is thrown).

    :param formula: CNF formula;
    :return: dict{variable: its boolean value}.
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
