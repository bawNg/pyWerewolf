#!/usr/bin/env python

from player import *
import config
from game_data import *
import random

class Game(object):
    def __init__(self, bot, who):
        self.irc = bot
        self.c  = bot.connection
        self.timers = bot.timers
        self.theme = Theme()
        self.players = {}
        self.wolves = []
        self.mode = Mode.join
        self._start(who)

    def _chan_message(self, message_list):
        self.irc.send_message(self.irc.channel,
                              self.theme.get_string(message_list))

    def _notice(self, who, message_list):
        self.irc.send_notice(who,
                             self.theme.get_string(message_list))

    def _add_player(self, who):
        self.players[who.lower()] = Player(who)

    def _rem_player(self, who):
        if who.lower() in self.players:
            del self.players[who.lower()]

    def _check_win(self):
        #TODO: end game if win and print appropriate messages
        return False#TODO: count num wolves and num villagers

    def _assign_roles(self):
        num_players     = len(self.players)
        num_wolves      = num_players//5
        num_angels      = 1
        num_traitors    = 1
        num_guardians   = num_players//9
        num_seers       = num_players//6

        if num_wolves < 1:
            num_wolves = 1
        if num_seers < 1:
            num_seers = 1

        num_villagers   = num_players-num_wolves-num_angels-num_traitors- \
                            num_guardians-num_seers

        if num_villagers <= 0:
            num_villagers += num_angels
            num_angels = 0
            num_villagers += num_traitors
            num_traitors = 0

        roles = []
        for i in xrange(num_wolves):
            roles.append(Wolf())
        for i in xrange(num_angels):
            roles.append(Angel())
        for i in xrange(num_traitors):
            roles.append(Traitor())
        for i in xrange(num_guardians):
            roles.append(Guardian())
        for i in xrange(num_seers):
            roles.append(Seer())
        for i in xrange(num_villagers):
            roles.append(Villager())

        random.shuffle(roles)

        for i, player in enumerate(self.players.keys()):
            self.players[player].role = roles[i]
            print self.players[player].nick, self.theme.role_names[roles[i].role],
            print self.theme.role_names[roles[i].appears_as]
            role = roles[i].role
            who = self.players[player].nick
            self.theme.reset()
            self.theme.user = who
            self._notice(who, self.theme.role_message[role])
            if role == Role.wolf:
                self.wolves.append(who)

        if num_wolves >= 2:
            for i in xrange(len(self.wolves)):
                other_wolves = []
                for j in xrange(i):
                    other_wolves.append(self.wolves[j])
                for j in xrange(i+1, len(self.wolves)):
                    other_wolves.append(self.wolves[j])
                self.theme.reset()
                self.theme.user = self.wolves[i]
                who = self.wolves[i]
                self.theme.wolves = " ".join(other_wolves)
                if len(other_wolves) == 1:
                    self._notice(who, self.theme.role_other_message[Role.wolf])
                else:
                    self._notice(who, self.theme.role_others_message[Role.wolf])
        if num_wolves > 1:
            self.theme.reset()
            self.theme.num = str(num_wolves)
            self._chan_message(self.theme.role_num_message[Role.wolf])
        if num_seers > 1:
            self.theme.reset()
            self.theme.num = str(num_seers)
            self._chan_message(self.theme.role_num_message[Role.seer])
        if num_guardians > 1:
            self.theme.reset()
            self.theme.num = str(num_guardians)
            self._chan_message(self.theme.role_num_message[Role.guardian])
        if num_angels > 1:
            self.theme.reset()
            self.theme.num = str(num_angels)
            self._chan_message(self.theme.role_num_message[Role.angel])
            
    def _is_alive(self, role):
        for player in self.players:
            if role == self.players[player].role.role:
                return True
        return False

    def _num(self, role):
        ans = 0
        for player in self.players:
            if role == self.players[player].role.role:
                ans += 1
        return ans
    
    def _reset_players(self):
        for player in self.players:
            self.players[player].reset()
            
    def _start(self, who):
        #register callbacks
        for cb in Commands.game:
            self.irc.callbacks.reg_callback(cb, getattr(self, cb))
        self.irc.callbacks.reg_leave_callback(self.player_leave)
        self.irc.callbacks.reg_nick_callback(self.player_nick)

        #setup game info
        self.theme.reset()
        self.theme.user = who
        self.theme.num = Consts.join_time
        self._chan_message(self.theme.game_start_message)
        self._add_player(who)
        self.timers.add_timer(Consts.join_time, self.join_end)

    def restart(self, who, args):
        self._notice(who, self.theme.game_started_message)

    def end(self):
        for cb in Commands.game:
            self.irc.callbacks.unreg_callback(cb)
        self.irc.callbacks.unreg_leave_callback()
        self.irc.callbacks.unreg_nick_callback()
        self.timers.remove_all()
        self.irc.reset_modes()

    def join_end(self):
        if len(self.players) >= Consts.min_players:
            self.irc.reset_modes()
            self.irc.set_moderated()
            self.theme.reset()
            self.theme.num = str(len(self.players))
            self._chan_message(self.theme.join_end_message)
            self._chan_message(self.theme.join_success_message)
            self._assign_roles()
            self.theme.reset()
            self._chan_message(self.theme.night_first_message)
            self.night_start()
        else:
            self.theme.reset()
            self._chan_message(self.theme.join_fail_message)
            self.irc.end_game()

    def night_start(self):
        self.theme.reset()
        time = 0
        if self._num(Role.wolf) == 1:
            time = Consts.night_wolf_time
        else:
            time = Consts.night_wolves_time
    
        self.theme.num = time
        self.mode = Mode.night
        for role in [Role.wolf, Role.seer, Role.guardian]:
            if self._is_alive(role):
                if self._num(role) == 1:
                    self._chan_message(self.theme.night_player_message[role])
                else:
                    self._chan_message(self.theme.night_players_message[role])
        self.timers.add_timer(time, self.night_end)

    def night_end(self):
        #TODO: output results of night
        if not self._check_win():
            self.day_start()

    def day_start(self):
        #TODO: voice everyone
        self.mode = Mode.day_talk
        self.theme.reset()
        self.theme.num = Consts.talk_time
        self._chan_message(self.theme.day_start_message)
        self.timers.add_timer(Consts.talk_time, self.vote_start)

    def vote_start(self):
        #TODO: tell people how to vote
        self.theme.reset()
        self.theme.num = Consts.vote_time
        self._chan_message(self.theme.vote_start_message)
        self.timers.add_timer(Consts.vote_time, self.vote_end)
        pass

    def vote_end(self):
        self.theme.reset()
        self._chan_message(self.theme.vote_end_message)
        
        #TODO: unvoice everyone
        #TODO: tally votes
        #TODO: kill player
        #TODO: check win
        #TODO: show night after vote message
        #TODO: start_night
        pass

    def join(self, who, args):
        if self.mode == Mode.join:
            if who.lower() not in self.players:
                self._add_player(who)
                self.theme.reset()
                self.theme.user = who
                self.theme.num  = str(len(self.players))
                self._chan_message(self.theme.join_new_message)
                time = Consts.join_extend_time
                if self.timers.get_timer(self.join_end).time_left < time:
                    self.timers.get_timer(self.join_end).set_timeleft(time)
            else:
                self.theme.reset()
                self.theme.user = who
                self._notice(who, self.theme.join_old_message)
        else:
            self._notice(who, self.theme.join_ended_message)

    def leave(self, who, args=None):
        if who.lower() in self.players:
            self.theme.reset()
            self.theme.user = self.theme.target = who
            if self.mode != Mode.join:
                role = self.players[who.lower()].role.role
                self._chan_message(self.theme.leave_kill_message[role])
                self._rem_player(who)
                self._check_win()
            else:
                self._chan_message(self.theme.join_leave_message)
                self._rem_player(who)

    def vote(self, who, args):
        if who.lower() in self.players:
            if len(args) == 1:
                if self.mode == Mode.day_vote:
                    target = args[0]
                    if target.lower() in self.players:
                        #TODO update vote nd output
                        pass
                    else:
                        self.theme.reset()
                        self.theme.target = target
                        self._notice(who, self.theme.vote_invalid_target_message)
                else:
                    self.theme.reset()
                    self.theme.user = self.theme.target = who
                    self._notice(who, self.theme.vote_not_vote_time_message)
            else:
                self.theme.reset()
                self.theme.user = self.theme.target = who
                self._notice(who, self.theme.vote_invalid_message)
        else:
            self.theme.reset()
            self.theme.user = self.theme.target = who
            self._notice(who, self.theme.not_player_message)

    def kill(self, who, args):
        if who.lower() in self.players:
            if len(args) == 1:
                if self.mode == Mode.night:
                    #TODO: update vote and output
                    pass
                else:
                    #TODO: output not valid time
                    pass
            else:
                #TODO: output invalid format
                pass
        else:
            self.theme.reset()
            self.theme.user = self.theme.target = who
            self._notice(who, self.theme.not_player_message)

    def guard(self, who, args):
        if who.lower() in self.players:
            if len(args) == 1:
                if self.mode == Mode.day_vote:
                    #TODO: update vote and output
                    pass
                else:
                    #TODO: output not valid time
                    pass
            else:
                #TODO: output invalid format
                pass
        else:
            self.theme.reset()
            self.theme.user = self.theme.target = who
            self._notice(who, self.theme.not_player_message)

    def see(self, who, args):
        if who.lower() in self.players:
            if len(args) == 1:
                if self.mode == Mode.day_vote:
                    #TODO: update vote and output
                    pass
                else:
                    #TODO: output not valid time
                    pass
            else:
                #TODO: output invalid format
                pass
        else:
            self.theme.reset()
            self.theme.user = self.theme.target = who
            self._notice(who, self.theme.not_player_message)

    def randplayer(self, who, args):
        if self.mode in [Mode.day_talk, Mode.day_vote]:
            tplayers = []
            for player in self.players:
                tplayers.append(player.nick)
            user = tplayers[random.randint(0, len(tplayers)-1)]
            self.theme.reset()
            self.theme.user = self.theme.target = user
            self._chan_message(self.theme.randplayer_message)

    def player_leave(self, who):
        self.leave(who)

    def player_nick(self, old, new):
        """player nick change"""
        if old.lower() in self.players:
            self.theme.reset()
            self.theme.user = self.theme.target = old 
            if self.mode != Mode.join:
                role = self.players[old.lower()].role.role
                self._chan_message(self.theme.leave_kill_message[role])
                self._rem_player(old)
                self._check_win()
            else:
                self._chan_message(self.theme.join_leave_nick_message)
                self._rem_player(old)

