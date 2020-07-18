#ifndef __LIN_TMA__H_
#define __LIN_TMA__H_

//Charles McMarrow

typedef struct Dimension {
	short width;
	short height;
} Dimension;

Dimension get_dimension();
void enable_get_key();
void disable_get_key();
int get_key();
#endif
