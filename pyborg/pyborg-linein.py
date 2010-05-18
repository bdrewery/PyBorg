#!/usr/bin/env python
#
# PyBorg Offline line input module
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

class ModLineIn:
	"""
	Module to interface console input and output with the PyBorg learn
	and reply modules. Allows offline chat with PyBorg.
	"""
	# Command list for this module
	commandlist = "LineIn Module Commands:\n!quit"
	commanddict = { "quit": "Usage: !quit\nQuits pyborg and saves the dictionary" }

	def __init__(self, my_pyborg):
		self.pyborg = my_pyborg
		self.start()

	def start(self):
		print "PyBorg offline chat!\n"
		print "Type !quit to leave"
		print "What is your name"
		name = raw_input("? ")
		while 1:
			try:
				body = raw_input("> ")
			except (KeyboardInterrupt, EOFError), e:
				print
				return
			if body == "":
				continue
			if body[0] == "!":
				if self.linein_commands(body):
					continue
			# Pass message to borg
			self.pyborg.process_msg(self, body, 100, 1, ( name ), owner = 1)

	def linein_commands(self, body):
		command_list = string.split(body)
		command_list[0] = string.lower(command_list[0])

		if command_list[0] == "!quit":
			sys.exit(0)

	def output(self, message, args):
		"""
		Output a line of text.
		"""
		message = message.replace("#nick", args)
		print message

if __name__ == "__main__":
	# start the pyborg
	my_pyborg = pyborg.pyborg()
	try:
		ModLineIn(my_pyborg)
	except SystemExit:
		pass
	my_pyborg.save_all()
	del my_pyborg

