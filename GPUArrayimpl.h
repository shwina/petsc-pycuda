#include <petscvec.h>
PetscErrorCode VecGetGPUArray(Vec vec, PetscScalar **array);
PetscErrorCode VecRestoreGPUArray(Vec vec, PetscScalar **array);
