#include <petscvec.h>
#include <petsc.h>

PetscErrorCode VecGetGPUArray(Vec vec, PetscScalar **array);
PetscErrorCode VecUpdateGPUStatus(Vec vec);
