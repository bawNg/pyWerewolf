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
        self.callbacks  = {}    #callbacks dictionary
        self.nick_cb    = None  #nick callback      -when user renames
        self.join_cb    = None  #join callback      - when user joins channel
        self.leave_cb   = None  #leave callback     - when user leaves channel

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

    def reg_nick_callback(self, callback):
        """callback is the function that will be called when a user
           changes their nick.
           callback must be of the form:
                def cb(old, new):
                where old is the old nick and new is the new one"""
        self.nick_cb = callback

    def unreg_nick_callback(self):
        self.nick_cb = None

    def reg_join_callback(self, callback):
        """callback is the function that will be called when a user
           joins the channel.
           callback must be of the form:
                def cb(user):
                where user is the name of the user"""
        self.join_cb = callback

    def unreg_join_callback(self):
        self.join_cb = None

    def reg_leave_callback(self, callback):
        """callback is the function that will be called when a user
           leaves the channel.
           callback must be of the form:
                def cb(user):
                where user is the name of the user"""
        self.leave_cb = callback

    def unreg_leave_callback(self):
        self.leave_cb = None

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
            self.irc.send_message
            print "Failed to process msg:", msg
            print "from:", nick
            print "reason:", str(exc)

    def process_nick(self, e):
        target  = e.target()
        nick    = nm_to_n(e.source())
        self.irc.send_message(self.irc.channel, nick + " has change their nick to " + target)
        if self.nick_cb != None:
            self.nick_cb(nick, target)
        pass

    def process_join(self, e):
        nick    = nm_to_n(e.source())
        self.irc.send_message(self.irc.channel, nick + " has joined the channel")
        if self.join_cb != None:
            self.join_cb(nick)
        pass

    def process_leave(self, e):
        nick    = nm_to_n(e.source())
        self.irc.send_message(self.irc.channel, nick + " has left the channel")
        if self.leave_cb != None:
            self.leave_cb(nick)
        pass

