import pytest
from search_chromosome.sat.components import find_components
from search_chromosome.sat.test.util import read_graph_from_file
from typing import DefaultDict, List, Dict


class Case:
    def __init__(self, name: str, G: DefaultDict[int, List], comps: Dict):
        self._name = name
        self.G = G
        self.comps = comps

    def __str__(self) -> str:
        return 'task1_test_{}'.format(self._name)


TEST_CASES = [
    Case(
        name='graph_basic',
        G=read_graph_from_file("graph_basic.txt"),
        comps={1: 1}
    ),
    Case(
        name='graph_all_single',
        G=read_graph_from_file("graph_all_single.txt"),
        comps={9: 1, 10: 2, 11: 3, 1: 4, 2: 5, 4: 6, 3: 7, 5: 8, 7: 9, 8: 10, 6: 11}
    ),
    Case(
        name='graph_1',
        G=read_graph_from_file("graph_1.txt"),
        comps={0: 1, 2: 2, 4: 3, 6: 4, 5: 5, 1: 5, 3: 5, 7: 6}
    ),
    Case(
        name='graph_3',
        G=read_graph_from_file("graph_3.txt"),
        comps={4: 1, 2: 2, 0: 3, 1: 3, 3: 3, 5: 4, 6: 4, 7: 5}
    ),
    Case(
        name='graph_4',
        G=read_graph_from_file("graph_4.txt"),
        comps={5: 1, 7: 1, 6: 2, 2: 3, 4: 4, 1: 5, 0: 6, 3: 7}
    )
]


@pytest.mark.parametrize('case', TEST_CASES, ids=str)
def test_task1(case: Case) -> None:
    answer = find_components(graph=case.G)
    assert answer == case.comps
