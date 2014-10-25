import os
from os.path import join as pjoin
from setuptools import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import subprocess
import numpy

import os

THRUST_DIR = os.environ['THRUST_DIR']
CUSP_DIR = os.environ['CUSP_DIR']

# cusp and thrust 
INCLUDE_DIRS = [THRUST_DIR, CUSP_DIR]
LIBRARY_DIRS = []
LIBRARIES    = []

# PETSc
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

LIBRARIES += ['GPUArrayimpl']
LIBRARY_DIRS += [os.curdir]

ext = Extension('GPUArray',
                sources = ['GPUArray.pyx'],
                language = 'c++',
                include_dirs = INCLUDE_DIRS + [os.curdir],
                libraries = LIBRARIES,
                library_dirs = LIBRARY_DIRS,
                runtime_library_dirs = LIBRARY_DIRS,
                )

setup(name = 'GPUArray',
      ext_modules = [ext],
      cmdclass = {'build_ext': build_ext},
      zip_safe = False)
