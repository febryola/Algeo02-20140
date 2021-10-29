import numpy as np


def remove_row(matrix: list[list[np.array]], row_index: int) -> list[list[np.array]]:
    newMatrix = []
    for i in range(len(matrix)):
        if i != row_index:
            newMatrix.append(matrix[i])
    return newMatrix


def remove_col(matrix: list[list[np.array]], col_index: int) -> list[list[np.array]]:
    matrix = remove_row(np.transpose(matrix), col_index)
    return np.transpose(matrix)


def minor(matrix: list[list[np.array]], row_index: int, col_index: int) -> np.array:
    submatrix = remove_row(matrix, row_index)
    submatrix = remove_col(submatrix, col_index)
    return determinant(submatrix)


def cofactor(matrix: list[list[np.array]], row_index: int, col_index: int) -> np.array:
    sign = 1 if (row_index + col_index) % 2 == 0 else -1
    minor_value = minor(matrix, row_index, col_index)
    return np.polymul(minor_value, np.array([sign]))


def determinant(matrix: list[list[np.array]]) -> np.array:
    if len(matrix) == 1:
        return matrix[0][0]
    elif len(matrix) == 2:
        [[a, b], [c, d]] = matrix
        return np.polysub(np.polymul(a, d), np.polymul(b, c))
    else:
        det = np.array([0])
        for i in range(len(matrix)):
            val = matrix[0][i]
            cof = cofactor(matrix, 0, i)
            det = np.polyadd(det, np.polymul(val, cof))
        return det


def normalize(vector: np.array) -> np.array:
    n = np.linalg.norm(vector)
    for i in range(len(vector)):
        vector[i] /= n
    return vector


def multiply(matrix1: list[list[np.array]], matrix2: list[list[np.array]]) -> list[list[np.array]]:
    rows = len(matrix1)
    cols = len(matrix2[0])
    matrix: list[list[np.array]] = []
    for i in range(rows):
        row: list[np.array] = []
        for j in range(cols):
            res = np.array([0])
            for k in range(cols):
                for l in range(rows):
                    val1 = matrix1[i][k]
                    val2 = matrix2[l][j]
                    adder = np.polymul(val1, val2)
                    res = np.polyadd(res, adder)
            row.append(res)
        matrix.append(row)
    return matrix


def subtract(matrix1: list[list[np.array]], matrix2: list[list[np.array]]) -> list[list[np.array]]:
    matrix: list[list[np.array]] = []
    rows = len(matrix1)
    cols = len(matrix1[0])
    for i in range(rows):
        row: list[np.array] = []
        for j in range(cols):
            val1 = matrix1[i][j]
            val2 = matrix2[i][j]
            row.append(np.polysub(val1, val2))
        matrix.append(row)
    return matrix


def substitute(matrix: list[list[np.array]], val: float) -> np.array:
    rows = len(matrix)
    cols = len(matrix[0])
    constant_matrix: list[list[float]] = []
    for i in range(rows):
        row: list[float] = []
        for j in range(cols):
            expr = matrix[i][j]
            row.append(np.polyval(expr, val))
        constant_matrix.append(row)
    return constant_matrix


def get_identity_matrix(dim: int) -> list[list[np.array]]:
    matrix: list[list[np.array]] = []
    for i in range(dim):
        row: list[np.array] = []
        for j in range(dim):
            if i == j:
                row.append(np.array([1, 0]))
            else:
                row.append(np.array([0]))
        matrix.append(row)
    return matrix


def get_zeros_matrix(dim: int) -> np.array:
    m: list[float] = [0 for i in range(dim)]
    return np.array(m)


def to_poly_matrix(matrix: np.array) -> list[list[np.array]]:
    m: list[list[np.array]] = []
    rows = len(matrix)
    cols = len(matrix[0])
    for i in range(rows):
        row: list[np.array] = []
        for j in range(cols):
            row.append(np.array([matrix[i][j]]))
        m.append(row)
    return m


def get_eigen_values(matrix: np.array) -> np.array:
    i = get_identity_matrix(len(matrix))
    m = to_poly_matrix(matrix)
    m = subtract(i, m)
    return np.roots(determinant(m))


def get_singular_values(matrix: np.array) -> list[float]:
    rows = len(matrix)
    cols = len(matrix[0])
    if (rows < cols):
        m = np.matmul(matrix, np.transpose(matrix))
    else:
        m = np.matmul(np.transpose(matrix), matrix)
    eigens = get_eigen_values(m)
    singulars = []
    for value in eigens:
        singulars.append(np.sqrt(value))
    return np.array(singulars)


def get_left_singular_vectors(matrix: np.array):
    m = np.matmul(matrix, np.transpose(matrix))
    idm = get_identity_matrix(len(m))
    eigens = -np.sort(-get_eigen_values(m))
    m = subtract(idm, m)
    singular_vectors = []
    for i in range(len(eigens)):
        les = substitute(m, eigens[i])
        b = np.transpose(les)[0]
        les = remove_row(les, 0)
        les = remove_col(les, 0)
        vector = np.linalg.solve(les, -b[1:])
        vector = [1, *vector]
        singular_vectors.append(normalize(vector))
    return np.transpose(singular_vectors)


def get_right_singular_vectors(matrix: np.array):
    m = np.matmul(np.transpose(matrix), matrix)
    idm = get_identity_matrix(len(m))
    eigens = -np.sort(-get_eigen_values(m))
    m = subtract(idm, m)
    singular_vectors = []
    for i in range(len(eigens)):
        les = substitute(m, eigens[i])
        b = np.transpose(les)[0]
        les = remove_row(les, 0)
        les = remove_col(les, 0)
        vector = np.linalg.solve(les, -b[1:])
        vector = [1, *vector]
        singular_vectors.append(normalize(vector))
    return np.array(singular_vectors)


def construct_singular_matrix(singulars: np.array, rows: int, cols: int) -> np.array:
    matrix = []
    for i in range(rows):
        row = []
        for j in range(cols):
            if (i == j):
                row.append(singulars[i])
            else:
                row.append(0)
        matrix.append(row)
    return matrix


def svd_decompose(matrix: np.array) -> tuple[np.array, np.array, np.array]:
    return [get_left_singular_vectors(matrix),
            get_singular_values(matrix),
            get_right_singular_vectors(matrix)]
