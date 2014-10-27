import sys
sys.path.append('..')

from petsc4py import PETSc as petsc
from pycuda import autoinit
import pycuda.gpuarray as gpuarray
import pycuda.driver as cuda
from pycuda.compiler import SourceModule

import GPUArray

# Crete a PETSc Vec and fill with ones:
V = petsc.Vec()
V.create()
V.setType('cusp')
V.setSizes(10)
V.set(1.0)

# Get a handle to the vector:
varray = GPUArray.getGPUArray(V)

# CUDA kernel:
mod = SourceModule("""
  __global__ void doublify(double *a)
  {
    int idx = threadIdx.x;
    a[idx] *= 2;
  }
  """)

# Apply the kernel to the GPUArray:
func = mod.get_function('doublify')
func(varray, block=(10,1,1))

# Inform the Vec that its values have been udpated:
GPUArray.restoreGPUArray(V)
print V.array
