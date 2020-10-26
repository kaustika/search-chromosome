import pytest
from typing import Dict

from search_chromosome.sat.sat_solver import solve_2_sat, Input, NoSolution
from search_chromosome.sat.test.util import abspath


class Case:
    def __init__(self, name: str, formula: Input, var_values: Dict[str, bool]):
        self._name = name
        self.formula = formula
        self.var_values = var_values

    def __str__(self) -> str:
        return 'two_sat_solver_test_{}'.format(self._name)


TEST_CASES = [
    Case(
        name='formula_empty',
        formula=Input(),
        var_values={}
    ),
    Case(
        name='formula_trivial',
        formula=Input().from_file(abspath("trivial.txt", __file__)),
        var_values={'x1': True}
    ),
    Case(
        name='formula_basic',
        formula=Input().from_file(abspath("basic.txt", __file__)),
        var_values={'x1': True, 'x2': True, 'x3': True, 'x4': True}
    ),
    Case(
        name='formula_1',
        formula=Input().from_file(abspath("sat_case1.txt", __file__)),
        var_values={'a': False, 'b': False, 'c': False}
    ),
    Case(
        name='formula_2',
        formula=Input().from_file(abspath("sat_case2.txt", __file__)),
        var_values={'x': True, 'y': True, 'z': True}
    ),
    Case(
        name='formula_3',
        formula=Input().from_file(abspath("sat_case3.txt", __file__)),
        var_values={'a': True, 'b': False, 'c': False}
    )
]


@pytest.mark.parametrize('case', TEST_CASES, ids=str)
def test_two_sat_solver(case: Case) -> None:
    answer = solve_2_sat(formula=case.formula)
    assert answer == case.var_values


def test_no_solution() -> None:
    with pytest.raises(NoSolution):
        solve_2_sat(Input().from_file(abspath("no_solution.txt", __file__)))
