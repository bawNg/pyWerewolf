#!/usr/bin/env python

import sys
import traceback
from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr

from command_handler import *
from callbacks import *
from game import *
import config

class WerewolfBot(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.command_handler = Command_Handler(self)
        self.connection.add_global_handler("all_events", self.on_all_events, -100)
        self.callbacks = Callbacks(self)
        #game
        self.game = None
        self.callbacks.reg_callback("start", self.start_game)
        self.callbacks.reg_callback("help", self.help)
        #TODO: remove these callbacks
        self.callbacks.admin = ["blaq_phoenix", "shadowmaster", "defi"] 
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

    ### Wrapper Methods ###
    def send_message(self, target, msg):
        self.connection.privmsg(target, msg)

    def send_notice(self, target, msg):
        self.connection.notice(target, msg)

    def voice_users(self, targets):
        self.connection.mode(self.channel, "+%s %s" % \
                             ('v'*len(targets), "".join(targets, " ")))

    ### Game Management Methods ###
    def start_game(self, who, args):
        if self.game == None:
            self.game = Game(self, who)
            #TODO: add player in who started game

    def end_game(self):
        if self.game != None:
            self.game.end()
            self.game = None

    ### Miscellaneous ###
    def help(self, who, args):
        self.send_notice(who, "To start of a game of Werewolf type: !start")
        self.send_notice(who, "To join a running game," +
                              " while joins are being accepted, type: !join")
        self.send_notice(who, "While a game is running and talking is allowed," +
                              " to name a random player type: !randplayer")
        self.send_notice(who, "The rest of the commands will be explained in game" + 
                              " just read my messages.")

    def is_admin(self, nick):
        if nick.lower() in config.irc.admins: return True
        return False

    def cmd_die(self, who, args):
        if self.is_admin(who):
            self.die(msg="RAWR")
        else:
            self.send_message(self.channel, "Help! " + who + " tried to kill me :'(")

    def cmd_end(self, who, args):
        if self.is_admin(who):
            self.end_game()
        else:
            self.send_message(self.channel, "Help! " + who + " tried to end my fun :'(")

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
    except Exception as exc:
        bot.disconnect(msg="Unexpected Error. Sorry Folks.")
        print "traceback:"
        print traceback.print_exc()
        sys.exit(0)

if __name__ == "__main__":
    main()
