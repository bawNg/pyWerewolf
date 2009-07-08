#!/usr/bin/env python

from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr
import config

class WerewolfBot(SingleServerIRCBot):
	def __init__(self, channel, nickname, server, port=6667):
		SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
		self.channel = channel
		self.connection.add_global_handler("all_events", self.on_all_events, -10)

	def on_all_events(self, c, e):
		if e.eventtype() == "all_raw_messages": return
		print "%s %s %s %s" % (e.source(), e.eventtype(), e.target(), e.arguments())

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

	def process_command(self, e, text):
		nick = nm_to_n(e.source())
		c = self.connection

		cmd = "cmd_" + text.lower()
		if hasattr(self, cmd):
			do_cmd = getattr(self, cmd)
			do_cmd(e, text)
		else:
			do_cmd = getattr(self, "cmd_unknown")
			do_cmd(e, text)

############
# COMMANDS #
############

	def cmd_hello(self, e, text):
		c = self.connection
		source_nick = nm_to_n(e.source())
		response = "Hello " + source_nick + "!"

		c.privmsg(self.channel, response)

	def cmd_disconnect(self, e, text):
		self.disconnect()

	def cmd_die(self, e, text):
		self.die()

	def cmd_unknown(self, e, text):
		c = self.connection
		source_nick = nm_to_n(e.source())
		response = "Unknown command: " + text

		c.notice(source_nick, response)

def main():
	bot = WerewolfBot(config.irc.channel, config.irc.nickname, \
							config.irc.server, config.irc.port)
	bot.start()

if __name__ == "__main__":
	main()