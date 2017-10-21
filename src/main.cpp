#include <iostream>
#include <string>

#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

#include "version.h"
#include "node.h"

extern void addNode();
extern void *loop(void *t);
extern void setup();

void teste(int a){}
void teste(double a){}

int main(int argc, char const *argv[]) {

	std::cout << "IoT Profiling " << AutoVersion::IOT_PROFILING_VERSION << std::endl;

	pthread_t *threads;
	int i,n=10;
	threads = (pthread_t *)malloc(sizeof(pthread_t) * n);

	setup();

	//Node *gateway = new Node();

	for(i = 0; i < n; i++ ) {
		std::cout << "main() : creating thread, " << i << std::endl;
		int rc = pthread_create(&threads[i], NULL, loop, (void *)i );

		if (rc) {
			std::cout << "Error:unable to create thread," << rc << std::endl;
			exit(-1);
		}
	}

	// free attribute and wait for the other threads
	// pthread_attr_destroy(&attr);
	for(i = 0; i < n; i++ ) {
		int rc = pthread_join(threads[i], NULL);
		if (rc) {
			std::cout << "Error:unable to join," << rc << std::endl;
			exit(-1);
		}

		std::cout << "Main: completed thread id :" << i ;
		std::cout << "  exiting with status :" << std::endl;
	}

	std::cout << "Main: program exiting." << std::endl;

	pthread_exit(NULL);
}

void addNode(){
}

void setup(){
	addNode();
}

void *loop(void *t){
}
