from search_chromosome.sat.sat_solver import Input, solve_2_sat, NoSolution
from typing import List, Tuple


class SearchChromosomeException(Exception):
    """
    Base class for other exceptions.
    """
    pass


class NoGoodChromosome(SearchChromosomeException):
    """
    Raised when a desired good chromosome doesn't exist.
    """
    def __init__(self, message="A good chromosome doesnt exist!"):
        self.message = message
        super().__init__(self.message)


def search_chromosome(
        vars_on_chr: List[Tuple[int, int]],
        vars_present: List[Tuple[int, int]],
        vars_separated: List[Tuple[int, int]]
) -> int:
    """

    :param vars_on_chr:
    :param vars_present:
    :param vars_separated:
    :return:
    """
    # construct a formula
    f = Input()
    # K clauses - at least one of each pair must be in the chromosome
    for condition in vars_present:
        x, y = condition
        f.parse_and_add_clause('x' + str(x) + ' ' + 'x' + str(y))

    # L clauses - which structural variations mustn't be together
    for condition in vars_separated:
        x, y = condition
        f.parse_and_add_clause('!x' + str(x) + ' !x' + str(y))

    # 2N clauses to state structural variations found on each chromosome
    num_of_chr = 0
    for var_num in range(len(vars_on_chr)):
        l, r = vars_on_chr[var_num]
        num_of_chr = max(r, num_of_chr)
        f.parse_and_add_clause(str(l) + ' !x' + str(var_num+1))
        f.parse_and_add_clause('!' + str(r+1) + ' !x' + str(var_num+1))

    # M clauses to detect a good chromosome
    for chromosome in range(1, num_of_chr + 1):
        f.parse_and_add_clause(str(chromosome) + ' !' + str(chromosome + 1))

    try:
        var_values = solve_2_sat(f)
    except NoSolution:
        raise NoGoodChromosome

    good_chr_num = 0
    for var in var_values.keys():
        if not var.startswith('x') and var_values[var]:
            good_chr_num = max(int(var), good_chr_num)

    return good_chr_num
