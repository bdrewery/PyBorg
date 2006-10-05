#!/usr/bin/env python
#
# PyBorg ascii file input module
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
import string
import sys

import pyborg

class ModFileIn:
	"""
	Module for file input. Learning from ASCII text files.
	"""

	# Command list for this module
	commandlist = "FileIn Module Commands:\nNone"
	commanddict = {}
	
	def __init__(self, Borg, args):

		f = open(args[1], "r")
		buffer = f.read()
		f.close()

		print "I knew "+`Borg.settings.num_words`+" words ("+`len(Borg.lines)`+" lines) before reading "+sys.argv[1]
		buffer = pyborg.filter_message(buffer, Borg)
		# Learn from input
		try:
			print buffer
			Borg.learn(buffer)
		except KeyboardInterrupt, e:
			# Close database cleanly
			print "Premature termination :-("
		print "I know "+`Borg.settings.num_words`+" words ("+`len(Borg.lines)`+" lines) now."
		del Borg

	def shutdown(self):
		pass

	def start(self):
		sys.exit()

	def output(self, message, args):
		pass

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Specify a filename."
		sys.exit()
	# start the pyborg
	my_pyborg = pyborg.pyborg()
	ModFileIn(my_pyborg, sys.argv)
	my_pyborg.save_all()
	del my_pyborg

