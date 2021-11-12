import numpy as np


def random_proj_matrix(rows: int, cols: int) -> np.array:
    # Generate random projection matrix
    sqrt3 = np.sqrt(3)
    re6 = 1 / 6
    values = [sqrt3 * -1, 0, sqrt3]
    return np.random.choice(values, size=(rows, cols), p=[re6, 1 - re6 - re6, re6])


def rsvd(matrix: np.array, rank: int) -> tuple[np.array, np.array, np.array]:
    # Compute randomized SVD
    rows = matrix.shape[1]
    P = random_proj_matrix(rows, rank)
    Z = np.matmul(matrix, P)
    Q = np.linalg.qr(Z)[0]
    Y = np.matmul(Q.T, matrix)
    Uy, S, V = tsvd(Y, rank)
    return [np.matmul(Q, Uy), S, V]


def tsvd(X, rank):
    # Compute truncated SVD up to `rank` rank
    L = X.dot(X.T)
    R = X.T.dot(X)
    U, S = simul_pow_iter(L)
    V, S = simul_pow_iter(R)
    ldim = U.shape[1]
    if rank > ldim:
        rank = ldim
    return U[:, :rank], correct_nan(np.sqrt(S[:rank])), V.T[:rank, :]


def chunks(a: np.array) -> np.array:
    # (deprecated) Split huge matrices to 64x64 chunks
    m, n = a.shape
    for i in range(0, m, 64):
        vb = i + 64
        if vb > m:
            vb = m
        for j in range(0, n, 64):
            hb = j + 64
            if hb > n:
                hb = n
            yield a[i:vb, j:hb]


def toscale(chunk_size: int, rate: float):
    # Convert compression rate to its corresponding rank
    # based on chunk size
    r = int(rate * chunk_size)
    if r == 0:
        r = 1
    return r


def clamp(value, min, max):
    # Clamp value to a certain minimum and maximum value
    if value < min:
        return min
    if value > max:
        return max
    return value


def simul_pow_iter(X):
    # Power iteration algorithm to find eigenvectors
    # and eigen values of a matrix
    m, n = X.shape
    V = np.random.rand(m, n)
    V, R = np.linalg.qr(V)
    V_ = V
    err = 1
    eps = 1e-5

    i = 0
    limit = 500
    while err > eps and i < limit:
        V = X.dot(V)
        V, E = np.linalg.qr(V)
        diff = V - V_
        absdiff = diff ** 2
        err = absdiff.sum()
        V_ = V
        i += 1
    return V, np.diag(E)


def correct_nan(arr: np.array):
    # Correct nan values of singular values, if any
    nans = np.isnan(arr)
    if nans.any():
        for i in range(len(nans)):
            if nans[i]:
                if i == 0:
                    if len(nans) > 1:
                        if nans[i + 1]:
                            arr[i] = 0
                        else:
                            arr[i] = 2 * arr[i + 1]
                elif i == len(nans) - 1:
                    arr[i] = 0.75 * arr[i - 1]
                else:
                    if nans[i + 1]:
                        arr[i] = 0.75 * arr[i - 1]
                    else:
                        arr[i] = np.sqrt(arr[i - 1] * arr[i + 1])
    return arr
