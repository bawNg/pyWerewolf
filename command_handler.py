#!/usr/bin/env python

from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr

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
        self.irc = bot
        self.c  = bot.connection
        self.callbacks = {}                #callbacks dictionary

    def reg_callback(self, command, callback):
        """command is the command that will be linked to the callback
           callback is the function to be run when that command is ran
                    callbacks have to be in the form of:
                    def cb(who, args):
                    where who is the person who ran the command
                    and args are the args to that command"""
        self.callbacks[command.upper()] = callback

    def unreg_callback(self, command):
        command = command.upper()
        if command in self.callbacks:
            del self.callbacks[command]

    def process_command(self, e, msg):
        target  = e.target()
        nick    = nm_to_n(e.source())

        print "[Command_Handler] Recieved command [%s] from [%s] type [%s]." % \
                    (msg, nick,  e.eventtype().upper())

        try:
            command = msg.split()[0].upper()
            args = msg.split()[1:]

            if command in self.callbacks:
                self.callbacks[command](nick, args)
        except Exception as exc:
            print "Failed to process msg:", msg
            print "from:", nick
            print "reason:", str(exc)

