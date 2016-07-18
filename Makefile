all:
	gcc -I include -Wall src/main.c src/gnuplot_i.c -lm -o bin/ublox
