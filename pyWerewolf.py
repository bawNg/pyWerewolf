#!/usr/bin/env python

import sys
from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr

from command_handler import *
from game import *
import config

class WerewolfBot(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.command_handler = Command_Handler(self)
        self.connection.add_global_handler("all_events", self.on_all_events, -100)
        self.game = None
        self.command_handler.reg_callback("start", self.start_game)
        #TODO: remove these callbacks
        self.command_handler.reg_callback("die", self.cmd_die)
        self.command_handler.reg_callback("end", self.end_game)
        import ircbot
        print ircbot

    ### IRC Events ###
    def on_all_events(self, c, e):
        if e.eventtype() != "all_raw_messages":
            print e.source(), e.eventtype().upper(), e.target(), e.arguments()

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_nicknameinuse(self, c, e):
        for n in config.irc.nickname:
            if n != c.get_nickname():
                c.nick(n)
                break
        if c.get_nickname() != config.irc.nickname[0]:
            c.nick(config.irc.nickname[0])
        c.nick(c.get_nickname() + "_")

    def on_privmsg(self, c, e):
        msg = e.arguments()[0]
        if (msg[:1] == "!") and ((msg.find("!",1,4) & msg.find("?",1,4)) == -1):
            msg = msg[1:]
        self.command_handler.process_command(e, msg)

    def on_pubmsg(self, c, e):
        msg = e.arguments()[0]
        a = msg.split(":", 1)
        if len(a) > 1 and irc_lower(a[0]) == irc_lower(c.get_nickname()):
            self.command_handler.process_command(e, a[1].strip())
        elif msg[:1] == "!" and ((msg.find("!",1,4) & msg.find("?",1,4)) == -1):
            self.command_handler.process_command(e, msg[1:])

    def on_privnotice(self, c, e):
        nick = nm_to_n(e.source())
        msg  = e.arguments()[0]
        if (nick == "NickServ") and \
        (msg.startswith("This nickname is registered and protected.")):
            c.privmsg(nick, "identify %s" % config.irc.password)

    def on_kick(self, c, e):
        self.command_handler.process_leave(e)

    def on_part(self, c, e):
        self.command_handler.process_leave(e)
        
    def on_quit(self, c, e):
        self.command_handler.process_leave(e)

    def on_join(self, c, e):
        self.command_handler.process_join(e)

    def on_nick(self, c, e):
        self.command_handler.process_nick(e)

    ### Wrapper Methods ###
    def send_message(self, target, msg):
        self.connection.privmsg(target, msg)

    def send_notice(self, target, msg):
        self.connection.privnotice(target, msg)

    ### Game Management Methods ###
    def start_game(self, who, args):
        if self.game == None:
            self.game = Game(self)
            #TODO: add player in who started game
    
    def end_game(self):
        self.game = None

    ### Miscellaneous ###
    def cmd_die(self, who, args):
        self.die()

def main():
    if len(sys.argv) is 5:
        bot = WerewolfBot(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))
    elif len(sys.argv) is not 1:
        print "Usage:\n\tpyWerewolf.py [<#channel> <nickname> <server> <port>]"
        sys.exit(1)
    else:
        bot = WerewolfBot(config.irc.channel, config.irc.nickname[0], \
                                    config.irc.server, config.irc.port)
    try:
        bot.start()
    except KeyboardInterrupt:
        print "^C - Exiting gracefully..."
        bot.disconnect(msg="Terminated at terminal")
        sys.exit(0)

if __name__ == "__main__":
    main()
