CC = gcc
CFLAGS = -Wall -c -pthread
LD = gcc
LDFLAGS = -pthread

OBJS = main.o utils.o

.PHONY: clean

main: $(OBJS)
	$(LD) $(LDFLAGS) -o $@ $^

main.o: main.c utils.h config.h
	$(CC) $(CFLAGS) -o $@ $<

utils.o: utils.c utils.h
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm $(OBJS)