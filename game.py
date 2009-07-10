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
        pass #TODO: remove player from player list and check if game ended
    
    def _check_win(self):
        return False#TODO: count num wolves and num villagers

    def _can_start_game(self):
        return len(self.players) >= 5

    def _assign_roles(self):
        num_players     = len(self.players)
        num_wolves      = num_players//5
        num_angels      = 1
        num_traitors    = 1
        num_guards      = num_players//9
        num_seers       = num_players//6
        num_villagers   = num_players-num_wolves-num_angels-num_traitors- \
                            num_guards-num_seers
        if num_wolves < 1:
            num_wolves = 1
        if num_seers < 1:
            num_seers = 1
        roles = []
        for i in xrange(num_wolves):
            roles.append(Wolf())
        for i in xrange(num_angels):
            roles.append(Angel())
        for i in xrange(num_traitors):
            roles.append(Traitor())
        for i in xrange(num_guards):
            roles.append(Guard())
        for i in xrange(num_seers):
            roles.append(Seer())
        for i in xrange(num_villagers):
            roles.append(Villager())
        random.shuffle(roles)
        for i, player in enumerate(self.players.keys()):
            self.players[player][0] = roles[i]
            print self.players[player][1], self.theme.roles[roles[i].role]
            #TODO: Output player roles

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
        #TODO: start join end timer

    def end(self):
        for cb in Commands.game:
            self.irc.callbacks.unreg_callback(cb)
        self.irc.callbacks.unreg_leave_callback()
        self.irc.callbacks.unreg_nick_callback()
        #TODO: kill timers

    def join_end(self):
        if self._can_start_game():
            #TODO: Unvoice everyone
            #TODO: moderate channel
            self._assign_roles()
            #TODO: Start Night
            pass
        else:
            #TODO: tell too few players
            self.irc.end_game()

    def night_start(self):
        #TODO: tell alive roles what to do
        #TODO: start timers
        pass

    def night_end(self):
        #TODO: output results of night
        if not self._check_win():
            #TODO: start day
            pass

    def day_start(self):
        #TODO: Voice alive people
        #TODO: start vote start timer
        pass

    def vote_start(self):
        #TODO: tell people how to vote
        #TODO: start vote end timer
        pass

    def vote_end(self):
        #TODO: unvoice everyone
        #TODO: tally votes
        #TODO: kill player
        #TODO: check win
        #TODO: start_night
        pass

    def join(self, who, args):
        if self.mode == Mode.join:
            if who.lower() not in self.players:
                self._add_player(who)
                self.theme.user = who
                self.theme.num  = str(len(self.players))
                self._chan_message(self.theme.join_new_message)
                #TODO: update timeleft
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

