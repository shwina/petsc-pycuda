#include <petsccusp.h>
#include <petscvec.h>
#include <petsc.h>
#include <petsc-private/vecimpl.h>

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
    cusp::array1d<PetscScalar, cusp::device_memory> *cusparray;
    VecCUSPGetArrayWrite(vec, &cusparray);
    *array = thrust::raw_pointer_cast(cusparray->data());
    VecCUSPRestoreArrayWrite(vec, &cusparray);
    PetscFunctionReturn(0);
}

PetscErrorCode
VecUpdateGPUStatus(Vec vec)
{
    vec->valid_GPU_array = PETSC_CUSP_GPU;
    PetscFunctionReturn(0);
}
