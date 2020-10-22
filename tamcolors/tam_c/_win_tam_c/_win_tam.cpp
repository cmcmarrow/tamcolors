//python library
#define PY_SSIZE_T_CLEAN
#include <Python.h>


//built in library
#include <Windows.h>
#include <exception>


//tamcolors library
#include "win_tam.h"


/*
Python 3 API to windows console
can show and hide the cursor
can clear the console
can print text to console with color and position
*/


static PyObject* _WinTamError;


static PyObject* _has_vaild_win_console(PyObject* self, PyObject* args) {
	/*
	info: will check if applation has a vaild win console
	retrun: bool
	*/
	if (!PyArg_ParseTuple(args, "")) {
		return NULL;
	}
	try {
		if (has_vaild_win_console()) {
			Py_INCREF(Py_True);
			return Py_BuildValue("O", Py_True);
		}
		else {
			Py_INCREF(Py_False);
			return Py_BuildValue("O", Py_False);
		}
	} catch (std::exception& e){
		PyErr_SetString(_WinTamError, e.what());
		return NULL;
	}
	Py_RETURN_NONE;
}


static PyObject* _init_default_color(PyObject* self, PyObject* args) {
	/*
	info: will save current console color
	return: void
	*/
	if (!PyArg_ParseTuple(args, "")) {
		return NULL;
	}

	try {
		init_default_color();
	}
	catch (std::exception& e) {
		PyErr_SetString(_WinTamError, e.what());
		return NULL;
	}
	Py_RETURN_NONE;
}


static PyObject* _get_default_color(PyObject* self, PyObject* args) {
	/*
	info: will return console color
	return: int: console default color
	*/
	if (!PyArg_ParseTuple(args, "")) {
		return NULL;
	}

	try {
		int default_color = get_default_color();
		return Py_BuildValue("i", default_color);
	}
	catch (std::exception& e) {
		PyErr_SetString(_WinTamError, e.what());
		return NULL;
	}
}


static PyObject* _show_console_cursor(PyObject *self, PyObject *args) {
	/*
	info: will hide or reveal the cursor
	parameter: bool: showFlag: if true the cursor will be displayed
	return: void
	*/
	int flag;
	if (!PyArg_ParseTuple(args, "p", &flag)) {
		return NULL;
	}
	try {
		show_console_cursor(flag);
	} catch (std::exception& e) {
		PyErr_SetString(_WinTamError, e.what());
		return NULL;
	}
	Py_RETURN_NONE;
}


static PyObject* _get_dimensions(PyObject *self, PyObject *args) {
	/*
	info: will return Dimensions console window
	return: Dimensions
	*/
	if (!PyArg_ParseTuple(args, "")) {
		return NULL;
	}

	try {
		Dimensions dimensions = get_dimensions();
		return Py_BuildValue("ii", dimensions.get_width(), dimensions.get_height());
	} catch (std::exception& e) {
		PyErr_SetString(_WinTamError, e.what());
		return NULL;
	}
}


static PyObject* _get_buffer_dimensions(PyObject* self, PyObject* args) {
	/*
	info: will return Dimensions info of the console buffer
	return: Dimensions
	*/
	if (!PyArg_ParseTuple(args, "")) {
		return NULL;
	}
	try {
		Dimensions dimensions = get_buffer_dimensions();
		return Py_BuildValue("ii", dimensions.get_width(), dimensions.get_height());
	} catch (std::exception& e) {
		PyErr_SetString(_WinTamError, e.what());
		return NULL;
	}
}


static PyObject* _set_buffer_dimensions(PyObject* self, PyObject* args) {
	/*
	info: will set the console buffer dimensions
	parameter: Dimensions
	return: void
	*/
	int width, height;
	if (!PyArg_ParseTuple(args, "ii", &width, &height)) {
		return NULL;
	}

	try {
		Dimensions dimensions(width, height);
		set_buffer_dimensions(dimensions);
	} catch (std::exception& e) {
		PyErr_SetString(_WinTamError, e.what());
		return NULL;
	}
	Py_RETURN_NONE;
}


static PyObject* _clear(PyObject *self, PyObject *args) {
	/*
	info: will clear the screen and reset console cursor position, color and show cursor
	parameter: bool: reset_buffer: will shrink console buffer to windows size
	return: void
	*/
	int reset_buffer;
	if (!PyArg_ParseTuple(args, "p", &reset_buffer)) {
		return NULL;
	}

	try { 
		clear(static_cast<bool>(reset_buffer));
	} catch (std::exception& e) {
		PyErr_SetString(_WinTamError, e.what());
		return NULL;
	}
	Py_RETURN_NONE;
}


static PyObject* _set_cursor_info(PyObject *self, PyObject *args) {
	/*
	info: will set the curosor location and color
	parameter: int: x: console x position
	parameter: int: y: console y position
	parameter: int: color: console color
	return: void
	*/
	int x, y, color;
	if (!PyArg_ParseTuple(args, "iii", &x, &y, &color)) {
		return NULL;
	}

	try {
		set_cursor_info(x, y, color);
	} catch (std::exception& e) {
		PyErr_SetString(_WinTamError, e.what());
		return NULL;
	}
	Py_RETURN_NONE;
}


static PyObject* _set_console_color(PyObject *self, PyObject *args) {
	/*
	info: will set the console color
	parameter: int: color: console color
	return: void
	*/
	int color;
	if (!PyArg_ParseTuple(args, "i", &color)) {
		return NULL;
	}

	try {
		set_console_color(color);
	} catch (std::exception& e) {
		PyErr_SetString(_WinTamError, e.what());
		return NULL;
	}
	Py_RETURN_NONE;
}


static PyObject* _set_rgb_color(PyObject *self, PyObject *args) {
	/*
	info: will set the console color
	parameter: int: spot: color
	parameter: COLORREF: the new color for the spot
	return: void
	*/
	int spot, r, g, b;
	if (!PyArg_ParseTuple(args, "iiii", &spot, &r, &g, &b)) {
		return NULL;
	}
	try {
		set_rgb_color(spot, RGB(r, g, b));
	} catch (std::exception& e) {
		PyErr_SetString(_WinTamError, e.what());
		return NULL;
	}
	Py_RETURN_NONE;
}


static PyObject* _get_rgb_color(PyObject *self, PyObject *args) {
	/*
	info: will set the console color
	parameter: int: spot: color
	return: COLORREF
	*/
	int spot, r, g, b;
	if (!PyArg_ParseTuple(args, "i", &spot)) {
		return NULL;
	}
	try { 
		COLORREF color = get_rgb_color(spot);
		r = GetRValue(color);
		g = GetGValue(color);
		b = GetBValue(color);
		return Py_BuildValue("iii", r, g, b);
	} catch (std::exception& e) {
		PyErr_SetString(_WinTamError, e.what());
		return NULL;
	}
}


static PyObject* _get_key(PyObject* self, PyObject* args) {
	/*
	info: will get part of a key input
	return: int
	-1: no key data to give
	Not -1: value of key data
	*/
	if (!PyArg_ParseTuple(args, "")) {
		return NULL;
	}
	try {
		return Py_BuildValue("i", get_key());
	}
	catch (std::exception& e) {
		PyErr_SetString(_WinTamError, e.what());
		return NULL;
	}
}


static PyMethodDef _win_tam_methods[] = {
	{
		"_has_vaild_win_console", _has_vaild_win_console, METH_VARARGS,
		"_has_vaild_win_console"
	},
	{
		"_show_console_cursor", _show_console_cursor, METH_VARARGS,
		"_show_console_cursor"
	},
	{
		"_init_default_color", _init_default_color, METH_VARARGS,
		"_init_default_color"
	},
	{
		"_get_default_color", _get_default_color, METH_VARARGS,
		"_get_default_color"
	},
	{
		"_get_dimensions", _get_dimensions, METH_VARARGS,
		"_get_dimensions"
	},
	{
		"_get_buffer_dimensions", _get_buffer_dimensions, METH_VARARGS,
		"_get_buffer_dimensions"
	},
	{
		"_set_buffer_dimensions", _set_buffer_dimensions, METH_VARARGS,
		"_set_buffer_dimensions"
	},
	{
		"_clear", _clear, METH_VARARGS,
		"_clear"
	},
	{
		"_set_cursor_info", _set_cursor_info, METH_VARARGS,
		"_set_cursor_info"
	},
	{
		"_set_console_color", _set_console_color, METH_VARARGS,
		"_set_console_color"
	},
	{
		"_get_key", _get_key, METH_VARARGS,
		"_get_key"
	},
	{
		"_set_rgb_color", _set_rgb_color, METH_VARARGS,
		"_set_rgb_color"
	},
	{
		"_get_rgb_color", _get_rgb_color, METH_VARARGS,
		"_get_rgb_color"
	},
{ NULL, NULL, 0, NULL }
};

static struct PyModuleDef _win_tam_definition = {
	PyModuleDef_HEAD_INIT,
	"_win_tam",
	"Works with Windows console API",
	-1,
	_win_tam_methods
};

PyMODINIT_FUNC PyInit__win_tam(void) {
	PyObject* py_module = PyModule_Create(&_win_tam_definition);

	if (py_module == NULL) {
		return NULL;
	}

	_WinTamError = PyErr_NewException("_win_tam._WinTamError", NULL, NULL);
	Py_XINCREF(_WinTamError);
	if (PyModule_AddObject(py_module, "_WinTamError", _WinTamError) < 0) {
		Py_XDECREF(_WinTamError);
		Py_CLEAR(_WinTamError);
		Py_DECREF(py_module);
		return NULL;
	}

	return py_module;
}
