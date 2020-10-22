#ifndef __UNI_TAM__H_
#define __UNI_TAM__H_


typedef struct Dimensions {
	short width;
	short height;
} Dimensions;

Dimensions get_dimensions();
void enable_get_key();
void disable_get_key();
int get_key();
#endif
