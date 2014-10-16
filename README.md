petsc-pycuda
============

An attempt to bridge `petsc4py` and `PyCUDA`.

At the time of writing,
there is no way to access
the underlying device memory 
of a `cusp` vector
from `petsc4py`. 
This project attempts to add this  functionality,
making the memory accessible as a `PyCUDA gpuArray`.

The tests in `test_GPUArray.py`
should give you a fairly good idea
of how things work.

Thanks
======

This project is based on the following works;
thanks to the respective authors 
for the amazing software they develop:

* `petsc4py` : https://bitbucket.org/petsc/petsc4py

* `PyCUDA` : https://github.com/inducer/pycuda

* `Cython` : http://cython.org/

* `setup.py` is based on that from the project `npcuda-example: https://github.com/rmcgibbo/npcuda-example
