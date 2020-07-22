#ifndef __LIN_TAM__H_
#define __LIN_TAM__H_


typedef struct Dimension {
	short width;
	short height;
} Dimension;

Dimension get_dimension();
void enable_get_key();
void disable_get_key();
int get_key();
#endif
