#! /bin/sh

if ! [ -d data ]; then
  mkdir data
fi
cd data/
exec nice python ../lib/pyborg/pyborg-irc.py
