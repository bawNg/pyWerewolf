#!/usr/bin/env python

from player import *
import config
from game_data import *
import random

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
        self.players[who.lower()] = (None, who)

    def _rem_player(self, who):
        pass #remove player from player list and check if game ended

    def _can_start_game(self):
        return len(self.players) >= 5

    def _assign_roles(self):
        num_players = len(self.players)
        num_wolves = 1        

    def start(self, who):
        #register callbacks
        for cb in Commands.game:
            self.irc.callbacks.reg_callback(cb, getattr(self, cb))
        self.irc.callbacks.reg_leave_callback(self.player_leave)
        self.irc.callbacks.reg_nick_callback(self.player_nick)

        #setup game info
        self.theme.user = who
        self._chan_message(self.theme.game_start_message)
        self.players = {}
        self.mode = Mode.join
        self._add_player(who)

    def end(self):
        for cb in Commands.game:
            self.irc.callbacks.unreg_callback(cb)
        self.irc.callbacks.unreg_leave_callback()
        self.irc.callbacks.unreg_nick_callback()

    def join_ends(self):
        pass

    def join(self, who, args):
        if self.mode == Mode.join:
            if who.lower() not in self.players:
                self._add_player(who)
                self.theme.user = who
                self.theme.num  = str(len(self.players))
                self._chan_message(self.theme.join_new_message)
            else:
                self._notice(who, self.theme.join_old_message)
    
    def vote(self, who, args):
        pass
    
    def kill(self, who, args):
        pass
    
    def guard(self, who, args):
        pass

    def see(self, who, args):
        pass

    def randplayer(self, who, args):
        if self.mode in [Mode.day_talk, Mode.day_vote]:
            tplayers = []
            for player in self.players:
                tplayers.append(player[1])
            self.theme.user = tplayers[random.randint(0, len(tplayers)-1)]
            #TODO: print to channnel the random name
    
    def player_leave(self, who):
        self._rem_player(who)
    
    def player_nick(self, old, new):
        """player nick change"""
        self.player_leave(old)

