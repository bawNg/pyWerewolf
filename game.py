#!/usr/bin/env python

#werewolf game logic
from player import *
import config
from game_data import *

class Game(object):
    def __init__(self, bot, who):
        self.irc = bot
        self.c  = bot.connection
        self.execute_delayed = bot.connection.execute_delayed
        self.theme = Theme()
        self.start(who)

    def _chan_message(self, message_list):
        self.irc.send_message(self.irc.channel, 
                              self.theme.get_string(message_list))

    def _notice(self, who, message_list):
        self.irc.send_notice(who, 
                             self.theme.get_string(message_list))
        
    def _add_player(self, who):
        self.players[who] = None

    def _rem_player(self, who):
        pass #remove player from player list and check if game ended

    def start(self, who):
        #register callbacks
        reg = self.irc.command_handler.reg_callback
        reg("join", self.join)

        #setup game info
        self.theme.user = who
        self._chan_message(self.theme.game_start_message)
        self.players = {}
        self.mode = Mode.join
        self._add_player(who)

    def end(self):
        unreg = self.irc.command_handler.unreg_callback
        unreg("join")

    def join(self, who, args):
        if self.mode == Mode.join:
            if who not in self.players:
                self.add_player(who)
                self._chan_message(self.theme.join_new_message)
            else:
                self._notice(who, self.theme.join_old_message)
        
