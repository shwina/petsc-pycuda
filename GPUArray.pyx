from petsc4py.PETSc cimport Vec,  PetscVec
from petsc4py.PETSc import Error
from petsc4py import PETSc as petsc
import pycuda.gpuarray as gpuarray
from pycuda import autoinit

from libc.stdint cimport uintptr_t

cdef extern from "petsccusp.h":
    int VecCUSPGetCUDAArray(PetscVec vec, double** array)
    int VecCUSPRestoreCUDAArray(PetscVec vec, double** array)

def getGPUArray(Vec V):
    cdef double *array
    G = gpuarray.GPUArray(V.getLocalSize(), dtype=petsc.ScalarType, allocator=None, gpudata=V.getCUDAHandle())
    return G

def restoreGPUArray(Vec V):
    dummy_int = 0
    V.restoreCUDAHandle(dummy_int)
