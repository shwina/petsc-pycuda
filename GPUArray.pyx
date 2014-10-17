from petsc4py.PETSc cimport Vec,  PetscVec
from petsc4py.PETSc import Error
import pycuda.gpuarray as gpuarray
from pycuda import autoinit
import numpy as np

from libc.stdint cimport uintptr_t

cdef extern from "GPUArrayimpl.h":
    int VecGetGPUArray(PetscVec vec, double** array)
    int VecUpdateGPUStatus(PetscVec vec)

def getGPUArray(Vec V):
    cdef double *array
    VecGetGPUArray(V.vec, &array)
    G = gpuarray.GPUArray(V.getLocalSize(), dtype=np.float64, allocator=None, gpudata=int(<uintptr_t>array))
    return G

def updateVecStatus(Vec V):
    VecUpdateGPUStatus(V.vec)
