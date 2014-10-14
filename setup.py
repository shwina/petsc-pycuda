import os
from os.path import join as pjoin
from setuptools import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import subprocess
import numpy

# cusp and thrust 
INCLUDE_DIRS = ['/home/atrikut/local/cusplibrary', '/home/atrikut/local/thrust/']
LIBRARY_DIRS = []
LIBRARIES    = []

# PETSc
import os
PETSC_DIR  = os.environ['PETSC_DIR']
PETSC_ARCH = os.environ.get('PETSC_ARCH', '')
from os.path import join, isdir
if PETSC_ARCH and isdir(join(PETSC_DIR, PETSC_ARCH)):
    INCLUDE_DIRS += [join(PETSC_DIR, PETSC_ARCH, 'include'),
                     join(PETSC_DIR, 'include')]
    LIBRARY_DIRS += [join(PETSC_DIR, PETSC_ARCH, 'lib')]
else:
    if PETSC_ARCH: pass # XXX should warn ...
    INCLUDE_DIRS += [join(PETSC_DIR, 'include')]
    LIBRARY_DIRS += [join(PETSC_DIR, 'lib')]
LIBRARIES += [#'petscts', 'petscsnes', 'petscksp',
              #'petscdm', 'petscmat',  'petscvec',
              'petsc']

# PETSc for Python
import petsc4py
INCLUDE_DIRS += [petsc4py.get_include()]

# CUDA
from setup_cuda import locate_cuda
CUDA = locate_cuda()
print CUDA
LIBRARY_DIRS += [CUDA['lib64']]
LIBRARIES += ['cudart']
INCLUDE_DIRS += [CUDA['include']]

# Obtain the numpy include directory:
import numpy
numpy_include = numpy.get_include() 
INCLUDE_DIRS += [numpy_include]

ext = Extension('GPUArray',
                sources = ['GPUArray.pyx', 'GPUArrayimpl.cu'],
                depends = ['GPUArrayimpl.h'],
                language = 'c++',
                include_dirs = INCLUDE_DIRS + [os.curdir],
                libraries = LIBRARIES,
                library_dirs = LIBRARY_DIRS,
                runtime_library_dirs = LIBRARY_DIRS,
                extra_compile_args = {'gcc': [],
                                      'nvcc': ['-arch=sm_21', '--ptxas-options=-v', '-c', '--compiler-options', "'-fPIC'"]}
                )
def customize_compiler_for_nvcc(self):
    """inject deep into distutils to customize how the dispatch
    to gcc/nvcc works.

    If you subclass UnixCCompiler, it's not trivial to get your subclass
    injected in, and still have the right customizations (i.e.
    distutils.sysconfig.customize_compiler) run on it. So instead of going
    the OO route, I have this. Note, it's kindof like a wierd functional
    subclassing going on."""

    # tell the compiler it can processes .cu
    self.src_extensions.append('.cu')

    # save references to the default compiler_so and _comple methods
    default_compiler_so = self.compiler_so
    super = self._compile

    # now redefine the _compile method. This gets executed for each
    # object but distutils doesn't have the ability to change compilers
    # based on source extension: we add it.
    def _compile(obj, src, ext, cc_args, extra_postargs, pp_opts):
        if os.path.splitext(src)[1] == '.cu':
            # use the cuda for .cu files
            self.set_executable('compiler_so', CUDA['nvcc'])
            # use only a subset of the extra_postargs, which are 1-1 translated
            # from the extra_compile_args in the Extension class
            postargs = extra_postargs['nvcc']
        else:
            postargs = extra_postargs['gcc']

        super(obj, src, ext, cc_args, postargs, pp_opts)
        # reset the default compiler_so, which we might have changed for cuda
        self.compiler_so = default_compiler_so

    # inject our redefined _compile method into the class
    self._compile = _compile

# run the customize_compiler:
class custom_build_ext(build_ext):
    def build_extensions(self):
        customize_compiler_for_nvcc(self.compiler)
        build_ext.build_extensions(self)

setup(name = 'GPUArray',
      ext_modules = [ext],
      cmdclass = {'build_ext': custom_build_ext},
      zip_safe = False)

