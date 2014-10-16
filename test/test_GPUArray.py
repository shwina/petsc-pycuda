import sys
sys.path.append('..')

from numpy.testing import *
from petsc4py import PETSc as petsc
import GPUArray

class TestGPUArray:

    # In all the tests that
    # follow, `vec` is a PETSc vector
    # and `vec_gpu` is a PyCUDA gpuarray
    # they are supposed to share
    # device memory.

    def setup(self):
        V = petsc.Vec()
        V.create()
        V.setType('cusp')
        V.setSizes(5)
        V.set(2.0)
        self.vec = V

    def test_get(self):
        vec_gpu = GPUArray.getGPUArray(self.vec)
        assert_equal(self.vec.array, vec_gpu.get())

    def test_petsc_to_pycuda(self):
        vec_gpu = GPUArray.getGPUArray(self.vec)
        self.vec.set(3.14)
        assert_allclose(vec_gpu.get(), 3.14)

    def test_pycuda_to_petsc(self):
        vec_gpu = GPUArray.getGPUArray(self.vec)
        vec_gpu.fill(3.14)
        assert_allclose(self.vec.array, 3.14)

    def test_pycuda_to_petsc_reuse(self):
        vec_gpu = GPUArray.getGPUArray(self.vec)
        vec_gpu.fill(3.14)
        assert_allclose(self.vec.array, 3.14)

        # this is where we'll fail:
        vec_gpu.fill(6.28)
        assert_allclose(self.vec.array, 6.28)

    def test_pycuda_to_petsc_remake(self):
        vec_gpu = GPUArray.getGPUArray(self.vec)
        vec_gpu.fill(3.14)
        assert_allclose(self.vec.array, 3.14)
        
        # but this will work:
        del vec_gpu
        vec_gpu = GPUArray.getGPUArray(self.vec)
        vec_gpu.fill(6.28)
        assert_allclose(self.vec.array, 6.28)

    def teardown(self):
        self.vec.destroy()
