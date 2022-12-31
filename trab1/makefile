    CC     = gcc -g
    CFLAGS =
    LFLAGS = -lm

      PROG = transport
      OBJS = ./$(PROG).o \
             ./memHandler.o \
             ./problem.o \
             ./utils.o \

.PHONY: limpa faxina clean distclean purge all

%.o: ./%.c ./%.h
	$(CC) -c $(CFLAGS) $<

$(PROG):  $(OBJS)
	$(CC) -o $@ $^ $(LFLAGS)

clean: purge
	@rm -f *~ *.bak

purge:
	@rm -f *.o core a.out
	@rm -f $(PROG)
	@rm -f $(OBJS)

