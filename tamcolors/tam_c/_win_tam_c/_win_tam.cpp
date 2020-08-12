//built in library
#include <Windows.h>

//python library
#include <Python.h>

//tamcolors library
#include "win_tam.h"


/*
Python 3 API to windows console
can show and hide the cursor
can clear the console
can print text to console with color and position
*/

static PyObject* _show_console_cursor(PyObject *self, PyObject *args) {
	/*
	info: will hide or reveal the cursor
	parameter: bool: showFlag
	True: cursor will show
	False: cursor will not show
	return: None
	*/
	int flag;
	if (!PyArg_ParseTuple(args, "p", &flag)) {
		return NULL;
	}
	show_console_cursor(flag);
	Py_RETURN_NONE;
}

static PyObject* _init_default_color(PyObject *self, PyObject *args) {
	/*
	info: will save current console color
	return: int
	0: init default color failed
	1: init default color success
	*/
	if (!PyArg_ParseTuple(args, "")) {
		return NULL;
	}
	return Py_BuildValue("i", init_default_color());
}

static PyObject* _get_default_color(PyObject *self, PyObject *args) {
	/*
	info: will return console color
	return: int: console color
	*/
	if (!PyArg_ParseTuple(args, "")) {
		return NULL;
	}
	return Py_BuildValue("i", get_default_color());
}

static PyObject* _get_dimension(PyObject *self, PyObject *args) {
	/*
	info: will return Dimension info width and height
	return: (int, int)
	*/
	if (!PyArg_ParseTuple(args, "")) {
		return NULL;
	}

	Dimension dimension = get_dimension();
	return Py_BuildValue("(ii)", dimension.width, dimension.height);
}

static PyObject* _clear(PyObject *self, PyObject *args) {
	/*
	info: will clear the screen and reset console cursor position, color and show cursor
	return: None
	*/
	if (!PyArg_ParseTuple(args, "")) {
		return NULL;
	}

	clear();
	Py_RETURN_NONE;
}

static PyObject* _set_cursor_info(PyObject *self, PyObject *args) {
	/*
	parameter: int: x: console x position
	parameter: int: y: console y position
	parameter: int: color: console color
	return: None
	*/
	int x, y, color;
	if (!PyArg_ParseTuple(args, "iii", &x, &y, &color)) {
		return NULL;
	}

	set_cursor_info(x, y, color);
	Py_RETURN_NONE;
}

static PyObject* _set_console_color(PyObject *self, PyObject *args) {
	/*
	parameter: int: color: console color
	return: None
	*/
	int color;
	if (!PyArg_ParseTuple(args, "i", &color)) {
		return NULL;
	}

	set_console_color(color);
	Py_RETURN_NONE;
}

static PyObject* _get_key(PyObject *self, PyObject *args) {
	/*
	return: int
	0: no key data to give
	Not 0: value of key data
	*/
	if (!PyArg_ParseTuple(args, "")) {
		return NULL;
	}

	return Py_BuildValue("i", get_key());
}

static PyObject* _set_rgb_color(PyObject *self, PyObject *args) {
	/*
	*/
	int spot, r, g, b;
	if (!PyArg_ParseTuple(args, "iiii", &spot, &r, &g, &b)) {
		return NULL;
	}
	set_rgb_color(spot, RGB(r, g, b));
	Py_RETURN_NONE;
}

static PyObject* _get_rgb_color(PyObject *self, PyObject *args) {
	/*
	*/
	int spot, r, g, b;
	if (!PyArg_ParseTuple(args, "i", &spot)) {
		return NULL;
	}
	COLORREF color = get_rgb_color(spot);
	r = GetRValue(color);
	g = GetGValue(color);
	b = GetBValue(color);
	return Py_BuildValue("(iii)", r, g, b);
}

static PyMethodDef _win_tam_methods[] = {
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
		"_get_dimension", _get_dimension, METH_VARARGS,
		"_get_dimension"
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
	"Can work with Windows terminal.",
	-1,
	_win_tam_methods
};

PyMODINIT_FUNC PyInit__win_tam(void) {
	Py_Initialize();
	return PyModule_Create(&_win_tam_definition);
}
