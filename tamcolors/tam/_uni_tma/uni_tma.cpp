//built in libraries
#include <termios.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <unistd.h>


/*
C++ API to linux console
can get dimension of console
get key input in the background
*/

typedef struct Dimension{
	short width;
	short height;
} Dimension;

Dimension get_dimension() {
    /*
	info: will return Dimension info width and height
	return: Dimension
	*/
    struct winsize windowSize;
    ioctl(STDOUT_FILENO, TIOCGWINSZ, &windowSize);
    Dimension dimension;
    dimension.width = windowSize.ws_col;
    dimension.height = windowSize.ws_row;
    return dimension;
}

void enable_get_key(){
    /*
	info: will enable terminal for kbhit and get_key
	turns off echo and other settings
	*/
    termios term;
    tcgetattr(0, &term);

    termios term2 = term;

    term2.c_lflag &= ~ICANON;
    term2.c_lflag &= ~ECHO;
    term2.c_cc[VMIN] = 1;
    term2.c_cc[VTIME] = 0;
    tcsetattr(0, TCSANOW, &term2);
}

void disable_get_key(){
    /*
	info: will reset terminal
	turns on echo and other settings
	*/
    termios term;
    tcgetattr(0, &term);
    term.c_lflag |= ICANON;
    term.c_lflag |= ICANON | ECHO;
    tcsetattr(0, TCSANOW, &term);
}

 bool kbhit(){
    /*
	return: bool
	false: no charter in buffer
	true: charter in buffer
	*/
    termios term;
    tcgetattr(0, &term);

    int byteswaiting;
    ioctl(0, FIONREAD, &byteswaiting);

    tcsetattr(0, TCSANOW, &term);

    return byteswaiting > 0;
}

int get_key() {
    /*
	return: int
	-1: no key data to give
	Not -1: value of key data
	*/
	//check if key data present
    int charter = 0;
    if (kbhit()){
        if (read(0, &charter, 1) < 0){
           return -1;
        }
        return charter;
    }
    return -1;
 }
