"""
Created on Sept 8, 2015
@author: dashesy
Purpose: CPP wrapper
"""

from libcpp.string cimport string
cimport cpython.ref as cpy_ref

cdef extern from "Python.h":
	# noinspection PyPep8Naming
    void PyEval_InitThreads()

cdef extern from "modules/avf.h":

    # noinspection PyPep8Naming
    cdef cppclass CppAVFCam:
        CppAVFCam()
        CppAVFCam(bint sink_file, bint sink_callback, cpy_ref.PyObject *obj) except +
        void record(string path, unsigned int duration)
        void stop_recording()
