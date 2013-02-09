#! /bin/sh

mkdir data 2>/dev/null || :
cd data/

PYTHON=$(which pypy 2>/dev/null)
if [ -z "$PYTHON" ]; then
  PYTHON=python
fi
exec nice ${PYTHON} ../lib/pyborg/pyborg-irc.py
