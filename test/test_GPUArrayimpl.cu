#include <GPUArrayimpl.h>
#include <petscvec.h>
#include <petsc.h>
#include <petsccusp.h>
#include <cusp/array1d.h>

int main(){     

    PetscInitialize(NULL, NULL, NULL, NULL);
    Vec V;
    double* array;

    VecCreate(PETSC_COMM_WORLD, &V);
    VecSetType(V, VECSEQCUSP);
    VecSetSizes(V, 10, PETSC_DECIDE);
    VecSet(V, 4);

    // get the raw pointer from V:
    VecGetGPUArray(V, &array);
        
    // get a thrust pointer:
    thrust::device_ptr<double> dev_ptr = thrust::device_pointer_cast(array);

    // modify the memory using thrust:
    thrust::fill(dev_ptr, dev_ptr+10, (double) 2.0);

    // check that the change is reflected in V!
    VecView(V, PETSC_VIEWER_STDOUT_WORLD);

    PetscFinalize();

    return 0;
}
