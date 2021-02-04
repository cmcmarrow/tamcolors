//built in libraries
#include <termios.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <stdbool.h>

// non apple libraries
#ifdef __unix__
#include <X11/Xlib.h>
#include <X11/keysym.h>
#endif


/*
C++ API to linux console
can get dimension of console
get key input in the background
*/

typedef struct Dimensions{
	short width;
	short height;
} Dimensions;

Dimensions get_dimensions() {
    /*
	info: will return Dimensions info width and height
	return: Dimensions
	*/
    struct winsize windowSize;
    ioctl(STDOUT_FILENO, TIOCGWINSZ, &windowSize);
    Dimensions dimensions;
    dimensions.width = windowSize.ws_col;
    dimensions.height = windowSize.ws_row;
    return dimensions;
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

#ifdef __unix__
bool get_key_state(int key){
    char keys_return[32];
    Display* display = XOpenDisplay(NULL);
    if (display == NULL){
        return false;
    }
    XQueryKeymap(display, keys_return);
    KeyCode key_code = XKeysymToKeycode(display, key);
    XCloseDisplay(display);
    return !!(keys_return[key_code>>3] & (1<<(key_code&7)));
 }
#endif

#ifdef __APPLE__
bool get_key_state(int key){
    return false;
}
#endif
