from search_chromosome.sat.sat_solver import Input, solve_2_sat
from typing import List, Tuple


def search_chromosome(
        vars_on_chr: List[Tuple[int, int]],
        vars_present: List[Tuple[int, int]],
        vars_separated: List[Tuple[int, int]]
) -> int:
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
        num_of_chr = r if r > num_of_chr else num_of_chr
        f.parse_and_add_clause(str(l) + ' !x' + str(var_num+1))
        f.parse_and_add_clause('!' + str(r+1) + ' !x' + str(var_num+1))

    # M clauses to detect a good chromosome
    for chromosome in range(1, num_of_chr + 1):
        f.parse_and_add_clause(str(chromosome) + ' !' + str(chromosome + 1))

    var_values = solve_2_sat(f)
    good_num = 0
    for var in var_values.keys():
        if not var.startswith('x') and var_values[var]:
            good_num = int(var) if int(var) > good_num else good_num
    return good_num


if __name__ == "__main__":
    print(search_chromosome([(1, 3), (2, 10), (3, 5), (8, 9)],
        [(1, 2), (3, 4)],
        [(1, 3)]))
