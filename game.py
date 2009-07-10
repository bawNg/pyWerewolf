#!/usr/bin/env python

#werewolf game logic
from player import *
import config

class Game(object):
    def __init__(self, bot, who):
        bot.send_message(bot.channel, "Game started")
        self.irc = bot
        self.c  = bot.connection
        self.execute_delayed = bot.connection.execute_delayed
        self.players = {}
        self.can_join = True
        self.start()

    def start(self):
        reg = self.irc.command_handler.reg_callback
        reg("join", self.join)

    def end(self):
        unreg = self.irc.command_handler.unreg_callback
        unreg("join")

    def join(self, who, args):
        if self.can_join:
            if who not in self.players:
                self.players[who] = None
                self.irc.send_message(self.irc.channel, who + " joined the hunt")
            else:
                self.irc.send_notice(who, "You are already in game")
        
    def signup(self): #hold game signups
        pass

    def assign_roles(self,): #assign player roles
        pass

    def night_cycle(self,):
        pass

    def day_cycle(self,):
        pass

    def vote_tally(self,):
        pass

