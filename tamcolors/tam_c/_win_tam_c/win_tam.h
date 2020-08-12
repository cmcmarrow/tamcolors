#ifndef __WIN_TAM__H_
#define __WIN_TAM__H_


typedef struct Dimension {
	short width;
	short height;
} Dimension;

void show_console_cursor(bool showFlag);
int init_default_color();
int get_default_color();
Dimension get_dimension();
void clear();
void set_cursor_info(int x, int y, int color);
void set_console_color(int color);
int get_key();
void set_rgb_color(int spot, COLORREF color);
COLORREF get_rgb_color(int spot);
#endif
