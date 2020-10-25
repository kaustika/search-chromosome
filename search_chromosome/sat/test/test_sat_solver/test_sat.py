from typing import Dict
import pytest

from search_chromosome.sat.sat_solver import solve_2_sat, Input, NoSolution


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
        formula=Input().from_file("trivial.txt"),
        var_values={'x1': True}
    ),
    Case(
        name='formula_basic',
        formula=Input().from_file("basic.txt"),
        var_values={'x1': True, 'x2': True, 'x3': True, 'x4': True}
    )
]


@pytest.mark.parametrize('case', TEST_CASES, ids=str)
def test_two_sat_solver(case: Case) -> None:
    answer = solve_2_sat(formula=case.formula)
    assert answer == case.var_values


def test_no_solution() -> None:
    with pytest.raises(NoSolution):
        solve_2_sat(Input().from_file("no_solution.txt"))
