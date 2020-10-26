import pytest

from search_chromosome.sat.components import find_components
from search_chromosome.sat.test.util import read_graph_from_file, abspath
from typing import DefaultDict, List, Dict


class Case:
    def __init__(self, name: str, G: DefaultDict[int, List], comps: Dict):
        self._name = name
        self.G = G
        self.comps = comps

    def __str__(self) -> str:
        return 'connected_components_test_{}'.format(self._name)


TEST_CASES = [
    Case(
        name='graph_empty',
        G=read_graph_from_file(abspath("graph_empty.txt", __file__)),
        comps={}
    ),
    Case(
        name='graph_basic',
        G=read_graph_from_file(abspath("graph_basic.txt", __file__)),
        comps={1: 1}
    ),
    Case(
        name='graph_all_single',
        G=read_graph_from_file(abspath("graph_all_single.txt", __file__)),
        comps={9: 1, 10: 2, 11: 3, 1: 4, 2: 5, 4: 6,
               3: 7, 5: 8, 7: 9, 8: 10, 6: 11}
    ),
    Case(
        name='graph_1',
        G=read_graph_from_file(abspath("graph_1.txt", __file__)),
        comps={0: 1, 2: 2, 4: 3, 6: 4, 5: 5, 1: 5, 3: 5, 7: 6}
    ),
    Case(
        name='graph_2',
        G=read_graph_from_file(abspath("graph_2.txt", __file__)),
        comps={4: 1, 2: 2, 0: 3, 1: 3, 3: 3, 5: 4, 6: 4, 7: 5}
    ),
    Case(
        name='graph_3',
        G=read_graph_from_file(abspath("graph_3.txt", __file__)),
        comps={5: 1, 7: 1, 6: 2, 2: 3, 4: 4, 1: 5, 0: 6, 3: 7}
    ),
    Case(
        name='graph_4',
        G=read_graph_from_file(abspath("graph_4.txt", __file__)),
        comps={1: 1, 5: 1, 2: 1, 7: 1, 4: 1, 3: 2, 6: 3, 9: 3, 8: 3}
    ),
    Case(
        name='graph_5',
        G=read_graph_from_file(abspath("graph_5.txt", __file__)),
        comps={1: 1, 3: 1, 2: 1, 5: 1, 4: 1, 6: 2, 9: 2, 7: 2, 8: 2,
               11: 3, 12: 3, 10: 4, 16: 5, 14: 5, 15: 5, 13: 6}
    )
]


@pytest.mark.parametrize('case', TEST_CASES, ids=str)
def test_connected_components(case: Case) -> None:
    answer = find_components(graph=case.G)
    assert answer == case.comps
