#!/usr/bin/env python

from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr
import game_data

class Command_Message:
    def __init__(self, e, msg):
        self.event_type = e.eventtype()             # event type is pubmsg, privmsg,etc
        self.source         = e.source()            # source user's nick mask
        self.target         = e.target()            # target user/channel to reply to
        self.nick           = nm_to_n(e.source())   # source user's nickname
        self.raw_message    = msg                   # raw message sent by user
        self.command        = msg.split(" ")[0]     # command string is the first word
        self.payload        = None                  # payload is the first argument
        self.args           = None                  # all arguments given after command
        if len(msg.split(" ")) >= 2:
            self.payload = msg.split(" ")[1]
            self.args    = msg.split(" ")[1:]


class Command_Handler:
    def __init__(self, bot):
        self.irc        = bot
        self.c          = bot.connection
        self.callbacks  = {}

    def process_command(self, e, msg):
        if msg.strip() == "": return
        target  = e.target()
        nick    = nm_to_n(e.source())

        print "[Command_Handler] Recieved command [%s] from [%s] type [%s]." % \
                    (msg, nick,  e.eventtype().upper())

        e_msg = Command_Message(e, msg)

        if hasattr(self, e_msg.command):
            do_cmd = getattr(self, "cmd_" + e_msg.command)
            do_cmd(self.c, e_msg)
        else:
            if e_msg.command in self.callbacks:
                self.callbacks[e_msg.command](e_msg.nick, *e_msg.args)
            elif e_msg.command in game_data.Commands.game:
                self.irc.send_notice(e_msg.nick, e_msg.command +
                    " can only be used when a game is running." +
                    " Start one with: !start")
            else:
                self.irc.send_notice(who, e_msg.command +
                    " is an unknown command." +
                    " For the list of commands type: !help")

            try:
                self.process_command_callback(e_msg.command, \
                                              e_msg.nick, e_msg.args)
            except Exception as exc:
                print "Failed to process command message [%s] from nick [%s]." \
                        % (e_msg.raw_message, e_msg.nick)
                raise

    def help(self, who, e):
        self.irc.send_notice(who, "To start of a game of Werewolf type: !start")
        self.irc.send_notice(who, "To join a running game," +
                              " while joins are being accepted, type: !join")
        self.irc.send_notice(who, "While a game is running and talking is" +
                        " allowed, to name a random player type: !randplayer")
        self.irc.send_notice(who, "The rest of the commands will be explained" +
                                    " in game just read my messages.")

    def cmd_die(self, who, e):
        if self.irc.is_admin(who):
            self.irc.die(msg="rAwr")
        else:
            self.irc.send_message("Help! %s tried to kill me :'(" % who)

    def cmd_end(self, who, e):
        if self.irc.is_admin(who):
            self.irc.end_game()
        else:
            self.irc.send_message("Help! %s tried to end my fun :'(" % who)

    def reg_callback(self, command, callback):
        """command is the command that will be linked to the callback
           callback is the function to be run when that command is ran
                    callbacks have to be in the form of:
                    def cb(who, args):
                    where who is the person who ran the command
                    and args are the args to that command"""
        self.callbacks[command.lower()] = callback

    def unreg_callback(self, command):
        if command.lower() in self.callbacks:
            del self.callbacks[command.lower()]