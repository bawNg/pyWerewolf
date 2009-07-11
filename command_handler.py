#!/usr/bin/env python

from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr
import game_data

class Command:
    start       = 0 #command to start game
    help        = 1 #command to get help
    join        = 2 #command to join game
    leave       = 3 #command to leave game
    kill        = 4 #command to kill
    guard       = 5 #command to guard
    see         = 6 #command to see
    vote        = 7 #command to vote
    randplayer  = 8 #command to choose random player
    num         = 9 #num commands

class Command_Message:
    def __init__(self, e, msg):
        self.event_type = e.eventtype()             # event type is pubmsg, privmsg,etc
        self.source         = e.source()            # source user's nick mask
        self.target         = e.target()            # target user/channel to reply to
        self.nick           = nm_to_n(e.source())   # source user's nickname
        self.raw_message    = msg                   # raw message sent by user
        self.command        = msg.split()[0].lower()# command string is the first word
        self.payload        = None                  # payload is the first argument
        self.args           = None                  # all arguments given after command
        if len(msg.split()) >= 2:
            self.payload = msg.split()[1]
            self.args    = msg.split()[1:]

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

        if hasattr(self, "cmd_" + e_msg.command):
            do_cmd = getattr(self, "cmd_" + e_msg.command)
            do_cmd(self.c, e_msg)
        else:
            if e_msg.command in self.callbacks:
                try:
                    self.callbacks[e_msg.command](e_msg.nick, e_msg.args)
                except Exception as exc:
                    print "Failed to process command [%s] from nick [%s]." \
                            % (e_msg.raw_message, e_msg.nick)
                    raise
            elif e_msg.command in game_data.Commands.game:
                #TODO: get these messages from themes
                self.irc.send_notice(e_msg.nick, e_msg.command +
                    " can only be used when a game is running." +
                    " Start one with: !start")
            else:
                self.irc.send_notice(e_msg.nick, e_msg.command +
                    " is an unknown command." +
                    " For the list of commands type: !help")


    def cmd_help(self, c, e):
        #TODO: Move out to theme class
        self.irc.send_notice(e.nick, "To start of a game of Werewolf type: !start")
        self.irc.send_notice(e.nick, "To join a running game," +
                              " while joins are being accepted, type: !join")
        self.irc.send_notice(e.nick, "While a game is running and talking is" +
                        " allowed, to name a random player type: !randplayer")
        self.irc.send_notice(e.nick, "The rest of the commands will be explained" +
                                    " in game just read my messages.")

    def cmd_say(self, c, e):
        if self.irc.is_admin(e.nick):
            c.privmsg(e.payload, e.raw_message[len(e.command)+len(e.payload)+2:])

    def cmd_send(self, c, e):
        if self.irc.is_admin(e.nick):
            c.send_raw(e.raw_message[len(e.command)+1:])

    def cmd_die(self, c, e):
        if self.irc.is_admin(e.nick):
            self.irc.die(msg="rAwr")
        else:
            self.irc.send_message("Help! %s tried to kill me :'(" % e.nick)

    def cmd_end(self, c, e):
        if self.irc.is_admin(e.nick):
            self.irc.end_game()
        else:
            self.irc.send_message("Help! %s tried to end my fun :'(" % e.nick)

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
