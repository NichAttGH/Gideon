# Makefile per BWSTATES su Ubuntu 22

# Sopprime i warning durante la compilazione (opzionale)
# WARNINGS = -w

##########################################################################
# DIRECTORY DI DESTINAZIONE                                              #
##########################################################################

# Dove installare l'eseguibile (puoi cambiare in /usr/local/bin se preferisci)
BIN = ./

# Directory per le pagine del manuale
MANROOT = /usr/local/man
MANSECT = 1

##########################################################################
# Imposta SIZE al numero massimo di blocchi che ti serviranno.           #
# Il requisito di memoria è quadratico rispetto a SIZE.                  #
##########################################################################

SIZE = 200

##########################################################################
# Compilatore e flag                                                      #
##########################################################################

CC = gcc
MAXBLOCKS = -DSZ=$(SIZE)
CFLAGS = -O2 $(WARNINGS) $(MAXBLOCKS)
MANDIR = $(MANROOT)/man$(MANSECT)

# Per Ubuntu, usa semplicemente -lm per la libreria matematica
MATHLIB = -lm

##########################################################################
# Target di compilazione                                                  #
##########################################################################

all: bwstates

bwstates: bwstates.o
	$(CC) $(CFLAGS) bwstates.o -o bwstates $(MATHLIB)

bwstates.o: bwstates.c bwstates.h
	$(CC) $(CFLAGS) -c bwstates.c

README: README.ms
	nroff -ms README.ms > README

install_bwstates: bwstates
	cp bwstates $(BIN)
	chmod 755 $(BIN)/bwstates

install_man:
	sudo mkdir -p $(MANDIR)
	sudo cp bwstates.man $(MANDIR)/bwstates.$(MANSECT)
	sudo chmod 644 $(MANDIR)/bwstates.$(MANSECT)
	
install: install_bwstates install_man

clean:
	rm -f *.o core bwstates README

# Per rimuovere l'installazione
deinstall:
	rm -f $(BIN)/bwstates
	sudo rm -f $(MANDIR)/bwstates.$(MANSECT)*

.PHONY: all install install_bwstates install_man clean deinstall