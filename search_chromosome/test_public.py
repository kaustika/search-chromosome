import pytest
from typing import List, Tuple

from search_chromosome.search_chr import search_chromosome, NoGoodChromosome


class Case:
    def __init__(
            self, name: str,
            vars_on_chr: List[Tuple[int, int]],
            vars_present: List[Tuple[int, int]],
            vars_separated: List[Tuple[int, int]],
            good_chr_num: int
    ):
        self._name = name
        self.vars_on_chr = vars_on_chr
        self.vars_present = vars_present
        self.vars_separated = vars_separated
        self.good_chr_num = good_chr_num

    def __str__(self) -> str:
        return 'search_chromosome_test_{}'.format(self._name)


TEST_CASES_POSITIVE = [
    Case(
        name='base',
        vars_on_chr=[(1, 3), (2, 10), (3, 5), (8, 9)],
        vars_present=[(1, 2), (3, 4)],
        vars_separated=[(1, 3)],
        good_chr_num=9
    ),
    Case(
        name='unique_good_chr',
        vars_on_chr=[(1, 3), (2, 8), (3, 5), (8, 8)],
        vars_present=[(1, 2), (3, 4)],
        vars_separated=[(1, 3)],
        good_chr_num=8
    ),
    Case(
        name='multiple_choice',
        vars_on_chr=[(1, 5), (3, 15), (4, 8), (7, 13), (14, 14)],
        vars_present=[(4, 1), (3, 4)],
        vars_separated=[(2, 3)],
        good_chr_num=13
    ),
    Case(
        name='no_conditions',
        vars_on_chr=[(1, 5), (3, 15), (4, 8), (7, 13), (14, 14)],
        vars_present=[],
        vars_separated=[],
        good_chr_num=14
    ),
    Case(
        name='no_structural_variations',
        vars_on_chr=[],
        vars_present=[],
        vars_separated=[],
        good_chr_num=0
    )
]

TEST_CASES_NEGATIVE = [
    Case(
        name='one_structural_variation_per_chr',
        vars_on_chr=[(1, 1), (2, 2), (3, 3), (4, 4)],
        vars_present=[(1, 2), (3, 4)],
        vars_separated=[(1, 3)],
        good_chr_num=-1
    ),
    Case(
        name='mutually_exclusive_conditions_on_good_chr',
        vars_on_chr=[(1, 1), (1, 4), (3, 7)],
        vars_present=[(1, 1)],
        vars_separated=[(1, 1)],
        good_chr_num=-1
    )
]


@pytest.mark.parametrize('case', TEST_CASES_POSITIVE, ids=str)
def test_search_chromosome_solver(case: Case) -> None:
    answer = search_chromosome(
        vars_on_chr=case.vars_on_chr,
        vars_present=case.vars_present,
        vars_separated=case.vars_separated
    )
    assert answer == case.good_chr_num


@pytest.mark.parametrize('case', TEST_CASES_NEGATIVE, ids=str)
def test_no_good_chromosome(case: Case) -> None:
    with pytest.raises(NoGoodChromosome):
        search_chromosome(
            vars_on_chr=case.vars_on_chr,
            vars_present=case.vars_present,
            vars_separated=case.vars_separated
        )
