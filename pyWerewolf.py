#!/usr/bin/env python

from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr

class WerewolfBot(SingleServerIRCBot):
	def __init__(self, channel, nickname, server, port=6667):
		SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
		self.channel = channel

	def on_nicknameinuse(self, c, e):
		c.nick(c.get_nickname() + "_")

	def on_welcome(self, c, e):
		c.join(self.channel)

	def on_privmsg(self, c, e):
		pass

	def on_pubmsg(self, c, e):
		a = e.arguments()[0].split(":", 1)
		if len(a) > 1 and irc_lower(a[0]) == irc_lower(self.connection.get_nickname()):
			self.process_command(e, a[1].strip())
			return

	def process_command(self, e, cmd):
		nick = nm_to_n(e.source())
		c = self.connection

		if cmd == "hello":
			c.privmsg(self.channel, "Hello " + nm_to_n(e.source()) + "!")
		elif cmd == "disconnect":
			self.disconnect()
		elif cmd == "die":
			self.die()
		else:
			c.notice(nick, "Unknown command: " + cmd)

def main():
	server = "za.shadowfire.org"
	port = 6667
	channel = "#werewolf.dev"
	nickname = "pyWerewolf"

	bot = WerewolfBot(channel, nickname, server, port)
	bot.start()

if __name__ == "__main__":
	main()