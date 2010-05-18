#!/usr/bin/env python
#
# Use to convert pyborg 0.9.10 and 0.9.11 dictionaries to the
# version 1.0.0+ format.
#
# Copyright (c) 2000, 2006 Tom Morton, Sebastien Dailly
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#        
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
import sys
import marshal
import struct
import string

# Read the dictionary
print "Reading dictionary stage 1..."

try:
	f = open("lines.dat", "r")
	s = f.read()
	f.close()
	lines = marshal.loads(s)
	del s
except (EOFError, IOError), e:
	print "Error reading dictionary."
	sys.exit()

print "working..."
for x in lines.keys():
	# clean up whitespace mess
	line = lines[x]
	words = string.split(line)
	lines[x] = string.join(words, " ")

print "Saving Dictionary..."

f = open("lines.dat", "w")
s = marshal.dumps(lines)
f.write(s)
f.close()

# Read the dictionary
print "Reading dictionary stage 2..."

try:
	f = open("words.dat", "r")
	s = f.read()
	f.close()
	words = marshal.loads(s)
	del s
except (EOFError, IOError), e:
	print "Error reading dictionary."
	sys.exit()

print "working..."
for key in words.keys():
	# marshallise it:
	y = []
	for i in words[key]:
		y.append(struct.pack("iH", i[0], i[1]))
	words[key] = y

print "Saving Dictionary..."

f = open("words.dat", "w")
s = marshal.dumps(words)
f.write(s)
f.close()
print "Done."

