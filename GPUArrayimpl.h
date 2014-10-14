#include <petscvec.h>
#include <petsc.h>
#include <GPUArrayimpl.h>

PetscErrorCode VecGetGPUArray(Vec vec, PetscScalar **array)
