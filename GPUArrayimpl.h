#include <petscvec.h>
PetscErrorCode VecGetGPUArray(Vec vec, PetscScalar **array);
PetscErrorCode VecUpdateGPUStatus(Vec vec, PetscScalar **array);
