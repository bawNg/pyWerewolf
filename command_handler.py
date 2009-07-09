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

    def process_command(self, e, msg):
        target  = e.target()
        nick        = nm_to_n(e.source())

        print "[Command_Handler] Recieved command [%s] from [%s] type [%s]." % \
                    (msg, nick,  e.eventtype().upper())

        msg_event = Command_Message(e, msg)
        if msg_event.target == self.c.get_nickname(): msg_event.target = nick

        cmd = "cmd_" + msg.split(" ")[0]
        do_cmd = getattr(self, "cmd_unknown")
        if hasattr(self, cmd): do_cmd = getattr(self, cmd)
        do_cmd(self.c, msg_event)

    def cmd_hello(self, c, e):
        c.privmsg(e.target, "Hello %s!" % e.nick)

    def cmd_disconnect(self, c, e):
        self.irc.disconnect()

    def cmd_die(self, c, e):
        self.irc.die()

    def cmd_unknown(self, c, e):
        c.notice(e.nick, "Unknown command: %s" % e.command)

