from petsc4py.PETSc cimport Vec,  PetscVec
from petsc4py.PETSc import Error

cdef extern from "GPUArrayimpl.h":
    int VecGetGPUArray(PetscVec vec, double** array)

def getGPUArray(Vec V):
    print 'HI'
