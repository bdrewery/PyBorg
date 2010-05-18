#! /usr/bin/env python
#
# PyBorg MSN module
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



import time
import sys
import pyborg
import cfgfile
import traceback
import thread
try:
	import msnp
except:
	print "ERROR !!!!\msnp not found, please install it ( http://msnp.sourceforge.net/ )"
	sys.exit(1)

def get_time():
	"""
	Return time as a nice yummy string
	"""
	return time.strftime("%H:%M:%S", time.localtime(time.time()))


class ModMSN(msnp.Session, msnp.ChatCallbacks):

	def __init__(self, my_pyborg, args):
		"""
		Args will be sys.argv (command prompt arguments)
		"""
		# PyBorg
		self.pyborg = my_pyborg
		# load settings
		
		self.settings = cfgfile.cfgset()
		self.settings.load("pyborg-msn.cfg",
			{ "myname": ("The bot's nickname", "PyBorg"),
			  "msn_passport": ("Reported passport account", "passport@hotmail.com"),
			  "msn_password": ("Reported password account", "password"),
			  "owners": ("Owner(s) passport account", [ "owner@hotmail.com" ]),
			  "password": ("password for control the bot (Edit manually !)", "")
			} )


		self.owners = self.settings.owners[:]

	def our_start(self):
		print "Connecting to msn..."
		msnp.Session.__init__(self, self.MsnListener(self))
		self.login(self.settings.msn_passport, self.settings.msn_password)
		
		if self.logged_in: print "connected"
		self.sync_friend_list()
		while True:
			bot.process(chats = True)
			time.sleep(1)

	class MsnListener(msnp.SessionCallbacks):

		def __init__(self, bot):
			self.bot = bot
		
		def chat_started(self, chat):
			callbacks = ModMSN.MsnChatActions(bot)
			chat.callbacks = callbacks
			callbacks.chat = chat


	class MsnChatActions(msnp.ChatCallbacks):

		# Command list for this module
		commandlist =   "MSN Module Commands:\n!nick, !owner"

		# Detailed command description dictionary
		commanddict = {
			"nick": "Owner command. Usage: !nick nickname\nChange nickname",
			"quit": "Owner command. Usage: !quit\nMake the bot quit IRC",
			"owner": "Usage: !owner password\nAllow to become owner of the bot"
		}


		def __init__(self, bot):
			self.bot = bot

		def message_received(self, passport_id, display_name, text, charset):
			print '%s: %s' % (passport_id, text)
			if text[0] == '!':
				if self.msn_command(passport_id, display_name, text, charset) == 1:
					return

			self.chat.send_typing()
			if passport_id in bot.owners:
				bot.pyborg.process_msg(self, text, 100, 1, (charset, display_name, text), owner=1)
			else:
				thread.start_new_thread(bot.pyborg.process_msg, (self, text, 100, 1, (charset, display_name, text)))

		def msn_command(self, passport_id, display_name, text, charset):
			command_list = text.split()
			command_list[0] = command_list[0].lower()

			if command_list[0] == "!owner" and len(command_list) > 1 and passport_id not in bot.owners:
				if command_list[1] == bot.settings.password:
					bot.owners.append(passport_id)
					self.output("You've been added to owners list", (charset, display_name, text))
				else:
					self.output("try again", (charset))


			if passport_id in bot.owners:
				if command_list[0] == '!nick' and len(command_list) > 1:
					bot.change_display_name(command_list[1])
		
		def output(self, message, args):
			charset, display_name, text = args
			
			message = message.replace("#nick", display_name)
			
			print "[%s] <%s> > %s> %s" % ( get_time(), display_name, bot.display_name, text)
			print "[%s] <%s> > %s> %s" % ( get_time(), bot.display_name, display_name, message)
			self.chat.send_message(message, charset)
			


if __name__ == "__main__":
	
	if "--help" in sys.argv:
		print "Pyborg msn bot. Usage:"
		print " pyborg-msn.py"
		print "Defaults stored in pyborg-msn.cfg"
		print
		sys.exit(0)
	# start the pyborg
	my_pyborg = pyborg.pyborg()
	bot = ModMSN(my_pyborg, sys.argv)
	try:
		bot.our_start()

	except KeyboardInterrupt, e:
		pass
	except SystemExit, e:
		pass
	except:
		traceback.print_exc()
		c = raw_input("Ooops! It looks like Pyborg has crashed. Would you like to save its dictionary? (y/n) ")
		if c.lower()[:1] == 'n':
			sys.exit(0)
	bot.logout()
	my_pyborg.save_all()
	del my_pyborg
