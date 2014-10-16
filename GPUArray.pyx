from petsc4py.PETSc cimport Vec,  PetscVec
from petsc4py.PETSc import Error
import pycuda.gpuarray as gpuarray
from pycuda import autoinit
import numpy as np

cdef extern from "GPUArrayimpl.h":
    int VecGetGPUArray(PetscVec vec, double** array)
    int VecUpdateGPUStatus(PetscVec vec)

cdef extern from "stdint.h":
    ctypedef unsigned long long uint64_t

def getGPUArray(Vec V):
    cdef double *array
    VecGetGPUArray(V.vec, &array)
    G = gpuarray.GPUArray(V.getSize(), dtype=np.float64, allocator=None, gpudata=int(<uint64_t>array))
    return G

def updateVecStatus(Vec V):
    VecUpdateGPUStatus(V.vec)
