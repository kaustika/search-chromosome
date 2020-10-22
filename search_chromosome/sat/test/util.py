from collections import defaultdict


def read_graph_from_file(file_name):
    """
    Reads graph represented as an adjacency list from file.

    :param file_name: file to read from (path to it);
    :return: adj. list representation - dict{node: list of its adj. nodes}.
    """
    adj_list = defaultdict(list)
    with open(file_name) as file:
        for line in file:
            if line.startswith("#"):
                continue
            x, *y = line.split()
            adj_list[x] = y
    return adj_list
