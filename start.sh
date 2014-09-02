#! /bin/sh

PYTHON=$(which pypy 2>/dev/null)
if [ -z "$PYTHON" ]; then
  PYTHON=python
fi

# Ensure the proper symlinks are there. Github's .zip archiving
# does not properly extract them.

if ! [ -L lib/pyborg/irclib.py ]; then
	rm -f lib/pyborg/irclib.py lib/pyborg/ircbot.py lib/pyborg/atomicfile.py
	ln -s ../irclib/irclib.py lib/pyborg/irclib.py
	ln -s ../irclib/ircbot.py lib/pyborg/ircbot.py
	ln -s ../atomicfile/atomicfile.py lib/pyborg/atomicfile.py
fi

DATADIR=${1:-data}
PYBORG=${2:-pyborg-irc.py}

mkdir $DATADIR 2>/dev/null || :
cd ${DATADIR}/

exec nice ${PYTHON} ../lib/pyborg/${PYBORG}
