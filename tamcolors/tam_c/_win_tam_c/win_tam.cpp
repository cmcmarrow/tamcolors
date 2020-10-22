//built in libraries
#include <exception>
#include <algorithm>
#include <conio.h>
#include <iostream>
#include <windows.h>
#include <wingdi.h>


/*
C++ API to windows console
can show and hide the cursor
can clear the console
can print text to console with color and position
*/


int DEFAULT_COLOR = 0;


class ConsoleException : public std::exception {
	private:
		virtual const char* what() const throw() {
			return "Failed to get console screen buffer!";
		}
} console_exception;


class Dimensions {
	private:
		short width;
		short height;
	public:
		Dimensions(short width, short height) {
			this->width = max(width, 0);
			this->height = max(height, 0);
		}
		short get_width() {
			return this->width;
		}
		short get_height() {
			return this->height;
		}
};


void get_console_info(HANDLE &handle, CONSOLE_SCREEN_BUFFER_INFOEX &console_info) {
	/*
	info: will populate console_info with data drom handle
	parameter: HANDLE: handle
	parameter: CONSOLE_SCREEN_BUFFER_INFOEX: console_info
	return: void
	throw: ConsoleException
	*/
	console_info.cbSize = sizeof(console_info);
	if (!GetConsoleScreenBufferInfoEx(handle, &console_info)) {
		throw console_exception;
	}
}

bool has_vaild_win_console() {
	/*
	info: will check if applation has a vaild win console
	retrun: bool
	*/
	try {
		HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE);
		CONSOLE_SCREEN_BUFFER_INFOEX console_info;
		get_console_info(handle, console_info);
	} catch (ConsoleException) {
		return false;
	}
	return true;
}

void init_default_color() {
	/*
	info: will save current console color
	return: void
	*/
	HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE);
	CONSOLE_SCREEN_BUFFER_INFOEX console_info;
	get_console_info(handle, console_info);
	DEFAULT_COLOR = console_info.wAttributes;
}

int get_default_color() {
	/*
	info: will return console color
	return: int: console default color
	*/
	return DEFAULT_COLOR;
}

void show_console_cursor(bool showFlag){
	/*
	info: will hide or reveal the cursor
	parameter: bool: showFlag: if true the cursor will be displayed
	return: void
	*/
    HANDLE out = GetStdHandle(STD_OUTPUT_HANDLE);
	CONSOLE_CURSOR_INFO cursorInfo;
	GetConsoleCursorInfo(out, &cursorInfo);

	cursorInfo.bVisible = showFlag;
	SetConsoleCursorInfo(out, &cursorInfo);
}

Dimensions get_dimensions() {
	/*
	info: will return Dimensions console window
	return: Dimensions
	*/
	HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE);
	CONSOLE_SCREEN_BUFFER_INFOEX console_info;
	get_console_info(handle, console_info);

	Dimensions dimensions(console_info.srWindow.Right - console_info.srWindow.Left + 1, console_info.srWindow.Bottom - console_info.srWindow.Top);
	return dimensions;
}

Dimensions get_buffer_dimensions(){
	/*
	info: will return Dimensions info of the console buffer
	return: Dimensions
	*/
	HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE);
	CONSOLE_SCREEN_BUFFER_INFOEX console_info;
	get_console_info(handle, console_info);

	Dimensions dimensions(console_info.dwSize.X, console_info.dwSize.Y);
	return dimensions;
}

void set_buffer_dimensions(Dimensions dimensions) {
	/*
	info: will set the console buffer dimensions
	parameter: Dimensions
	return: void
	*/
	HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE);
	COORD const buffer_dimension = {dimensions.get_width(), dimensions.get_height()};
	SetConsoleScreenBufferSize(handle, buffer_dimension);
}

void clear(bool reset_buffer){
	/*
	info: will clear the screen and reset console cursor position, color and show cursor
	parameter: bool: reset_buffer: will shrink console buffer to windows size
	return: void
	*/
	HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE);
	CONSOLE_SCREEN_BUFFER_INFOEX console_info;
	get_console_info(handle, console_info);

	// shrink buffer to be the same size as windows
	// this will remove the scroll bar
	if (reset_buffer) {
		Dimensions dimensions = get_dimensions();
		COORD const buffer_dimensions = { dimensions.get_width(), dimensions.get_height() + 1 };
		SetConsoleScreenBufferSize(handle, buffer_dimensions);
	}

	COORD top_left = {0, 0};
	DWORD length = console_info.dwSize.X * console_info.dwSize.Y;
	DWORD written;

	// clear the console
	FillConsoleOutputCharacter(handle, TEXT(' '), length, top_left, &written);
	FillConsoleOutputAttribute(handle, console_info.wAttributes, length, top_left, &written);

    // set the cursor position
	SetConsoleCursorPosition(handle, top_left);
}

void set_cursor_info(int x, int y, int color) {
	/*
	info: will set the curosor location and color
	parameter: int: x: console x position
	parameter: int: y: console y position
	parameter: int: color: console color
	return: void
	*/
	static const HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE);

	//set the cursor position
	COORD coord = { static_cast<SHORT>(x), static_cast<SHORT>(y)};
	SetConsoleCursorPosition(handle, coord);

	//set the console color
	SetConsoleTextAttribute(handle, color);
}

void set_console_color(int color) {
	/*
	info: will set the console color
	parameter: int: color: console color
	return: void
	*/
	static const HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE);

	//set the console color
	SetConsoleTextAttribute(handle, color);
}

void set_rgb_color(int spot, COLORREF color) {
	/*
	info: will set the console color
	parameter: int: spot: color
	parameter: COLORREF: the new color for the spot
	return: void
	*/
	HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE);
	CONSOLE_SCREEN_BUFFER_INFOEX console_info;
	get_console_info(handle, console_info);
	GetConsoleScreenBufferInfoEx(handle, &console_info);
	console_info.srWindow.Right += 1;
	console_info.srWindow.Bottom += 1;
	console_info.ColorTable[spot] = color;
	SetConsoleScreenBufferInfoEx(handle, &console_info);
}

COLORREF get_rgb_color(int spot) {
	/*
	info: will set the console color
	parameter: int: spot: color
	return: COLORREF
	*/
	HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE);
	CONSOLE_SCREEN_BUFFER_INFOEX console_info;
	get_console_info(handle, console_info);
	GetConsoleScreenBufferInfoEx(handle, &console_info);
	return console_info.ColorTable[spot];
}

int get_key() {
	/*
	info: will get part of a key input
	return: int
	-1: no key data to give
	Not -1: value of key data
	*/
	//check if key data present
	if (kbhit()) {
		//get key data
		return getch();
	}
	//no key data
	return -1;
}

