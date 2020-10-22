#ifndef __WIN_TAM__H_
#define __WIN_TAM__H_
#include <exception>

class ConsoleException : public std::exception {
	private:
		virtual const char* what() const throw();
};


class Dimensions {
	private:
		short width;
		short height;
	public:
		Dimensions(short, short);
		short get_width();
		short get_height();
};

void get_console_info(HANDLE&, CONSOLE_SCREEN_BUFFER_INFOEX&);
bool has_vaild_win_console();
void init_default_color();
int get_default_color();
void show_console_cursor(bool);
Dimensions get_dimensions();
Dimensions get_buffer_dimensions();
void set_buffer_dimensions(Dimensions);
void clear(bool);
void set_cursor_info(int, int, int);
void set_console_color(int);
void set_rgb_color(int, COLORREF);
COLORREF get_rgb_color(int);
int get_key();
#endif
