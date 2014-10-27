include ${PETSC_DIR}/conf/variables
include ${PETSC_DIR}/conf/rules
CPPFLAGS = -I . 
MPIEXEC=
PYTHON=python

SCRIPT=run_demo
MODULE=GPUArray

.PHONY:build
build: ${MODULE}.so

.PHONY:run
run: build
	${MPIEXEC} ${PYTHON} ${SCRIPT}.py

${MODULE}.so: ${MODULE}.pyx
	CC=${CXX} F90=${FC} LDSHARED='${CLINKER} -shared' \
	${PYTHON} setup.py build_ext --inplace
	${RM} -r build ${MODULE}_wrap.c

.PHONY:clean
clean::
	${RM} ${MODULE}.c ${MODULE}*.so
	${RM} *.py[co]
	${RM} -r __pycache__
	${RM} *.cpp
	${RM} -rf build

test: test/test_GPUArrayimpl.o GPUArrayimpl.o
	-${CLINKER} ${CPPFLAGS} -o test/test test/test_GPUArrayimpl.o GPUArrayimpl.o ${PETSC_LIB}
	rm *.o
	rm test/*.o

MPIEXEC=
