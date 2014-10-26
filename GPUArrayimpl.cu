#include <petsc-private/vecimpl.h>
#include <petscvec.h>
#include <petsccusp.h>

#include <thrust/device_ptr.h>
#include <thrust/device_vector.h>
#include <cusp/array1d.h>

#include <GPUArrayimpl.h>

PetscErrorCode
VecGetGPUArray(Vec vec, PetscScalar **array)
{
    /* Get raw device pointer
     * from the underlying CUSP
     * vector in vec
     */
    VecCUSPGetCUDAArray(vec, array);
    PetscFunctionReturn(0);
}

PetscErrorCode
VecRestoreGPUArray(Vec vec, PetscScalar **array)
{
    VecCUSPRestoreCUDAArray(vec, array);
    PetscFunctionReturn(0);
}
