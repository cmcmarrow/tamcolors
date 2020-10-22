//python library
#define PY_SSIZE_T_CLEAN
#include <Python.h>

//tamcolors library
#include "uni_tam.h"


/*
C++ API to Unix console
can get dimension of console
get key input in the background
*/


static PyObject* _get_dimensions(PyObject *self, PyObject *args) {
    /*
	info: will return Dimensions info width and height
	return: Dimensions
	*/
	if (!PyArg_ParseTuple(args, "")) {
		return NULL;
	}
	Dimensions dimensions = get_dimensions();
	return Py_BuildValue("ii", dimensions.width, dimensions.height);
}

static PyObject* _enable_get_key(PyObject *self, PyObject *args) {
    /*
	info: will enable terminal for kbhit and get_key
	turns off echo and other settings
	*/
	if (!PyArg_ParseTuple(args, "")) {
		return NULL;
	}
	enable_get_key();
	Py_RETURN_NONE;
}

static PyObject* _disable_get_key(PyObject *self, PyObject *args) {
    /*
	info: will reset terminal
	turns on echo and other settings
	*/
	if (!PyArg_ParseTuple(args, "")) {
		return NULL;
	}
	disable_get_key();
	Py_RETURN_NONE;
}

static PyObject* _get_key(PyObject *self, PyObject *args) {
    /*
	return: int
	-1: no key data to give
	Not -1: value of key data
	*/
	if (!PyArg_ParseTuple(args, "")) {
		return NULL;
	}
	return Py_BuildValue("i", get_key());
}

static PyMethodDef _uni_tam_methods[] = {
	{
		"_get_dimensions", _get_dimensions, METH_VARARGS,
		"_get_dimensions"
	},
	{
		"_enable_get_key", _enable_get_key, METH_VARARGS,
		"_enable_get_key"
	},
	{
		"_disable_get_key", _disable_get_key, METH_VARARGS,
		"_disable_get_key"
	},
	{
		"_get_key", _get_key, METH_VARARGS,
		"_get_key"
	},
{ NULL, NULL, 0, NULL }
};

static struct PyModuleDef _uni_tam_definition = {
	PyModuleDef_HEAD_INIT,
	"_uin_tam",
	"Can work with Unix terminal.",
	-1,
	_uni_tam_methods
};

PyMODINIT_FUNC PyInit__uni_tam(void) {
    PyObject* py_module = PyModule_Create(&_uni_tam_definition);

	if (py_module == NULL) {
		return NULL;
	}

	return py_module;
}
