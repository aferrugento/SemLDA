# (C) Copyright 2004, David M. Blei (blei [at] cs [dot] cmu [dot] edu)

# This file is part of LDA-C.

# LDA-C is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your
# option) any later version.

# LDA-C is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

.SUFFIXES: .c .u
CC= gcc
CFLAGS= -O3 -Wall -g
LDFLAGS= -lm

LOBJECTS= semlda-data.o semlda-estimate.o semlda-model.o semlda-inference.o utils.o cokus.o semlda-alpha.o

LSOURCE= semlda-data.c semlda-estimate.c semlda-model.c semlda-inference.c utils.c cokus.c semlda-alpha.c

lda:	$(LOBJECTS)
	$(CC) $(CFLAGS) $(LOBJECTS) -o semlda $(LDFLAGS)

clean:
	-rm -f *.o
