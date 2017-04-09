from itertools import product
from cython import boundscheck, wraparound, cdivision
from libc.stdlib cimport malloc, free
from numpy import array, fromiter, empty, diff



@boundscheck(False)
@wraparound(False)
@cdivision(True)
cpdef int[:] align(int[:] pattern, int[:] sequence, int c_sub=1, int c_ins=1, int c_del=1, int c_trans=1):
    """
    damerau-levenshtein sequence alignment

    :return: array[int] - array of edit distances
    """
    cdef int i, j, cost, s_i, t_j, above, left, diag

    cdef int n=pattern.shape[0]+1
    cdef int m=sequence.shape[0]+1

    cdef int *matrix = <int *>malloc( n * m * sizeof(int))
    for i in range(n):matrix[i*m]=i
    for j in range(m):matrix[j]=0
    
    for i in range(1,n):
        s_i = pattern[i-1]
        for j in range(1,m):
            t_j = sequence[j-1]
            if s_i == t_j: cost = 0
            else: cost = c_sub
            above = matrix[(i-1)*m+j]
            left = matrix[i*m+j-1]
            diag = matrix[(i-1)*m+j-1]
            matrix[i*m+j] = min( above + c_ins, min(left + c_del, diag + cost))
            if i>1 and j>1 and pattern[i-2]==t_j and s_i==sequence[j-2]:
                matrix[i*m+j]=min(matrix[i*m+j],matrix[(i-2)*m+j-2]+c_trans)

    cdef int[:] res = empty(m-1,'i')
    for i in range(1,m):
        res[i-1]=matrix[(n-1)*m+i]

    free(matrix)

    return res


@boundscheck(False)
@wraparound(False)
@cdivision(True)
cpdef float score(int[:] pattern, int[:] sequence, int c_sub=1, int c_ins=1, int c_del=1, int c_trans=1):
    """
    convert alignment to score

    :return: float - pattern-score
    """
    cdef int[:] alignment=align(pattern, sequence, c_sub,  c_ins, c_del, c_trans)
    cdef int l = alignment.shape[0]
    cdef float res=0
    cdef int i
    for i in range(l):
        res+=1./(alignment[i]+1)
    return res/l


def iter_scores(sequence, n, c_sub=1, c_ins=1, c_del=1, c_trans=1, repeats=True):
    """
    return scores of length-n patterns as iterator

    :param sequence: list of int
    :param n: int - pattern length
    :param repeats: bool - allow repeats?
    :return: iterator[float] - scores of length-n patterns as iterator
    """
    sequence=array(sequence, dtype='i')
    for pattern in product(range(9), repeat=n):
        pattern=array(pattern, dtype='i')
        if repeats or not 0 in diff(pattern):
            yield score(pattern,sequence, c_sub,  c_ins, c_del, c_trans)


def array_scores(sequence, n, c_sub=1, c_ins=1, c_del=1, c_trans=1, repeats=True):
    """
    return scores of length-n patterns as array

    :param sequence: list of int
    :param n: int - pattern length
    :param repeats: bool - allow repeats?
    :return: array[float] - scores of length-n patterns as array
    """
    return fromiter(iter_scores(sequence, n, c_sub,  c_ins, c_del, c_trans, repeats), dtype='f')
