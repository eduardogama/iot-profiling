# Makefile for profiling IoT

TARGET=main
OBJS=main.o node.o
CFLAGS=-I. -lpthread#-O2 -g -D_GNU_SOURCE -std=c99
LDFLAGS= -fopenmp
CC=g++

%.o : %.cpp
	$(CC) -c $< $(CFLAGS)

all: $(OBJS)
	$(CC) -o $(TARGET) $^ $(CFLAGS)

clean:
	rm -f *.o $(TARGET)


# program_NAME := main
# program_C_SRCS := $(wildcard *.c)
# program_CXX_SRCS := $(wildcard *.cpp)
# program_C_OBJS := ${program_C_SRCS:.c=.o}
# program_CXX_OBJS := ${program_CXX_SRCS:.cpp=.o}
# program_OBJS := $(program_C_OBJS) $(program_CXX_OBJS)
# # program_INCLUDE_DIRS :=
# # program_LIBRARY_DIRS :=
# # program_LIBRARIES :=
#
# CPPFLAGS += $(foreach includedir,$(program_INCLUDE_DIRS),-I$(includedir))
# LDFLAGS += $(foreach librarydir,$(program_LIBRARY_DIRS),-L$(librarydir))
# LDFLAGS += $(foreach library,$(program_LIBRARIES),-l$(library))
#
# .PHONY: all clean distclean
#
# all: $(program_NAME)
#
# $(program_NAME): $(program_OBJS)
#    $(LINK.cc) $(program_OBJS) -o $(program_NAME)
#
# clean:
#    @- $(RM) $(program_NAME)
#    @- $(RM) $(program_OBJS)
#
# distclean: clean
