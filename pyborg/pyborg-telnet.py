#!/usr/bin/env python
#
# PyBorg Telnet module (fairly raw 'telnet'...)
# Defaults to listening on port 8489
#
# Copyright (c) 2000, 2001 Tom Morton
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
import string
import socket
import SocketServer

import pyborg

class handler(SocketServer.BaseRequestHandler):
	# Command list for this module
	commandlist = "Telnet Module Commands:\n!quit"
	commanddict = {}
	
	def handle(self):
		####
		if ("-v" in sys.argv) or ("--verbose" in sys.argv):
			self.opt_verbose = 1
		else:
			self.opt_verbose = 0
		####
		print "Connection from ", self.request.getpeername()
		self.request.send("\r\nPyborg. Type !quit to leave.\r\n")
		while 1:
			try:
				self.request.send("> ")
				body = ""
				while 1:
					new = self.request.recv(1000)
					if new[-2:] != "\r\n":
						if new == '\x08':
							body = body[:-1]
						else:
							body = body + new
					else:
						body = body + new
						break
			except socket.error, e:
				print "Closed connection to", self.request.getpeername(), ": ", e, e.args
				return
			else:
				if self.opt_verbose:
					print "%s --> \"%s\"" % (self.request.getpeername(), body[:-2])
				# Telnet module commands.
				if string.lower(body[0:5]) == "!quit":
					self.output("Bye", None)
					print "Closed connection to", self.request.getpeername(), ". User quit."
					return
				else:
					my_pyborg.process_msg(self, body, 100, 1, None, owner=0)

	def output(self, message, args):
		"""
		Output pyborg reply.
		"""
		if self.opt_verbose:
			print "%s <-- \"%s\"" % (self.request.getpeername(), message)
		try:
			self.request.send(message+"\r\n")
		except:
			pass	

if __name__ == '__main__':
	# start the damn server
	if "--help" in sys.argv:
		print "Pyborg telnet module."
		print
		print "-v --verbose"
		print "-p --port n      Listen on port n (Defaults to 8489)"
		print
		sys.exit(0)

	port = 8489
	if "-p" in sys.argv or "--port" in sys.argv:
		try:
			x = sys.argv.index("-p")
		except ValueError, e:
			x = sys.argv.index("--port")
		if len(sys.argv) > x+1:
			try:
				port = int(sys.argv[x+1])
			except ValueError, e:
				pass
	try:
		server = SocketServer.ThreadingTCPServer(("", port), handler)
	except socket.error, e:
		print "Socket error: ", e.args
	else:
		print "Starting pyborg..."
		my_pyborg = pyborg.pyborg()
		print "Awaiting connections..."
		try:
			server.serve_forever()
		except KeyboardInterrupt, e:
			print "Server shut down"
		my_pyborg.save_all()
		del my_pyborg

