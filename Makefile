.SUFFIXES:
.SUFFIXES: .o .cpp

CC=g++
FLAGS=-O3 -Wall -msse -msse2 -msse3 -march=native -fopenmp -c
CFLAGS=$(FLAGS)
CXXFLAGS=-std=c++11 $(FLAGS)
LD=$(CXX)
LDFLAGS=-std=c++11 -Wall -fopenmp

%.o: %.c
	$(CC) $(CFLAGS) $*.c

%.o: %.cpp
	$(CXX) $(CXXFLAGS) $*.cpp

monte: monte.o
	$(LD) $(LDFLAGS) $^ -o $@

all: monte

clean:
	rm -rf *.o monte
