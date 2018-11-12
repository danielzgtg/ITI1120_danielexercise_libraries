# Matrix utilities

from typing import List, Callable, TypeVar


T = TypeVar("T")


def generate_entrywise_matrix_transformer_with_pair_transformer(
        pair_transformer: Callable[[T, T], T]) ->\
        Callable[[List[List[T]], List[List[T]]], List[List[T]]]:
    """
    generate_entrywise_matrix_transformer_with_pair_transformer(
        pair_transformer: Callable[[T, T], T]) ->
        matrix_transformer_func: Callable[[List[List[T]], List[List[T]]], List[List[T]]]:

    Returns a parsing that takes a prompt string and uses this function's argument error string and parser.
    """
    def result(orig1: List[List[T]], orig2: List[List[T]]) -> List[List[T]]:
        """
        result(orig1: List[List[T]], orig2: List[List[T]]) -> transformed: List[List[T]],
            len(orig1) == len(orig2) == len(transformed)

        Returns a new matrix with values computed by a function taking values
        from the same position in the original matrices.
        """
        return [[pair_transformer(value1, value2) for value1, value2 in zip(row1, row2)]
                for row1, row2 in zip(orig1, orig2)]
    return result


sum_matrices = generate_entrywise_matrix_transformer_with_pair_transformer(lambda x, y: x + y)
sum_matrices.__doc__ = """
    sum_matrices(orig1: List[List[T]], orig2: List[List[T]]) -> sum: List[List[T]],
        len(orig1) == len(orig2) == len(transformed)

    Returns a new matrix with values computed by summing values
    from the same position in the original matrices.
    """


def matdim(mat: List[List]) -> (int, int):
    if not mat:
        return 0, 0
    return len(mat), len(mat[0])


def multiply_matrices(orig1: List[List[T]], orig2: List[List[T]]) -> List[List[T]]:
    """
    multiply_matrices(orig1: List[List[T]], orig2: List[List[T]]) -> product: List[List[T]],
        matdim(orig1) == matdim(orig2)[::-1]

    Returns a new matrix with values computed by a function taking values
    from the same position in the original matrices.
    """
    l1 = len(orig1)
    w1 = len(orig1[0])
    w2 = len(orig2[0])
    result = [[sum(orig1[x][a] * orig2[a][y] for a in range(w1)) for y in range(w2)] for x in range(l1)]
    # result = []
    # for x in range(l1):
    #     row = []
    #     for y in range(w2):
    #         acc = 0
    #         for a in range(w1):
    #             acc += orig1[x][a] * orig2[a][y]
    #         row.append(acc)
    #     result.append(row)
    return result


#LIBRARY
def transpose(orig: List[List[T]]) -> List[List[T]]:
    """
    transpose(orig: List[List[T]]) -> transposed: List[List[T]]

    Returns a matrix representing the original matrix but transposed
    """
    if not orig:
        return []
    l = len(orig)
    w = len(orig[0])
    return [[orig[orig_x][orig_y] for orig_x in range(l)] for orig_y in range(w)]
