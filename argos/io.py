import numpy as np
from scipy.sparse import lil_matrix
import scipy
import pickle

def save(d, filename):
    f = open(filename, "wb")
    pickle.dump( d, f, pickle.HIGHEST_PROTOCOL)
    f.close()
    '''
    f = open(filename, "w")
    f.write(str(d))
    f.close()
    '''


def load(filename):
    '''
    f = open(filename, "r")
    content = f.read()
    d = eval(content)
    '''
    f = open(filename, "rb")
    d = pickle.load( f)
    f.close()
    return d


def save_distance_matrix(x, filename):
    x = scipy.sparse.csr_matrix(x)
    scipy.sparse.save_npz(filename, x)


def load_distance_matrix(filename):
    d = scipy.sparse.load_npz(filename)
    d = lil_matrix(d)
    return d
