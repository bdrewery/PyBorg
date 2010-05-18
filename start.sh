#! /bin/sh

if ! [ -d data ]; then
  mkdir data
fi
cd data/
nice python ../pyborg/pyborg-irc.py
