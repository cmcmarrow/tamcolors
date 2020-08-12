//built in libraries
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

CONSOLE_SCREEN_BUFFER_INFO csbi;
int defaultColor = 0;

typedef struct Dimension{
	short width;
	short height;
} Dimension;

void show_console_cursor(bool showFlag){
	/*
	info: will hide or reveal the cursor
	parameter: bool: showFlag
	True: cursor will show
	False: cursor will not show
	return: void
	*/
    HANDLE out = GetStdHandle(STD_OUTPUT_HANDLE);

	CONSOLE_CURSOR_INFO cursorInfo;

	GetConsoleCursorInfo(out, &cursorInfo);
	cursorInfo.bVisible = showFlag;
	SetConsoleCursorInfo(out, &cursorInfo);
}

int init_default_color() {
	/*
	info: will save current console color
	return: int
	0: init default color failed
	1: init default color success
	*/
	if (!GetConsoleScreenBufferInfo(GetStdHandle(STD_OUTPUT_HANDLE), &csbi)) {
		return 0;
	}
	defaultColor = csbi.wAttributes;
	return 1;
}

int get_default_color() {
	/*
	info: will return console color
	return: int: console color
	*/
	return defaultColor;
}

Dimension get_dimension() {
	/*
	info: will return Dimension info width and height
	return: Dimension
	*/
	if (!GetConsoleScreenBufferInfo(GetStdHandle(STD_OUTPUT_HANDLE), &csbi)) {
		abort();
	}

	Dimension dimension;
	dimension.width = csbi.srWindow.Right - csbi.srWindow.Left + 1;
	dimension.height = csbi.srWindow.Bottom - csbi.srWindow.Top;
	if (dimension.width < 0){
	    dimension.width = 0;
	}
	if (dimension.height < 0){
	    dimension.height = 0;
	}
	return dimension;
}

void clear(){
	/*
	info: will clear the screen and reset console cursor position, color and show cursor
	return: void
	*/
	HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
	if (!GetConsoleScreenBufferInfo(hOut, &csbi)) {
		abort();
	}

	Dimension dimension = get_dimension();
	COORD const size = {dimension.width, dimension.height + 1};
	SetConsoleScreenBufferSize(hOut, size);

	COORD topLeft = {0, 0};
	DWORD length = csbi.dwSize.X * csbi.dwSize.Y;
	DWORD written;

	//clear the console
	FillConsoleOutputCharacter(hOut, TEXT(' '), length, topLeft, &written);
	FillConsoleOutputAttribute(hOut, csbi.wAttributes, length, topLeft, &written);

    //set the cursor position
	SetConsoleCursorPosition(hOut, topLeft);
}

void set_cursor_info(int x, int y, int color) {
	/*
	parameter: int: x: console x position
	parameter: int: y: console y position
	parameter: int: color: console color
	return: void
	*/
	static const HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
	std::cout.flush();

	//set the cursor position
	COORD coord = { (SHORT)x, (SHORT)y };
	SetConsoleCursorPosition(hOut, coord);

	//set the console color
	SetConsoleTextAttribute(hOut, color);
}

void set_console_color(int color) {
	/*
	parameter: int: color: console color
	return: void
	*/
	static const HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
	std::cout.flush();

	//set the console color
	SetConsoleTextAttribute(hOut, color);
}

int get_key() {
	/*
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

void set_rgb_color(int spot, COLORREF color) {
	CONSOLE_SCREEN_BUFFER_INFOEX info;
	info.cbSize = sizeof(info);
	HANDLE out = GetStdHandle(STD_OUTPUT_HANDLE);
	GetConsoleScreenBufferInfoEx(out, &info);
	info.srWindow.Right += 1;
	info.srWindow.Bottom += 1;
	info.ColorTable[spot] = color;
	SetConsoleScreenBufferInfoEx(out, &info);
}

COLORREF get_rgb_color(int spot) {
	CONSOLE_SCREEN_BUFFER_INFOEX info;
	info.cbSize = sizeof(info);
	HANDLE out = GetStdHandle(STD_OUTPUT_HANDLE);
	GetConsoleScreenBufferInfoEx(out, &info);
	return info.ColorTable[spot];
}
