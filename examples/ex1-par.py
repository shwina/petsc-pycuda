import sys
sys.path.append('..')

from petsc4py import PETSc as petsc
from pycuda import autoinit
import pycuda.gpuarray as gpuarray
import pycuda.driver as cuda
from pycuda.compiler import SourceModule

import GPUArray

da = petsc.DA().create([16,1], stencil_width=1, comm=petsc.COMM_WORLD, stencil_type='star')
da.setVecType('cusp')

V_local = da.createLocalVec()
V_global = da.createGlobalVec()

V_global.set(1.0)

# Get a handle to the global vec:
varray = GPUArray.getGPUArray(V_global)

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
func(varray, block=(8,1,1))

GPUArray.updateVecStatus(V_global)

# Update the 'ghost' element:
da.globalToLocal(V_global, V_local)

# Check that all values (including ghost) are
# correctly set:
V_local.view()

V_global.destroy()
V_local.destroy()
da.destroy()
