#include "stdio.h"
#include "DummyLib.h"

int main(int argc, char* argv[]){
		const char* msg = hello();
		printf( "%s\n" , msg );
		return 0;
}
