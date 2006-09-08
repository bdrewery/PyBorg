#!/usr/bin/env python
#
# PyBorg: The python AI bot.
#
#
# Use to convert pyborg 1.0.6 dictionaries to the
# version 1.1.0+ format.
#
# Copyright (c) 2006 Sebastien Dailly
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

print "Reading dictionary..."
try:
	f = open("words.dat", "rb")
	s = f.read()
	f.close()
	self.words = marshal.loads(s)
	del s
	f = open("lines.dat", "rb")
	s = f.read()
	f.close()
	self.lines = marshal.loads(s)
	del s
except (EOFError, IOError), e:
	pass
	

#change the contexts here !
compteur = 0
for x in self.lines.keys():
	self.lines[x]=[self.lines[x],1]
	compteur = 1
if compteur != 0:
	print "Contexts update done"

print "Writing dictionary..."

zfile = zipfile.ZipFile('archive.zip','r')
for filename in zfile.namelist():
	data = zfile.read(filename)
	file = open(filename, 'w+b')
	file.write(data)
	file.close()

f = open("words.dat", "wb")
s = marshal.dumps(self.words)
f.write(s)
f.close()
f = open("lines.dat", "wb")
s = marshal.dumps(self.lines)
f.write(s)
f.close()

#zip the files
f = zipfile.ZipFile('archive.zip','w',zipfile.ZIP_DEFLATED)
f.write('words.dat')
f.write('lines.dat')
f.close()

try:		
	os.remove('words.dat')
	os.remove('lines.dat')
except (OSError, IOError), e:
	print "could not remove the files"

f.close()
