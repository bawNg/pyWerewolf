#!/usr/bin/env python

from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr
from game_data import *

class Callbacks:
    def __init__(self, bot):
        self.irc        = bot
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
        self.callbacks[command.lower()] = callback

    def unreg_callback(self, command):
        command = command.lower()
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

    def run_command(self, command, who, args):
        if command in self.callbacks:
            self.callbacks[command](who, args)
        elif command in Commands.game:
            self.irc.send_notice(who, command + 
                " can only be used when a game is running." +
                " Start one with: !start")
        else:
            self.irc.send_notice(who, command + 
                " is an unknown command." +
                " For the list of commands type: !help")

    def run_join(self, c, e):
        nick    = nm_to_n(e.source())
        self.irc.send_message(self.irc.channel, nick + " has joined the channel")
        if self.join_cb != None:
            self.join_cb(nick)

    def run_leave(self, c, e):
        nick    = nm_to_n(e.source())
        self.irc.send_message(self.irc.channel, nick + " has left the channel")
        if self.leave_cb != None:
            self.leave_cb(nick)
    
    def run_nick(self, c, e):
        target  = e.target()
        nick    = nm_to_n(e.source())
        self.irc.send_message(self.irc.channel, nick + " has change their nick to " + target)
        if self.nick_cb != None:
            self.nick_cb(nick, target)
        
