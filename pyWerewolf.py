#!/usr/bin/env python

import sys
import traceback
import string
from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr

from command_handler import *
from timers import *
from callbacks import *
from game import *
import config

class WerewolfBot(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.command_handler = Command_Handler(self)
        self.connection.add_global_handler("all_events", self.on_all_events, -100)
        self.timers = Timers()
        self.callbacks = Callbacks(self)

        #game
        self.game = None
        self.callbacks.reg_callback("start", self.start_game)
        self.callbacks.reg_callback("help", self.help)
        #TODO: remove these callbacks
        self.callbacks.reg_callback("die", self.cmd_die)
        self.callbacks.reg_callback("end", self.cmd_end)

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
        self.on_quit(c, e)

    def on_part(self, c, e):
        self.on_quit(c, e)

    def on_quit(self, c, e):
        self.callbacks.run_leave(c, e)

    def on_join(self, c, e):
        self.callbacks.run_join(c, e)

    def on_nick(self, c, e):
        self.callbacks.run_nick(c, e)

    def on_mode(self, c, e):
        nick = nm_to_n(e.source())
        if (nick == "ChanServ") and (e.arguments()[1] == c.get_nickname()):
            if e.arguments()[0].startswith("+") and "o" in e.arguments()[0]:
                self.reset_modes()

    ### Wrapper Methods ###
    def send_message(self, *args):
        if len(args) == 1:
            self.connection.privmsg(self.channel, args[0])
        elif len(args) == 2:
            self.connection.privmsg(args[0], args[1])

    def send_notice(self, target, msg):
        self.connection.notice(target, msg)

    def reset_modes(self):
        voiced_nicks = self.channels[self.channel].voiced()
        self.set_moderated(False)
        self.devoice_users(voiced_nicks,True)

    def unvoice_everyone(self):
        voiced_nicks = self.channels[self.channel].voiced()
        self.devoice_users(voiced_nicks)

    def set_modes(self, modes):
        self.connection.mode(self.channel, modes)

    def set_moderated(self, moderated=True):
        self.set_modes("%sm" % ('+' if moderated else '-'))

    def voice_users(self, targets):
        for start in range(0, len(targets), 12):
            end = start+12
            if len(targets) < end: end = len(targets)
            nicks = ""
            for t in targets[start:end]: nicks += "%s " % t
            modes = "+%s %s" % ('v'*(end-start), nicks)
            self.set_modes(modes)

    def devoice_users(self, targets, unmoderate=False):
        for start in range(0, len(targets), 12):
            end = start+12
            if len(targets) < end: end = len(targets)
            nicks = ""
            for t in targets[start:end]: nicks += "%s " % t
            modes = "+%s %s" % ('v'*(end-start), nicks)
            if unmoderate: modes = "-m%s" % modes[1:]
            self.set_modes(modes)

    ### Game Management Methods ###
    def start_game(self, who, args):
        if not self.game:
            self.game = Game(self, who)
        else:
            self.game.restart(who, args)

    def end_game(self):
        if self.game:
            self.game.end()
            self.game = None

    ### Miscellaneous ###
    def is_admin(self, nick):
        if nick.lower() in config.irc.admins: return True
        return False
    def process_forever(self):
        self._connect()
        while 1:
            self.ircobj.process_once(0.2)
            self.timers.process_timeout()

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
        bot.process_forever()
    except KeyboardInterrupt:
        print "^C - Exiting gracefully..."
        bot.disconnect(msg="Terminated at terminal")
        sys.exit(0)
    except Exception as exc:
        bot.disconnect(msg="Unexpected Error. Sorry Folks.")
        print "traceback:"
        print traceback.print_exc()
        sys.exit(0)

if __name__ == "__main__":
    main()
