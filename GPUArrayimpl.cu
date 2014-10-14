#include <petsccusp.h>
#include <petscvec.h>
#include <petsc.h>

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
    PetscFunctionReturn(0);
}
