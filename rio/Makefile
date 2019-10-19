CC = gcc
LD = gcc
CFLAGS = -c -Wall
OBJS = main.o rio.o riob.o

main: $(OBJS)
	$(CC) -o $@ $^

main.o: main.c rio.h
	$(CC) $(CFLAGS) -o $@ $<

rio.o: rio.c rio.h
	$(CC) $(CFLAGS) -o $@ $<

riob.o: riob.c rio.h
	$(CC) $(CFLAGS) -o $@ $<

.PHOTY: clean

clean:
	rm $(OBJS)
