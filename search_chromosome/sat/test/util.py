from collections import defaultdict
import os


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
            adj_list[int(x)] = [int(v) for v in y]
    return adj_list


def abspath(filename, file):
    """
    Use instead of os.path.abspath() in test
    cases to call pytest from terminal.

    :param filename: name of the file;
    :param file: pass __file__ here.
    :return: -
    """
    return os.path.join(os.path.dirname(os.path.realpath(file)), filename)
